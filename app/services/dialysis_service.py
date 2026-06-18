from sqlalchemy.orm import Session

from app.models import DialysisSession, Patient
from app.schemas import DialysisSessionCreate, DialysisSessionUpdate


class DialysisSessionError(ValueError):
    pass


class DialysisSessionNotFoundError(DialysisSessionError):
    pass


class DialysisSessionPatientNotFoundError(DialysisSessionError):
    pass


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
            "session_day_of_week": session.weekday,
            "actual_start_time": session.actual_start_time,
            "actual_end_time": session.actual_end_time,
            "target_ultrafiltration": session.target_ultrafiltration,
            "target_fluid_removal_ml": session.target_fluid_removal_ml,
            "session_status": session.session_status,
            "session_duration_minutes": session.session_duration_minutes,
        }
        for session, patient_code in rows
    ]


def create_dialysis_session(db: Session, payload: DialysisSessionCreate) -> dict[str, object]:
    patient = db.get(Patient, payload.patient_id)
    if patient is None or patient.status == "deleted":
        raise DialysisSessionPatientNotFoundError("Patient not found")
    values = _session_model_values(payload.model_dump())
    session = DialysisSession(**values)
    db.add(session)
    db.commit()
    db.refresh(session)
    return _session_to_dict(session, patient.patient_code)


def update_dialysis_session(db: Session, session_id: int, payload: DialysisSessionUpdate) -> dict[str, object]:
    session = db.get(DialysisSession, session_id)
    if session is None:
        raise DialysisSessionNotFoundError("Dialysis session not found")
    values = _session_model_values(payload.model_dump(exclude_unset=True))
    for field, value in values.items():
        setattr(session, field, value)
    db.commit()
    db.refresh(session)
    patient = db.get(Patient, session.patient_id)
    return _session_to_dict(session, patient.patient_code if patient else None)


def _session_model_values(values: dict[str, object]) -> dict[str, object]:
    values = dict(values)
    values.pop("session_day_of_week", None)
    if not values.get("weekday") and values.get("session_date"):
        values["weekday"] = values["session_date"].strftime("%A")
    return values


def _session_to_dict(session: DialysisSession, patient_code: str | None = None) -> dict[str, object]:
    return {
        "id": session.id,
        "patient_id": session.patient_id,
        "patient_code": patient_code,
        "session_date": session.session_date,
        "weekday": session.weekday,
        "session_day_of_week": session.weekday,
        "actual_start_time": session.actual_start_time,
        "actual_end_time": session.actual_end_time,
        "target_ultrafiltration": session.target_ultrafiltration,
        "target_fluid_removal_ml": session.target_fluid_removal_ml,
        "session_status": session.session_status,
        "session_duration_minutes": session.session_duration_minutes,
    }
