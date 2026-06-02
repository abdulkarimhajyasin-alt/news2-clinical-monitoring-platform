from sqlalchemy.orm import Session

from app.models import IntradialyticMeasurement


def list_recent_measurements(db: Session, limit: int = 25) -> list[IntradialyticMeasurement]:
    return db.query(IntradialyticMeasurement).order_by(IntradialyticMeasurement.measurement_time.desc()).limit(limit).all()
