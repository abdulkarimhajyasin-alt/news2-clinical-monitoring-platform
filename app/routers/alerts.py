from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AlertRead
from app.services.alert_service import list_alerts

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def read_alerts(db: Session = Depends(get_db)):
    return list_alerts(db)
