from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ClinicalResponseCreate, ClinicalResponseRead, ClinicalResponseResult
from app.services.response_service import (
    ResponseEventLockedError,
    ResponseEventNotFoundError,
    ResponseInvalidTimeError,
    ResponseNotFoundError,
    ResponseTraceabilityError,
    create_clinical_response,
    get_clinical_response,
    get_clinical_responses,
)

router = APIRouter(prefix="/api/responses", tags=["responses"])


@router.post("", response_model=ClinicalResponseResult, status_code=status.HTTP_201_CREATED)
def create_response(payload: ClinicalResponseCreate, db: Session = Depends(get_db), _current_user=Depends(require_permission("responses:create"))):
    try:
        return create_clinical_response(db, payload)
    except ResponseEventNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ResponseEventLockedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ResponseInvalidTimeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ResponseTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[ClinicalResponseRead])
def read_responses(
    clinical_deterioration_event_id: int | None = Query(default=None, gt=0),
    alert_id: int | None = Query(default=None, gt=0),
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    responded_by_user_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("responses:view")),
):
    return get_clinical_responses(
        db,
        clinical_deterioration_event_id=clinical_deterioration_event_id,
        alert_id=alert_id,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
        responded_by_user_id=responded_by_user_id,
        limit=limit,
    )


@router.get("/{response_id}", response_model=ClinicalResponseRead)
def read_response(response_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("responses:view"))):
    try:
        return get_clinical_response(db, response_id)
    except ResponseNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
