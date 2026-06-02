from sqlalchemy.orm import Session

from app.models import Alert


def list_alerts(db: Session) -> list[Alert]:
    return db.query(Alert).order_by(Alert.created_at.desc()).all()
