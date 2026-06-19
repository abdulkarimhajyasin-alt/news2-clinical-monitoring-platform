from __future__ import annotations

import json
from collections import Counter, defaultdict
from statistics import median

from sqlalchemy.orm import Session

from app.models import Alert, DialysisSession, IntradialyticMeasurement, News2Assessment, OutcomeValidation72h, Patient


PREDICTION_CLASSES = [
    "true_positive_early",
    "true_positive_concurrent",
    "false_negative",
    "true_negative",
    "false_positive",
    "incomplete",
]


def classify_session_prediction(
    *,
    validation_completed: bool,
    deterioration_occurred: bool | None,
    prediction_status: str | None,
    red_alert_present: bool,
) -> dict[str, object]:
    if not validation_completed:
        return {"prediction_classification": "incomplete", "classification_reason": "72-hour validation is missing"}
    if deterioration_occurred is None:
        return {"prediction_classification": "incomplete", "classification_reason": "Deterioration occurrence is missing"}
    if deterioration_occurred:
        if prediction_status == "predicted_before":
            return {"prediction_classification": "true_positive_early", "classification_reason": "Deterioration occurred and platform predicted before event"}
        if prediction_status == "predicted_concurrent":
            return {"prediction_classification": "true_positive_concurrent", "classification_reason": "Deterioration occurred and platform predicted at event time"}
        if prediction_status in {"not_predicted", "false_negative"}:
            return {"prediction_classification": "false_negative", "classification_reason": "Deterioration occurred without effective platform prediction"}
        return {"prediction_classification": "incomplete", "classification_reason": "Prediction status is missing for deteriorated session"}
    if red_alert_present:
        return {"prediction_classification": "false_positive", "classification_reason": "No deterioration occurred but HD2-mNEWS red alert was present"}
    return {"prediction_classification": "true_negative", "classification_reason": "No deterioration occurred and no HD2-mNEWS red alert was present"}


def build_prediction_evaluation_dataset(db: Session) -> list[dict[str, object]]:
    sessions = (
        db.query(DialysisSession)
        .join(Patient, DialysisSession.patient_id == Patient.id)
        .filter(Patient.status != "deleted")
        .order_by(DialysisSession.session_date.desc(), DialysisSession.id.desc())
        .all()
    )
    return [_session_prediction_row(db, session) for session in sessions]


def build_prediction_summary(db: Session) -> dict[str, object]:
    rows = build_prediction_evaluation_dataset(db)
    validated_rows = [row for row in rows if row["outcome_validation_completed"]]
    non_deteriorated = [row for row in validated_rows if row["deterioration_occurred"] is False]
    deteriorated = [row for row in validated_rows if row["deterioration_occurred"] is True]
    counts = Counter(row["prediction_classification"] for row in rows)
    tp_early = counts["true_positive_early"]
    tp_concurrent = counts["true_positive_concurrent"]
    tp_total = tp_early + tp_concurrent
    fn = counts["false_negative"]
    tn = counts["true_negative"]
    fp = counts["false_positive"]
    return {
        "total_sessions": len(rows),
        "validated_sessions": len(validated_rows),
        "unvalidated_sessions": len(rows) - len(validated_rows),
        "deteriorated_sessions": len(deteriorated),
        "non_deteriorated_sessions": len(non_deteriorated),
        "true_positive_early": tp_early,
        "true_positive_concurrent": tp_concurrent,
        "true_positive_total": tp_total,
        "false_negative": fn,
        "true_negative": tn,
        "false_positive": fp,
        "incomplete_classification_count": counts["incomplete"],
        "sensitivity": _safe_rate(tp_total, tp_total + fn),
        "specificity": _safe_rate(tn, tn + fp),
        "positive_predictive_value": _safe_rate(tp_total, tp_total + fp),
        "negative_predictive_value": _safe_rate(tn, tn + fn),
        "early_detection_rate": _safe_rate(tp_early, len(deteriorated)),
        "false_negative_rate": _safe_rate(fn, len(deteriorated)),
        "false_positive_rate": _safe_rate(fp, len(non_deteriorated)),
    }


def build_prediction_by_risk_color(db: Session) -> list[dict[str, object]]:
    rows = build_prediction_evaluation_dataset(db)
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("hd2_risk_color") or "none"].append(row)
    return [_group_summary("risk_color", risk_color, group_rows) for risk_color, group_rows in sorted(grouped.items())]


def build_prediction_by_deterioration_type(db: Session) -> list[dict[str, object]]:
    rows = build_prediction_evaluation_dataset(db)
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        types = row.get("deterioration_types") or []
        if not types:
            grouped["none"].append(row)
        for deterioration_type in types:
            grouped[str(deterioration_type)].append(row)
    return [_group_summary("deterioration_type", deterioration_type, group_rows) for deterioration_type, group_rows in sorted(grouped.items())]


def build_response_time_prediction_summary(db: Session) -> dict[str, object]:
    rows = [row for row in build_prediction_evaluation_dataset(db) if row.get("doctor_response_time_minutes") is not None]
    values = [int(row["doctor_response_time_minutes"]) for row in rows]
    by_class = {}
    for prediction_class in PREDICTION_CLASSES:
        class_values = [int(row["doctor_response_time_minutes"]) for row in rows if row["prediction_classification"] == prediction_class]
        by_class[prediction_class] = _response_stats(class_values)
    return {"records_with_doctor_response_time": len(values), **_response_stats(values), "by_prediction_classification": by_class}


def prediction_export_fields_for_session(db: Session, session_id: int) -> dict[str, object]:
    session = db.get(DialysisSession, session_id)
    if session is None:
        return _empty_prediction_export()
    row = _session_prediction_row(db, session)
    classification = row["prediction_classification"]
    return {
        "prediction_classification": classification,
        "true_positive_early": classification == "true_positive_early",
        "true_positive_concurrent": classification == "true_positive_concurrent",
        "false_negative": classification == "false_negative",
        "true_negative": classification == "true_negative",
        "false_positive": classification == "false_positive",
        "sensitivity_group_marker": classification in {"true_positive_early", "true_positive_concurrent", "false_negative"},
        "specificity_group_marker": classification in {"true_negative", "false_positive"},
        "early_detection_marker": classification == "true_positive_early",
        "classification_reason": row["classification_reason"],
    }


def _session_prediction_row(db: Session, session: DialysisSession) -> dict[str, object]:
    patient = db.get(Patient, session.patient_id)
    validation = db.query(OutcomeValidation72h).filter(OutcomeValidation72h.dialysis_session_id == session.id).first()
    assessments = (
        db.query(News2Assessment)
        .filter(News2Assessment.dialysis_session_id == session.id)
        .order_by(News2Assessment.hd2_mnews_total_score.desc().nullslast(), News2Assessment.id.desc())
        .all()
    )
    top_assessment = assessments[0] if assessments else None
    red_alert_present = any(assessment.hd2_mnews_risk_color == "red" for assessment in assessments) or _has_hd2_high_alert(db, session.id)
    classification = classify_session_prediction(
        validation_completed=validation is not None,
        deterioration_occurred=validation.deterioration_occurred if validation else None,
        prediction_status=validation.platform_prediction_status if validation else None,
        red_alert_present=red_alert_present,
    )
    return {
        "patient_id": patient.id if patient else session.patient_id,
        "patient_code": patient.patient_code if patient else None,
        "session_id": session.id,
        "session_date": session.session_date,
        "session_start_time": session.actual_start_time,
        "hd2_mnews_total_score": top_assessment.hd2_mnews_total_score if top_assessment else None,
        "hd2_risk_color": top_assessment.hd2_mnews_risk_color if top_assessment else None,
        "hd2_risk_label_ar": top_assessment.hd2_mnews_risk_label_ar if top_assessment else None,
        "critical_trigger_present": top_assessment.hd2_mnews_critical_trigger if top_assessment else None,
        "critical_trigger_reasons": _json_list(top_assessment.hd2_mnews_critical_reasons if top_assessment else None),
        "red_alert_present": red_alert_present,
        "outcome_validation_completed": validation is not None,
        "deterioration_occurred": validation.deterioration_occurred if validation else None,
        "deterioration_types": _json_list(validation.deterioration_types if validation else None),
        "deterioration_timing": validation.deterioration_timing_category if validation else None,
        "prediction_status_from_validation": validation.platform_prediction_status if validation else None,
        "doctor_response_time_minutes": validation.doctor_response_time_minutes if validation else None,
        "final_result": validation.final_result if validation else None,
        "verification_sources": _json_list(validation.verification_sources if validation else None),
        **classification,
    }


def _has_hd2_high_alert(db: Session, session_id: int) -> bool:
    alerts = db.query(Alert).filter(Alert.dialysis_session_id == session_id).all()
    return any(alert.risk_level == "high" and alert.trigger_reason and "HD2-mNEWS" in alert.trigger_reason for alert in alerts)


def _group_summary(key: str, value: str, rows: list[dict[str, object]]) -> dict[str, object]:
    counts = Counter(row["prediction_classification"] for row in rows)
    return {
        key: value,
        "total_sessions": len(rows),
        "validated_sessions": sum(1 for row in rows if row["outcome_validation_completed"]),
        "true_positive_early": counts["true_positive_early"],
        "true_positive_concurrent": counts["true_positive_concurrent"],
        "false_negative": counts["false_negative"],
        "true_negative": counts["true_negative"],
        "false_positive": counts["false_positive"],
        "incomplete": counts["incomplete"],
    }


def _response_stats(values: list[int]) -> dict[str, object]:
    return {
        "count": len(values),
        "average_minutes": round(sum(values) / len(values), 1) if values else None,
        "median_minutes": float(median(values)) if values else None,
        "fastest_minutes": min(values) if values else None,
        "slowest_minutes": max(values) if values else None,
    }


def _safe_rate(numerator: int, denominator: int) -> float | None:
    return round((numerator / denominator) * 100, 1) if denominator else None


def _json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        return []
    return loaded if isinstance(loaded, list) else []


def _empty_prediction_export() -> dict[str, object]:
    return {
        "prediction_classification": None,
        "true_positive_early": False,
        "true_positive_concurrent": False,
        "false_negative": False,
        "true_negative": False,
        "false_positive": False,
        "sensitivity_group_marker": False,
        "specificity_group_marker": False,
        "early_detection_marker": False,
        "classification_reason": None,
    }
