from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import PatientCreate, PatientCreateResult, PatientRead
from app.services.patient_service import PatientCodeExistsError, create_patient, list_patients

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
def read_patients(db: Session = Depends(get_db), _current_user=Depends(require_permission("patients:view"))):
    return list_patients(db)


@router.post("", response_model=PatientCreateResult, status_code=status.HTTP_201_CREATED)
def create_patient_record(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("patients:create")),
):
    try:
        patient = create_patient(db, payload)
    except PatientCodeExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"patient": patient, "patient_created": True, "message": "patient_created"}
