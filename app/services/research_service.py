from sqlalchemy.orm import Session

from app.models import Alert, ClinicalDeteriorationEvent, ClinicalOutcome, DialysisSession, IntradialyticMeasurement, News2Assessment, Patient


def get_research_summary(db: Session) -> dict[str, int]:
    active_alerts = db.query(Alert).filter(Alert.status != "closed").count()
    return {
        "patients": db.query(Patient).count(),
        "dialysis_sessions": db.query(DialysisSession).count(),
        "measurements": db.query(IntradialyticMeasurement).count(),
        "news2_assessments": db.query(News2Assessment).count(),
        "active_alerts": active_alerts,
        "deterioration_events": db.query(ClinicalDeteriorationEvent).count(),
        "outcomes": db.query(ClinicalOutcome).count(),
    }
