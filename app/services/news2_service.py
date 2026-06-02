from sqlalchemy.orm import Session

from app.models import News2Assessment


def list_recent_news2_assessments(db: Session, limit: int = 25) -> list[News2Assessment]:
    return db.query(News2Assessment).order_by(News2Assessment.created_at.desc()).limit(limit).all()
