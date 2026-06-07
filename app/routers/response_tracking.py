from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ResponseTrackingRead, ResponseTrackingResult, ResponseTrackingSummary
from app.services.response_tracking_service import (
    ResponseTrackingAlertNotFoundError,
    ResponseTrackingNotFoundError,
    ResponseTrackingTraceabilityError,
    get_response_tracking_record,
    get_response_tracking_records,
    get_response_tracking_summary,
    upsert_response_tracking_for_alert,
)

router = APIRouter(prefix="/api/response-tracking", tags=["response-tracking"])


@router.get("/summary", response_model=ResponseTrackingSummary)
def read_response_tracking_summary(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("responses:view")),
):
    return get_response_tracking_summary(db, patient_id=patient_id, dialysis_session_id=dialysis_session_id)


@router.post("/recalculate/{alert_id}", response_model=ResponseTrackingResult)
def recalculate_response_tracking(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("responses:create"))):
    try:
        return upsert_response_tracking_for_alert(
            db,
            alert_id,
            audit_action="response_tracking_recalculated",
            commit=True,
        )
    except ResponseTrackingAlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ResponseTrackingTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[ResponseTrackingRead])
def read_response_tracking_records(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    alert_id: int | None = Query(default=None, gt=0),
    clinical_deterioration_event_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("responses:view")),
):
    return get_response_tracking_records(
        db,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
        alert_id=alert_id,
        clinical_deterioration_event_id=clinical_deterioration_event_id,
        limit=limit,
    )


@router.get("/{tracking_id}", response_model=ResponseTrackingRead)
def read_response_tracking_record(tracking_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("responses:view"))):
    try:
        return get_response_tracking_record(db, tracking_id)
    except ResponseTrackingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
