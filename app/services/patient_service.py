from sqlalchemy.orm import Session

from app.models import Patient


def list_patients(db: Session) -> list[Patient]:
    return db.query(Patient).order_by(Patient.patient_code).all()
