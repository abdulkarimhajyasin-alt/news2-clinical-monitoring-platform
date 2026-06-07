from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ClinicalDeteriorationEventCreate, ClinicalDeteriorationEventRead, ClinicalDeteriorationEventResult
from app.services.deterioration_service import (
    DeteriorationAlertClosedError,
    DeteriorationAlertNotFoundError,
    DeteriorationEventNotFoundError,
    DeteriorationTraceabilityError,
    create_deterioration_event_from_alert,
    get_deterioration_event,
    get_deterioration_events,
)

router = APIRouter(prefix="/api/deterioration", tags=["deterioration"])


@router.post("/events", response_model=ClinicalDeteriorationEventResult, status_code=status.HTTP_201_CREATED)
def create_deterioration_event(payload: ClinicalDeteriorationEventCreate, db: Session = Depends(get_db), _current_user=Depends(require_permission("deterioration:create"))):
    try:
        return create_deterioration_event_from_alert(db, payload)
    except DeteriorationAlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DeteriorationAlertClosedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DeteriorationTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/events", response_model=list[ClinicalDeteriorationEventRead])
def read_deterioration_events(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    alert_id: int | None = Query(default=None, gt=0),
    deterioration_type: str | None = None,
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("deterioration:view")),
):
    return get_deterioration_events(
        db,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
        alert_id=alert_id,
        deterioration_type=deterioration_type,
        limit=limit,
    )


@router.get("/events/{event_id}", response_model=ClinicalDeteriorationEventRead)
def read_deterioration_event(event_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("deterioration:view"))):
    try:
        return get_deterioration_event(db, event_id)
    except DeteriorationEventNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
