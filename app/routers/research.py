from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ResearchSummary
from app.services.research_service import get_research_summary

router = APIRouter(prefix="/api/research", tags=["research"])


@router.get("/summary", response_model=ResearchSummary)
def read_research_summary(db: Session = Depends(get_db), _current_user=Depends(require_permission("research:view"))):
    return get_research_summary(db)
