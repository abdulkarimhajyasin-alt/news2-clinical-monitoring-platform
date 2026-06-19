from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import OutcomeValidation72hCreate, OutcomeValidation72hRead, OutcomeValidation72hResult, OutcomeValidation72hUpdate
from app.services.outcome_validation_service import (
    OutcomeValidationDuplicateError,
    OutcomeValidationEligibilityError,
    OutcomeValidationNotFoundError,
    OutcomeValidationTraceabilityError,
    create_outcome_validation,
    get_outcome_validation_for_session,
    list_outcome_validations,
    update_outcome_validation,
)
from app.services.patient_lifecycle_service import PatientLifecycleError


router = APIRouter(prefix="/api/outcome-validations", tags=["outcome-validations"])


@router.get("", response_model=list[OutcomeValidation72hRead])
def read_outcome_validations(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=100, gt=0, le=500),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("outcomes:view")),
):
    return list_outcome_validations(db, patient_id=patient_id, dialysis_session_id=dialysis_session_id, limit=limit)


@router.get("/session/{session_id}")
def read_outcome_validation_for_session(
    session_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("outcomes:view")),
):
    try:
        return get_outcome_validation_for_session(db, session_id)
    except OutcomeValidationTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=OutcomeValidation72hResult, status_code=status.HTTP_201_CREATED)
def create_72h_outcome_validation(
    payload: OutcomeValidation72hCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("outcomes:create")),
):
    try:
        return create_outcome_validation(db, payload)
    except OutcomeValidationDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except OutcomeValidationEligibilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except (OutcomeValidationTraceabilityError, PatientLifecycleError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/{validation_id}", response_model=OutcomeValidation72hResult)
def update_72h_outcome_validation(
    validation_id: int,
    payload: OutcomeValidation72hUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("outcomes:create")),
):
    try:
        return update_outcome_validation(db, validation_id, payload)
    except OutcomeValidationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except OutcomeValidationDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except OutcomeValidationEligibilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except (OutcomeValidationTraceabilityError, PatientLifecycleError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
