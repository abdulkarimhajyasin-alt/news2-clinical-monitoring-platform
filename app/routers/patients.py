from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PatientRead
from app.services.patient_service import list_patients

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
def read_patients(db: Session = Depends(get_db)):
    return list_patients(db)
