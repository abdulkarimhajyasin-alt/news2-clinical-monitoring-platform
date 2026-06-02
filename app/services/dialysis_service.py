from sqlalchemy.orm import Session

from app.models import DialysisSession, Patient


def list_dialysis_sessions(db: Session) -> list[dict[str, object]]:
    rows = (
        db.query(DialysisSession, Patient.patient_code)
        .join(Patient, DialysisSession.patient_id == Patient.id)
        .order_by(DialysisSession.session_date.desc(), DialysisSession.actual_start_time.desc())
        .all()
    )
    return [
        {
            "id": session.id,
            "patient_id": session.patient_id,
            "patient_code": patient_code,
            "session_date": session.session_date,
            "weekday": session.weekday,
            "actual_start_time": session.actual_start_time,
            "actual_end_time": session.actual_end_time,
            "target_ultrafiltration": session.target_ultrafiltration,
            "session_status": session.session_status,
            "session_duration_minutes": session.session_duration_minutes,
        }
        for session, patient_code in rows
    ]
