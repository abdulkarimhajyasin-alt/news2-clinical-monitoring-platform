from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import ResearchStudyCreate, ResearchStudyRead, ResearchStudyUpdate, StudyReadinessReport
from app.services.study_management_service import (
    build_study_readiness_report,
    create_study,
    get_study,
    list_studies,
    update_study,
)

router = APIRouter(prefix="/api/studies", tags=["studies"])


@router.post("", response_model=ResearchStudyRead)
def create_research_study(payload: ResearchStudyCreate, db: Session = Depends(get_db), _current_user=Depends(require_permission("studies:create"))):
    return create_study(db, payload)


@router.get("", response_model=list[ResearchStudyRead])
def read_research_studies(db: Session = Depends(get_db), _current_user=Depends(require_permission("studies:view"))):
    return list_studies(db)


@router.get("/{study_id}", response_model=ResearchStudyRead)
def read_research_study(study_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("studies:view"))):
    return get_study(db, study_id)


@router.put("/{study_id}", response_model=ResearchStudyRead)
def update_research_study(study_id: int, payload: ResearchStudyUpdate, db: Session = Depends(get_db), _current_user=Depends(require_permission("studies:update"))):
    return update_study(db, study_id, payload)


@router.get("/{study_id}/readiness", response_model=StudyReadinessReport)
def read_study_readiness(study_id: int, db: Session = Depends(get_db), _current_user=Depends(require_permission("studies:view"))):
    return build_study_readiness_report(db, study_id)
