from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models import Alert, ClinicalDeteriorationEvent, ClinicalOutcome, ClinicalResponse, DialysisSession, IntradialyticMeasurement, News2Assessment, Patient, ResponseTracking
from app.services.export_service import build_research_dataset, validate_research_dataset


def get_research_summary(db: Session) -> dict[str, int | float | None]:
    active_alerts = db.query(Alert).filter(Alert.status != "closed").count()
    average_news2 = db.query(func.avg(News2Assessment.total_score)).scalar()
    average_response_delay = db.query(func.avg(ClinicalResponse.response_delay_minutes)).scalar()
    fastest_response_delay = db.query(func.min(ClinicalResponse.response_delay_minutes)).scalar()
    slowest_response_delay = db.query(func.max(ClinicalResponse.response_delay_minutes)).scalar()
    average_time_to_alert = db.query(func.avg(ResponseTracking.time_to_alert_minutes)).scalar()
    average_time_to_response = db.query(func.avg(ResponseTracking.time_to_response_minutes)).scalar()
    fastest_response = db.query(func.min(ResponseTracking.time_to_response_minutes)).scalar()
    slowest_response = db.query(func.max(ResponseTracking.time_to_response_minutes)).scalar()
    alerts_without_response = db.query(ResponseTracking).filter(ResponseTracking.time_to_response_minutes.is_(None)).count()
    deterioration_counts = {
        row_type: count
        for row_type, count in db.query(ClinicalDeteriorationEvent.deterioration_type, func.count(ClinicalDeteriorationEvent.id))
        .group_by(ClinicalDeteriorationEvent.deterioration_type)
        .all()
    }
    outcome_counts = {
        row_type: count
        for row_type, count in db.query(ClinicalOutcome.outcome_type, func.count(ClinicalOutcome.id))
        .group_by(ClinicalOutcome.outcome_type)
        .all()
    }
    outcomes_count = db.query(ClinicalOutcome).count()
    dataset_rows = build_research_dataset(db)
    dataset_quality = validate_research_dataset(dataset_rows)
    missing_outcomes = dataset_quality["issues_by_type"].get("missing_outcome_for_deterioration", 0)
    quality_score = int(dataset_quality["quality_score"])
    return {
        "patients_count": db.query(Patient).count(),
        "sessions_count": db.query(DialysisSession).count(),
        "measurements_count": db.query(IntradialyticMeasurement).count(),
        "news2_assessments_count": db.query(News2Assessment).count(),
        "alerts_count": db.query(Alert).count(),
        "active_alerts_count": active_alerts,
        "deterioration_events_count": db.query(ClinicalDeteriorationEvent).count(),
        "acute_hypotension_count": deterioration_counts.get("acute_hypotension", 0),
        "suspected_sepsis_or_fever_count": deterioration_counts.get("suspected_sepsis_or_fever", 0),
        "arrhythmia_count": deterioration_counts.get("arrhythmia", 0),
        "seizures_count": deterioration_counts.get("seizures", 0),
        "reduced_consciousness_count": deterioration_counts.get("reduced_consciousness", 0),
        "responses_count": db.query(ClinicalResponse).count(),
        "clinical_responses_count": db.query(ClinicalResponse).count(),
        "average_response_delay_minutes": round(float(average_response_delay), 1) if average_response_delay is not None else None,
        "fastest_response_delay_minutes": int(fastest_response_delay) if fastest_response_delay is not None else None,
        "slowest_response_delay_minutes": int(slowest_response_delay) if slowest_response_delay is not None else None,
        "average_time_to_alert_minutes": round(float(average_time_to_alert), 1) if average_time_to_alert is not None else None,
        "average_time_to_response_minutes": round(float(average_time_to_response), 1) if average_time_to_response is not None else None,
        "fastest_response_minutes": int(fastest_response) if fastest_response is not None else None,
        "slowest_response_minutes": int(slowest_response) if slowest_response is not None else None,
        "alerts_without_response_count": alerts_without_response,
        "outcomes_count": outcomes_count,
        "total_outcomes": outcomes_count,
        "stable_completed_session_count": outcome_counts.get("stable_completed_session", 0),
        "session_stopped_early_count": outcome_counts.get("session_stopped_early", 0),
        "hospital_admission_count": outcome_counts.get("hospital_admission", 0),
        "emergency_department_transfer_count": outcome_counts.get("emergency_department_transfer", 0),
        "icu_admission_count": outcome_counts.get("icu_admission", 0),
        "death_count": outcome_counts.get("death", 0),
        "research_dataset_rows": len(dataset_rows),
        "dataset_quality_score": quality_score,
        "missing_outcomes_count": missing_outcomes,
        "export_readiness": "ready" if quality_score >= 80 and len(dataset_rows) > 0 else "needs_review",
        "average_news2": round(float(average_news2), 1) if average_news2 is not None else None,
    }
