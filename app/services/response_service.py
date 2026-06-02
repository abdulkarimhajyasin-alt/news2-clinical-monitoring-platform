from sqlalchemy.orm import Session

from app.models import ClinicalResponse


def list_clinical_responses(db: Session, limit: int = 25) -> list[ClinicalResponse]:
    return db.query(ClinicalResponse).order_by(ClinicalResponse.created_at.desc()).limit(limit).all()
