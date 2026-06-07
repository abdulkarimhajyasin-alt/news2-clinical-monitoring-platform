from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import DialysisSessionRead
from app.services.dialysis_service import list_dialysis_sessions

router = APIRouter(prefix="/api/dialysis-sessions", tags=["dialysis-sessions"])


@router.get("", response_model=list[DialysisSessionRead])
def read_dialysis_sessions(db: Session = Depends(get_db), _current_user=Depends(require_permission("sessions:view"))):
    return list_dialysis_sessions(db)
