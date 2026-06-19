from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.services.research_evaluation_service import (
    build_prediction_by_deterioration_type,
    build_prediction_by_risk_color,
    build_prediction_evaluation_dataset,
    build_prediction_summary,
    build_response_time_prediction_summary,
)


router = APIRouter(prefix="/api/research/evaluation", tags=["research evaluation"])


@router.get("/prediction-dataset")
def read_prediction_dataset(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_prediction_evaluation_dataset(db)


@router.get("/prediction-summary")
def read_prediction_summary(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_prediction_summary(db)


@router.get("/by-risk-color")
def read_prediction_by_risk_color(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_prediction_by_risk_color(db)


@router.get("/by-deterioration-type")
def read_prediction_by_deterioration_type(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_prediction_by_deterioration_type(db)


@router.get("/response-time-summary")
def read_prediction_response_time_summary(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_response_time_prediction_summary(db)
