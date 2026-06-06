from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.rbac import require_permission
from app.services.research_analytics_service import (
    build_analytics_summary,
    build_deterioration_analysis,
    build_group_comparison,
    build_news2_distribution,
    build_outcome_distribution,
    build_response_time_analysis,
)

router = APIRouter(prefix="/api/research/analytics", tags=["research analytics"])


@router.get("/summary")
def read_analytics_summary(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    db.add(AuditLog(action="research_analytics_viewed", entity_type="research_analytics", entity_id="summary"))
    db.commit()
    return build_analytics_summary(db)


@router.get("/news2-distribution")
def read_news2_distribution(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_news2_distribution(db)


@router.get("/outcomes")
def read_outcome_analysis(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_outcome_distribution(db)


@router.get("/response-times")
def read_response_time_analysis(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_response_time_analysis(db)


@router.get("/deterioration")
def read_deterioration_analysis(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_deterioration_analysis(db)


@router.get("/group-comparison")
def read_group_comparison(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:analytics"))):
    return build_group_comparison(db)
