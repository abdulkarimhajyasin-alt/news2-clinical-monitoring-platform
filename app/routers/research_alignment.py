from fastapi import APIRouter, Depends

from app.rbac import require_permission
from app.schemas import AlignmentAuditResponse
from app.services.research_alignment_service import build_alignment_audit

router = APIRouter(prefix="/api/research", tags=["research alignment"])


@router.get("/alignment-audit", response_model=AlignmentAuditResponse)
def read_alignment_audit(_current_user=Depends(require_permission("research:view"))):
    return build_alignment_audit()
