from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import DialysisSessionCreate, DialysisSessionRead, DialysisSessionUpdate
from app.services.dialysis_service import (
    DialysisSessionNotFoundError,
    DialysisSessionPatientNotFoundError,
    create_dialysis_session,
    list_dialysis_sessions,
    update_dialysis_session,
)

router = APIRouter(prefix="/api/dialysis-sessions", tags=["dialysis-sessions"])


@router.get("", response_model=list[DialysisSessionRead])
def read_dialysis_sessions(db: Session = Depends(get_db), _current_user=Depends(require_permission("sessions:view"))):
    return list_dialysis_sessions(db)


@router.post("", response_model=DialysisSessionRead, status_code=status.HTTP_201_CREATED)
def create_dialysis_session_record(
    payload: DialysisSessionCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("sessions:create")),
):
    try:
        return create_dialysis_session(db, payload)
    except DialysisSessionPatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{session_id}", response_model=DialysisSessionRead)
def update_dialysis_session_record(
    session_id: int,
    payload: DialysisSessionUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("sessions:update")),
):
    try:
        return update_dialysis_session(db, session_id, payload)
    except DialysisSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
