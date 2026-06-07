from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import NEWS2AssessmentRead, NEWS2CalculationRequest, NEWS2CalculationResult
from app.services.news2_service import calculate_news2, list_news2_assessments

router = APIRouter(prefix="/api/news2", tags=["news2"])


@router.post("/calculate", response_model=NEWS2CalculationResult)
def calculate_news2_endpoint(request: NEWS2CalculationRequest) -> NEWS2CalculationResult:
    return calculate_news2(request)


@router.get("/assessments", response_model=list[NEWS2AssessmentRead])
def read_news2_assessments(
    patient_id: int | None = Query(default=None, gt=0),
    dialysis_session_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=25, gt=0, le=200),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("news2:view")),
):
    return list_news2_assessments(db, patient_id=patient_id, dialysis_session_id=dialysis_session_id, limit=limit)
