from sqlalchemy.orm import Session

from app.models import ClinicalOutcome


def list_clinical_outcomes(db: Session, limit: int = 25) -> list[ClinicalOutcome]:
    return db.query(ClinicalOutcome).order_by(ClinicalOutcome.created_at.desc()).limit(limit).all()
