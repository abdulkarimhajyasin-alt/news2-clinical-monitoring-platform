from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import StaffTrainingEvaluationCreate, StaffTrainingEvaluationRead, StaffTrainingEvaluationResult, StaffTrainingEvaluationUpdate, StaffTrainingSummary
from app.services.training_evaluation_service import (
    TrainingEvaluationNotFoundError,
    TrainingEvaluationTraceabilityError,
    TrainingEvaluationValidationError,
    build_training_summary,
    create_training_evaluation,
    export_training_csv,
    get_training_evaluation,
    list_training_evaluations,
    update_training_evaluation,
)

router = APIRouter(prefix="/api/training", tags=["training"])


@router.post("/evaluations", response_model=StaffTrainingEvaluationResult, status_code=status.HTTP_201_CREATED)
def create_staff_training_evaluation(
    payload: StaffTrainingEvaluationCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("studies:create")),
):
    try:
        return create_training_evaluation(db, payload)
    except TrainingEvaluationValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except TrainingEvaluationTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/evaluations", response_model=list[StaffTrainingEvaluationRead])
def read_staff_training_evaluations(
    study_id: int | None = None,
    staff_user_id: int | None = None,
    limit: int = 200,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    return list_training_evaluations(db, study_id=study_id, staff_user_id=staff_user_id, limit=min(max(limit, 1), 1000))


@router.get("/evaluations/{evaluation_id}", response_model=StaffTrainingEvaluationRead)
def read_staff_training_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    try:
        return get_training_evaluation(db, evaluation_id)
    except TrainingEvaluationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/evaluations/{evaluation_id}", response_model=StaffTrainingEvaluationResult)
def update_staff_training_evaluation(
    evaluation_id: int,
    payload: StaffTrainingEvaluationUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("studies:update")),
):
    try:
        return update_training_evaluation(db, evaluation_id, payload)
    except TrainingEvaluationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TrainingEvaluationValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except TrainingEvaluationTraceabilityError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/summary", response_model=StaffTrainingSummary)
def read_training_summary(
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    return build_training_summary(db)


@router.get("/export/csv")
def export_training_evaluations_csv(
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    csv_content = export_training_csv(db)
    return Response(
        content="\ufeff" + csv_content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="staff_training_evaluations.csv"'},
    )
