from __future__ import annotations

import json
from datetime import datetime, time, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import AuditLog, DialysisSession, OutcomeValidation72h, Patient
from app.schemas import OutcomeValidation72hCreate, OutcomeValidation72hUpdate
from app.services.patient_lifecycle_service import ensure_patient_is_active


class OutcomeValidationError(Exception):
    pass


class OutcomeValidationNotFoundError(OutcomeValidationError):
    pass


class OutcomeValidationDuplicateError(OutcomeValidationError):
    pass


class OutcomeValidationEligibilityError(OutcomeValidationError):
    pass


class OutcomeValidationTraceabilityError(OutcomeValidationError):
    pass


def list_outcome_validations(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    limit: int = 100,
) -> list[dict[str, object]]:
    query = db.query(OutcomeValidation72h)
    if patient_id is not None:
        query = query.filter(OutcomeValidation72h.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(OutcomeValidation72h.dialysis_session_id == dialysis_session_id)
    validations = query.order_by(OutcomeValidation72h.completed_at.desc()).limit(limit).all()
    return [_validation_to_dict(db, validation) for validation in validations]


def get_outcome_validation_for_session(db: Session, session_id: int) -> dict[str, object]:
    validation = db.query(OutcomeValidation72h).filter(OutcomeValidation72h.dialysis_session_id == session_id).first()
    if validation is None:
        session = db.get(DialysisSession, session_id)
        if session is None:
            raise OutcomeValidationTraceabilityError("Dialysis session not found")
        eligibility = build_session_eligibility(session)
        return {
            "dialysis_session_id": session_id,
            "eligible_for_completion": eligibility["eligible_for_completion"],
            "eligibility_time": eligibility["eligibility_time"],
            "remaining_minutes": eligibility["remaining_minutes"],
            "message": eligibility["message"],
        }
    return _validation_to_dict(db, validation)


def create_outcome_validation(db: Session, payload: OutcomeValidation72hCreate) -> dict[str, object]:
    patient, session = _validate_patient_session(db, payload.patient_id, payload.dialysis_session_id)
    ensure_patient_is_active(patient)
    _ensure_eligible(session)
    existing = db.query(OutcomeValidation72h).filter(OutcomeValidation72h.dialysis_session_id == payload.dialysis_session_id).first()
    if existing is not None:
        raise OutcomeValidationDuplicateError("Outcome validation already exists for this dialysis session")

    validation = _payload_to_model(payload)
    validation.completed_at = datetime.now(timezone.utc).replace(microsecond=0)
    db.add(validation)
    db.flush()
    _create_audit_log(db, "outcome_validation_72h_created", validation, payload.completed_by_user_id)
    db.commit()
    db.refresh(validation)
    return {
        "validation": _validation_to_dict(db, validation),
        "validation_created": True,
        "message": "72-hour outcome validation created successfully",
    }


def update_outcome_validation(db: Session, validation_id: int, payload: OutcomeValidation72hUpdate) -> dict[str, object]:
    validation = db.get(OutcomeValidation72h, validation_id)
    if validation is None:
        raise OutcomeValidationNotFoundError("Outcome validation not found")
    patient, session = _validate_patient_session(db, payload.patient_id, payload.dialysis_session_id)
    ensure_patient_is_active(patient)
    _ensure_eligible(session)
    duplicate = (
        db.query(OutcomeValidation72h)
        .filter(OutcomeValidation72h.dialysis_session_id == payload.dialysis_session_id, OutcomeValidation72h.id != validation_id)
        .first()
    )
    if duplicate is not None:
        raise OutcomeValidationDuplicateError("Outcome validation already exists for this dialysis session")

    updated = _payload_to_model(payload, validation)
    updated.completed_at = datetime.now(timezone.utc).replace(microsecond=0)
    _create_audit_log(db, "outcome_validation_72h_updated", updated, payload.completed_by_user_id)
    db.commit()
    db.refresh(updated)
    return {
        "validation": _validation_to_dict(db, updated),
        "validation_created": False,
        "message": "72-hour outcome validation updated successfully",
    }


def build_session_eligibility(session: DialysisSession, now: datetime | None = None) -> dict[str, object]:
    now = now or datetime.now(timezone.utc)
    reference = _session_reference_time(session)
    eligibility_time = reference + timedelta(hours=72) if reference else None
    eligible = eligibility_time is not None and _as_aware(now) >= _as_aware(eligibility_time)
    remaining_minutes = None
    if eligibility_time and not eligible:
        remaining_minutes = max(0, int((_as_aware(eligibility_time) - _as_aware(now)).total_seconds() // 60))
    message = (
        "Outcome validation is available"
        if eligible
        else "ظ„ط§ ظٹظ…ظƒظ† طھظˆط«ظٹظ‚ ط§ظ„ظ†طھظٹط¬ط© ط§ظ„ط³ط±ظٹط±ظٹط© ظ‚ط¨ظ„ ظ…ط±ظˆط± 72 ط³ط§ط¹ط© ط¹ظ„ظ‰ ط§ظ„ط¬ظ„ط³ط©."
    )
    return {
        "eligible_for_completion": eligible,
        "eligibility_time": eligibility_time,
        "remaining_minutes": remaining_minutes,
        "message": message,
    }


def _validate_patient_session(db: Session, patient_id: int, session_id: int) -> tuple[Patient, DialysisSession]:
    patient = db.get(Patient, patient_id)
    session = db.get(DialysisSession, session_id)
    if patient is None or session is None:
        raise OutcomeValidationTraceabilityError("Patient or dialysis session not found")
    if session.patient_id != patient_id:
        raise OutcomeValidationTraceabilityError("Dialysis session does not belong to patient")
    return patient, session


def _ensure_eligible(session: DialysisSession) -> None:
    eligibility = build_session_eligibility(session)
    if not eligibility["eligible_for_completion"]:
        raise OutcomeValidationEligibilityError(str(eligibility["message"]))


def _payload_to_model(payload: OutcomeValidation72hCreate | OutcomeValidation72hUpdate, validation: OutcomeValidation72h | None = None) -> OutcomeValidation72h:
    validation = validation or OutcomeValidation72h()
    validation.patient_id = payload.patient_id
    validation.dialysis_session_id = payload.dialysis_session_id
    validation.deterioration_occurred = payload.deterioration_occurred
    validation.deterioration_types = json.dumps(payload.deterioration_types, ensure_ascii=False)
    validation.type_specific_details = json.dumps(payload.type_specific_details.model_dump(mode="json"), ensure_ascii=False)
    validation.deterioration_timing_category = payload.deterioration_timing_category
    validation.deterioration_time = payload.deterioration_time.isoformat() if isinstance(payload.deterioration_time, time) else None
    validation.deterioration_datetime = payload.deterioration_datetime
    validation.platform_prediction_status = payload.platform_prediction_status
    validation.interventions = json.dumps(payload.interventions, ensure_ascii=False)
    validation.doctor_response_time_minutes = payload.doctor_response_time_minutes
    validation.final_result = payload.final_result
    validation.verification_sources = json.dumps(payload.verification_sources, ensure_ascii=False)
    validation.notes = payload.notes
    validation.completed_by_user_id = payload.completed_by_user_id
    return validation


def _validation_to_dict(db: Session, validation: OutcomeValidation72h) -> dict[str, object]:
    patient = db.get(Patient, validation.patient_id)
    session = db.get(DialysisSession, validation.dialysis_session_id)
    eligibility = build_session_eligibility(session) if session else {}
    return {
        "id": validation.id,
        "patient_id": validation.patient_id,
        "patient_code": patient.patient_code if patient else None,
        "dialysis_session_id": validation.dialysis_session_id,
        "session_date": session.session_date if session else None,
        "deterioration_occurred": validation.deterioration_occurred,
        "deterioration_types": _json_list(validation.deterioration_types),
        "type_specific_details": _json_dict(validation.type_specific_details) or {},
        "deterioration_timing_category": validation.deterioration_timing_category,
        "deterioration_time": validation.deterioration_time,
        "deterioration_datetime": validation.deterioration_datetime,
        "platform_prediction_status": validation.platform_prediction_status,
        "interventions": _json_list(validation.interventions),
        "doctor_response_time_minutes": validation.doctor_response_time_minutes,
        "final_result": validation.final_result,
        "verification_sources": _json_list(validation.verification_sources),
        "notes": validation.notes,
        "completed_by_user_id": validation.completed_by_user_id,
        "completed_at": validation.completed_at,
        "created_at": validation.created_at,
        "updated_at": validation.updated_at,
        "eligible_for_completion": bool(eligibility.get("eligible_for_completion", False)),
        "eligibility_time": eligibility.get("eligibility_time"),
        "remaining_minutes": eligibility.get("remaining_minutes"),
    }


def _session_reference_time(session: DialysisSession) -> datetime | None:
    if session.actual_end_time:
        return session.actual_end_time
    if session.actual_start_time and session.session_duration_minutes:
        return session.actual_start_time + timedelta(minutes=session.session_duration_minutes)
    if session.actual_start_time:
        return session.actual_start_time
    if session.session_date:
        return datetime.combine(session.session_date, time.min, tzinfo=timezone.utc)
    return None


def _as_aware(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def _json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        return []
    return loaded if isinstance(loaded, list) else []


def _json_dict(value: str | None) -> dict[str, object] | None:
    if not value:
        return None
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None


def _create_audit_log(db: Session, action: str, validation: OutcomeValidation72h, user_id: int | None = None) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="outcome_validation_72h",
            entity_id=str(validation.id),
            new_value=f"72-hour outcome validation for session {validation.dialysis_session_id}",
        )
    )
