from collections import Counter, defaultdict
from statistics import median

from sqlalchemy.orm import Session

from app.services.export_service import build_research_dataset, validate_research_dataset


NEWS2_BUCKETS = [
    ("0_2", "منخفض جدا", lambda value: value <= 2),
    ("3_4", "منخفض", lambda value: 3 <= value <= 4),
    ("5_6", "متوسط", lambda value: 5 <= value <= 6),
    ("7_plus", "مرتفع", lambda value: value >= 7),
]

OUTCOME_TYPES = [
    "stable_completed_session",
    "session_stopped_early",
    "hospital_admission",
    "emergency_department_transfer",
    "icu_admission",
    "death",
]

DETERIORATION_TYPES = [
    "acute_hypotension",
    "suspected_sepsis_or_fever",
    "arrhythmia",
    "seizures",
    "reduced_consciousness",
    "other",
]


def build_research_kpis(db: Session) -> dict[str, object]:
    rows = build_research_dataset(db)
    quality = validate_research_dataset(rows)
    sessions = _unique_count(rows, "dialysis_session_id")
    alerts = _unique_count(rows, "alert_id")
    events = _unique_count(rows, "clinical_deterioration_event_id")
    responses = _unique_count(rows, "clinical_response_id")
    outcomes = _unique_count(rows, "clinical_outcome_id")
    response_values = _numeric_values(rows, "time_to_response_minutes")
    return {
        "total_patients": _unique_count(rows, "patient_code"),
        "total_sessions": sessions,
        "total_measurements": _unique_count(rows, "measurement_id"),
        "total_news2_assessments": _unique_count(rows, "news2_assessment_id"),
        "total_alerts": alerts,
        "total_deterioration_events": events,
        "total_responses": responses,
        "total_outcomes": outcomes,
        "average_news2_score": _average(rows, "news2_total_score"),
        "average_response_time_minutes": _average(rows, "time_to_response_minutes"),
        "alerts_per_100_sessions": round((alerts / sessions) * 100, 1) if sessions else 0,
        "deterioration_rate": round((events / sessions) * 100, 1) if sessions else 0,
        "response_completion_rate": round((responses / alerts) * 100, 1) if alerts else 0,
        "outcome_completion_rate": round((outcomes / events) * 100, 1) if events else 0,
        "dataset_quality_score": quality["quality_score"],
        "export_readiness": "ready" if rows and quality["quality_score"] >= 80 else "needs_review",
        "fastest_response": min(response_values) if response_values else None,
        "slowest_response": max(response_values) if response_values else None,
    }


def build_news2_distribution(db: Session) -> list[dict[str, object]]:
    rows = build_research_dataset(db)
    scores = [int(row["news2_total_score"]) for row in rows if row.get("news2_total_score") is not None]
    total = len(scores)
    items = []
    for key, label, predicate in NEWS2_BUCKETS:
        count = sum(1 for score in scores if predicate(score))
        items.append({"bucket": key, "label": label, "count": count, "percentage": 0})
    return _with_percentages(items, total)


def build_risk_level_distribution(db: Session) -> list[dict[str, object]]:
    rows = build_research_dataset(db)
    total = len(rows)
    items = []
    for risk in ["low", "medium", "high"]:
        risk_rows = [row for row in rows if row.get("risk_level") == risk]
        items.append(
            {
                "risk_level": risk,
                "count": len(risk_rows),
                "percentage": 0,
                "outcome_distribution": _counter_dict(risk_rows, "outcome_type", OUTCOME_TYPES),
                "average_response_time": _average(risk_rows, "time_to_response_minutes"),
            }
        )
    return _with_percentages(items, total)


def build_outcome_distribution(db: Session) -> dict[str, object]:
    rows = build_research_dataset(db)
    outcome_rows = [row for row in rows if row.get("outcome_type")]
    total = len(outcome_rows)
    items = [{"outcome_type": outcome_type, "count": _count_value(outcome_rows, "outcome_type", outcome_type), "percentage": 0} for outcome_type in OUTCOME_TYPES]
    distribution = _with_percentages(items, total)
    good_count = _count_value(outcome_rows, "outcome_type", "stable_completed_session")
    adverse_count = sum(_count_value(outcome_rows, "outcome_type", outcome_type) for outcome_type in ["hospital_admission", "emergency_department_transfer", "icu_admission", "death"])
    return {
        "total_outcomes": total,
        "distribution": distribution,
        "good_outcome_rate": round((good_count / total) * 100, 1) if total else 0,
        "adverse_outcome_rate": round((adverse_count / total) * 100, 1) if total else 0,
    }


def build_response_time_analysis(db: Session) -> dict[str, object]:
    rows = build_research_dataset(db)
    response_values = _numeric_values(rows, "time_to_response_minutes")
    return {
        "average_time_to_alert": _average(rows, "time_to_alert_minutes"),
        "average_time_to_view": _average(rows, "time_to_view_minutes"),
        "average_time_to_response": _average(rows, "time_to_response_minutes"),
        "average_time_to_action": _average(rows, "time_to_action_minutes"),
        "average_total_response_time": _average(rows, "total_response_time_minutes"),
        "fastest_response": min(response_values) if response_values else None,
        "slowest_response": max(response_values) if response_values else None,
        "median_response": float(median(response_values)) if response_values else None,
        "records_with_response": len(response_values),
    }


def build_deterioration_analysis(db: Session) -> list[dict[str, object]]:
    rows = build_research_dataset(db)
    event_rows = [row for row in rows if row.get("clinical_deterioration_event_id")]
    total = len(event_rows)
    items = []
    for deterioration_type in DETERIORATION_TYPES:
        type_rows = [row for row in event_rows if row.get("deterioration_type") == deterioration_type]
        items.append(
            {
                "deterioration_type": deterioration_type,
                "count": len(type_rows),
                "percentage": 0,
                "associated_outcomes": _counter_dict(type_rows, "outcome_type", OUTCOME_TYPES),
            }
        )
    return _with_percentages(items, total)


def build_group_comparison(db: Session) -> dict[str, object]:
    rows = build_research_dataset(db)
    return {
        "study_group": _comparison_for(rows, "study_group"),
        "study_phase": _comparison_for(rows, "study_phase"),
        "pre_post_placeholder": {
            "baseline_period": _group_metrics([row for row in rows if row.get("study_phase") == "pre_implementation"]),
            "intervention_period": _group_metrics([row for row in rows if row.get("study_phase") == "post_implementation"]),
            "inferential_analysis": "not_implemented",
        },
    }


def build_analytics_summary(db: Session) -> dict[str, object]:
    return {
        "kpis": build_research_kpis(db),
        "news2_distribution": build_news2_distribution(db),
        "risk_level_distribution": build_risk_level_distribution(db),
        "outcome_analysis": build_outcome_distribution(db),
        "response_time_analysis": build_response_time_analysis(db),
        "deterioration_analysis": build_deterioration_analysis(db),
        "group_comparison": build_group_comparison(db),
    }


def _comparison_for(rows: list[dict[str, object]], key: str) -> dict[str, object]:
    groups = sorted({row.get(key) for row in rows if row.get(key)})
    group_a = groups[0] if groups else None
    group_b = groups[1] if len(groups) > 1 else None
    return {
        "group_a": {"name": group_a, **_group_metrics([row for row in rows if row.get(key) == group_a])} if group_a else _empty_group(),
        "group_b": {"name": group_b, **_group_metrics([row for row in rows if row.get(key) == group_b])} if group_b else _empty_group(),
    }


def _group_metrics(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "count": len(rows),
        "average_news2": _average(rows, "news2_total_score"),
        "average_response_time": _average(rows, "time_to_response_minutes"),
        "outcome_distribution": _counter_dict(rows, "outcome_type", OUTCOME_TYPES),
    }


def _empty_group() -> dict[str, object]:
    return {"name": None, "count": 0, "average_news2": None, "average_response_time": None, "outcome_distribution": {}}


def _unique_count(rows: list[dict[str, object]], key: str) -> int:
    return len({row.get(key) for row in rows if row.get(key) is not None})


def _numeric_values(rows: list[dict[str, object]], key: str) -> list[float]:
    return [float(row[key]) for row in rows if row.get(key) is not None]


def _average(rows: list[dict[str, object]], key: str) -> float | None:
    values = _numeric_values(rows, key)
    return round(sum(values) / len(values), 1) if values else None


def _count_value(rows: list[dict[str, object]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def _counter_dict(rows: list[dict[str, object]], key: str, defaults: list[str]) -> dict[str, int]:
    counts = Counter(row.get(key) for row in rows if row.get(key))
    return {value: counts.get(value, 0) for value in defaults}


def _with_percentages(items: list[dict[str, object]], total: int) -> list[dict[str, object]]:
    if not total:
        return items
    running = 0.0
    last_index = len(items) - 1
    for index, item in enumerate(items):
        if index == last_index:
            item["percentage"] = round(100.0 - running, 1)
        else:
            percentage = round((int(item["count"]) / total) * 100, 1)
            item["percentage"] = percentage
            running += percentage
    return items
