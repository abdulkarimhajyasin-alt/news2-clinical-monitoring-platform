from fastapi import APIRouter

from app.schemas import HD2MNEWSCalculationRequest, HD2MNEWSCalculationResult
from app.services.hd2_mnews_service import calculate_hd2_mnews

router = APIRouter(prefix="/api/hd2-mnews", tags=["hd2-mnews"])


@router.post("/calculate", response_model=HD2MNEWSCalculationResult)
def calculate_hd2_mnews_endpoint(request: HD2MNEWSCalculationRequest) -> HD2MNEWSCalculationResult:
    return calculate_hd2_mnews(request)
