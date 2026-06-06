from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import MonitoringMeasurementCreate, MonitoringMeasurementRead, MonitoringMeasurementResult
from app.services.monitoring_service import (
    DialysisSessionNotFoundError,
    PatientNotFoundError,
    SessionPatientMismatchError,
    create_measurement_with_news2,
    list_recent_measurements,
)

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/measurements", response_model=list[MonitoringMeasurementRead])
def read_monitoring_measurements(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
):
    return list_recent_measurements(db, patient_id=patient_id, dialysis_session_id=dialysis_session_id, limit=limit)


@router.post("/measurements", response_model=MonitoringMeasurementResult, status_code=status.HTTP_201_CREATED)
def create_monitoring_measurement(payload: MonitoringMeasurementCreate, db: Session = Depends(get_db), _current_user=Depends(require_permission("measurements:create"))):
    try:
        return create_measurement_with_news2(db, payload)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DialysisSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except SessionPatientMismatchError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
