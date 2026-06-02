from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models import Alert, ClinicalDeteriorationEvent, ClinicalOutcome, ClinicalResponse, DialysisSession, IntradialyticMeasurement, News2Assessment, Patient


def get_research_summary(db: Session) -> dict[str, int | float | None]:
    active_alerts = db.query(Alert).filter(Alert.status != "closed").count()
    average_news2 = db.query(func.avg(News2Assessment.total_score)).scalar()
    return {
        "patients_count": db.query(Patient).count(),
        "sessions_count": db.query(DialysisSession).count(),
        "measurements_count": db.query(IntradialyticMeasurement).count(),
        "news2_assessments_count": db.query(News2Assessment).count(),
        "alerts_count": db.query(Alert).count(),
        "active_alerts_count": active_alerts,
        "deterioration_events_count": db.query(ClinicalDeteriorationEvent).count(),
        "responses_count": db.query(ClinicalResponse).count(),
        "outcomes_count": db.query(ClinicalOutcome).count(),
        "average_news2": round(float(average_news2), 1) if average_news2 is not None else None,
    }
