from sqlalchemy.orm import Session

from app.models import Patient
from app.schemas import PatientCreate


class PatientCodeExistsError(ValueError):
    pass


def list_patients(
    db: Session,
    *,
    status: str | None = None,
    include_archived: bool = False,
    include_deleted: bool = False,
) -> list[Patient]:
    query = db.query(Patient)
    if status:
        query = query.filter(Patient.status == status)
    else:
        allowed_statuses = ["active"]
        if include_archived:
            allowed_statuses.extend(["discharged", "archived"])
        if include_deleted:
            allowed_statuses.append("deleted")
        query = query.filter(Patient.status.in_(allowed_statuses))
    if not include_deleted:
        query = query.filter(Patient.status != "deleted")
    return query.order_by(Patient.patient_code).all()


def create_patient(db: Session, payload: PatientCreate) -> Patient:
    existing = db.query(Patient).filter(Patient.patient_code == payload.patient_code).first()
    if existing:
        raise PatientCodeExistsError("patient_code already exists")

    values = payload.model_dump()
    values["study_phase"] = values.get("study_phase") or "post_implementation"
    values["study_group"] = values.get("study_group") or "intervention"
    values["is_anonymized"] = True if values.get("is_anonymized") is None else values["is_anonymized"]
    patient = Patient(**values)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
