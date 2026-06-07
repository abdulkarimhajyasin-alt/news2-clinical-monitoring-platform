from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import AlertRead
from app.services.alert_service import (
    AlertNotFoundError,
    acknowledge_alert,
    close_alert,
    get_alert,
    list_alerts,
    start_alert_action,
    view_alert,
)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def read_alerts(
    status_filter: str | None = Query(default=None, alias="status"),
    risk_level: str | None = None,
    severity_level: str | None = None,
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("alerts:view")),
):
    return list_alerts(
        db,
        status=status_filter,
        risk_level=risk_level,
        severity_level=severity_level,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
    )


@router.get("/{alert_id}", response_model=AlertRead)
def read_alert(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("alerts:view"))):
    try:
        return get_alert(db, alert_id)
    except AlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{alert_id}/view", response_model=AlertRead)
def mark_alert_viewed(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("alerts:view"))):
    return _run_alert_action(db, alert_id, view_alert)


@router.post("/{alert_id}/acknowledge", response_model=AlertRead)
def mark_alert_acknowledged(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("alerts:manage"))):
    return _run_alert_action(db, alert_id, acknowledge_alert)


@router.post("/{alert_id}/start", response_model=AlertRead)
def mark_alert_started(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("alerts:manage"))):
    return _run_alert_action(db, alert_id, start_alert_action)


@router.post("/{alert_id}/close", response_model=AlertRead)
def mark_alert_closed(alert_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("alerts:manage"))):
    return _run_alert_action(db, alert_id, close_alert)


def _run_alert_action(db: Session, alert_id: int, action):
    try:
        return action(db, alert_id)
    except AlertNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
