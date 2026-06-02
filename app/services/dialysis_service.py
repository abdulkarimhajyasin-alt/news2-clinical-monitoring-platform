from sqlalchemy.orm import Session

from app.models import DialysisSession


def list_dialysis_sessions(db: Session) -> list[DialysisSession]:
    return db.query(DialysisSession).order_by(DialysisSession.session_date.desc()).all()
