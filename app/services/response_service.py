from datetime import datetime, timezone
import json

from sqlalchemy.orm import Session

from app.models import Alert, AlertStatus, AuditLog, ClinicalDeteriorationEvent, ClinicalResponse, DialysisSession, News2Assessment, Patient
from app.schemas import ClinicalResponseCreate


class ResponseWorkflowError(Exception):
    pass


class ResponseEventNotFoundError(ResponseWorkflowError):
    pass


class ResponseNotFoundError(ResponseWorkflowError):
    pass


class ResponseEventLockedError(ResponseWorkflowError):
    pass


class ResponseTraceabilityError(ResponseWorkflowError):
    pass


class ResponseInvalidTimeError(ResponseWorkflowError):
    pass


def create_clinical_response(db: Session, payload: ClinicalResponseCreate) -> dict[str, object]:
    event = db.get(ClinicalDeteriorationEvent, payload.clinical_deterioration_event_id)
    if event is None:
        raise ResponseEventNotFoundError("Clinical deterioration event not found")
    if event.is_locked:
        raise ResponseEventLockedError("Locked deterioration event cannot create response")

    alert = db.get(Alert, event.alert_id)
    if alert is None:
        raise ResponseTraceabilityError("Deterioration event alert is missing")
    delay_minutes = _response_delay_minutes(alert.created_at, payload.actual_response_start_time)
    if delay_minutes is not None and delay_minutes < 0:
        raise ResponseInvalidTimeError("Actual response start time cannot be before digital alert time")

    existing_response = (
        db.query(ClinicalResponse)
        .filter(ClinicalResponse.clinical_deterioration_event_id == event.id)
        .first()
    )
    if existing_response is not None:
        _create_audit_log(
            db,
            action="clinical_response_reused",
            response=existing_response,
            user_id=payload.responded_by_user_id,
            new_value=f"Reused clinical response for deterioration event {event.id}",
        )
        from app.services.response_tracking_service import upsert_response_tracking_for_alert

        upsert_response_tracking_for_alert(db, alert.id, audit_action="response_tracking_updated", commit=False)
        db.commit()
        return {
            "response": _response_to_dict(db, existing_response),
            "response_created": False,
            "message": "Existing clinical response returned for this deterioration event",
        }

    response = ClinicalResponse(
        clinical_deterioration_event_id=event.id,
        alert_id=alert.id,
        digital_alert_time=alert.created_at,
        actual_response_start_time=payload.actual_response_start_time,
        response_delay_minutes=delay_minutes,
        patient_actions=_json_list(payload.patient_actions),
        vascular_access_actions=_json_list(payload.vascular_access_actions),
        responded_by_user_id=payload.responded_by_user_id,
        notes=payload.notes,
    )
    db.add(response)
    db.flush()

    if alert.status not in {AlertStatus.closed, AlertStatus.cancelled}:
        alert.status = AlertStatus.in_progress
        if alert.action_taken_at is None:
            alert.action_taken_at = payload.actual_response_start_time

    _create_audit_log(
        db,
        action="clinical_response_created",
        response=response,
        user_id=payload.responded_by_user_id,
        new_value=f"Created clinical response for deterioration event {event.id}",
    )
    from app.services.response_tracking_service import upsert_response_tracking_for_alert

    upsert_response_tracking_for_alert(db, alert.id, audit_action="response_tracking_updated", commit=False)
    db.commit()
    db.refresh(response)
    return {
        "response": _response_to_dict(db, response),
        "response_created": True,
        "message": "Clinical response created successfully",
    }


def get_clinical_responses(
    db: Session,
    clinical_deterioration_event_id: int | None = None,
    alert_id: int | None = None,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    responded_by_user_id: int | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    query = db.query(ClinicalResponse).join(
        ClinicalDeteriorationEvent,
        ClinicalResponse.clinical_deterioration_event_id == ClinicalDeteriorationEvent.id,
    )
    if clinical_deterioration_event_id is not None:
        query = query.filter(ClinicalResponse.clinical_deterioration_event_id == clinical_deterioration_event_id)
    if alert_id is not None:
        query = query.filter(ClinicalResponse.alert_id == alert_id)
    if patient_id is not None:
        query = query.filter(ClinicalDeteriorationEvent.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(ClinicalDeteriorationEvent.dialysis_session_id == dialysis_session_id)
    if responded_by_user_id is not None:
        query = query.filter(ClinicalResponse.responded_by_user_id == responded_by_user_id)
    responses = query.order_by(ClinicalResponse.created_at.desc()).limit(limit).all()
    return [_response_to_dict(db, response) for response in responses]


def get_clinical_response(db: Session, response_id: int) -> dict[str, object]:
    response = db.get(ClinicalResponse, response_id)
    if response is None:
        raise ResponseNotFoundError("Clinical response not found")
    return _response_to_dict(db, response)


def _response_delay_minutes(alert_time: datetime | None, response_start_time: datetime | None) -> int | None:
    if alert_time is None or response_start_time is None:
        return None
    try:
        start = _as_utc_naive(alert_time)
        response = _as_utc_naive(response_start_time)
        return int((response - start).total_seconds() // 60)
    except (TypeError, ValueError, OverflowError):
        return None


def _as_utc_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _json_list(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False)


def _parse_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def _response_to_dict(db: Session, response: ClinicalResponse) -> dict[str, object]:
    event = db.get(ClinicalDeteriorationEvent, response.clinical_deterioration_event_id)
    alert = db.get(Alert, response.alert_id)
    patient = db.get(Patient, event.patient_id) if event else None
    session = db.get(DialysisSession, event.dialysis_session_id) if event else None
    assessment = db.get(News2Assessment, event.news2_assessment_id) if event else None
    return {
        "id": response.id,
        "clinical_deterioration_event_id": response.clinical_deterioration_event_id,
        "alert_id": response.alert_id,
        "patient_id": event.patient_id if event else 0,
        "patient_code": patient.patient_code if patient else None,
        "dialysis_session_id": event.dialysis_session_id if event else 0,
        "session_date": session.session_date if session else None,
        "news2_total_score": assessment.total_score if assessment else None,
        "deterioration_type": event.deterioration_type if event else None,
        "digital_alert_time": response.digital_alert_time or (alert.created_at if alert else None),
        "actual_response_start_time": response.actual_response_start_time,
        "response_delay_minutes": response.response_delay_minutes,
        "patient_actions": _parse_json_list(response.patient_actions),
        "vascular_access_actions": _parse_json_list(response.vascular_access_actions),
        "responded_by_user_id": response.responded_by_user_id,
        "notes": response.notes,
        "is_locked": response.is_locked,
        "locked_at": response.locked_at,
        "locked_by_user_id": response.locked_by_user_id,
        "created_at": response.created_at,
        "updated_at": response.updated_at,
    }


def _create_audit_log(
    db: Session,
    action: str,
    response: ClinicalResponse,
    new_value: str,
    user_id: int | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="clinical_response",
            entity_id=str(response.id),
            new_value=new_value,
        )
    )
