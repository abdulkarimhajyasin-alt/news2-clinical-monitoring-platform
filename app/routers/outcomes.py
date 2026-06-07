from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ClinicalOutcomeCreate, ClinicalOutcomeRead, ClinicalOutcomeResult, ClinicalOutcomeSummary
from app.services.outcome_service import (
    OutcomeEventNotFoundError,
    OutcomeNotFoundError,
    OutcomeTraceabilityError,
    create_outcome,
    get_outcome,
    get_outcome_summary,
    get_outcomes,
)

router = APIRouter(prefix="/api/outcomes", tags=["outcomes"])


@router.post("", response_model=ClinicalOutcomeResult, status_code=status.HTTP_201_CREATED)
def create_clinical_outcome(payload: ClinicalOutcomeCreate, db: Session = Depends(get_db), _current_user=Depends(require_permission("outcomes:create"))):
    try:
        return create_outcome(db, payload)
    except OutcomeEventNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except OutcomeTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[ClinicalOutcomeRead])
def read_clinical_outcomes(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    clinical_deterioration_event_id: int | None = Query(default=None, gt=0),
    outcome_type: str | None = None,
    outcome_window_hours: int | None = Query(default=None, ge=24, le=72),
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("outcomes:view")),
):
    return get_outcomes(
        db,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
        clinical_deterioration_event_id=clinical_deterioration_event_id,
        outcome_type=outcome_type,
        outcome_window_hours=outcome_window_hours,
        limit=limit,
    )


@router.get("/summary", response_model=ClinicalOutcomeSummary)
def read_clinical_outcome_summary(db: Session = Depends(get_db), _current_user=Depends(require_permission("outcomes:view"))):
    return get_outcome_summary(db)


@router.get("/{outcome_id}", response_model=ClinicalOutcomeRead)
def read_clinical_outcome(outcome_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("outcomes:view"))):
    try:
        return get_outcome(db, outcome_id)
    except OutcomeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
