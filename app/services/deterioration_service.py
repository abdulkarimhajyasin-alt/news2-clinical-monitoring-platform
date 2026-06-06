from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import (
    Alert,
    AlertStatus,
    AuditLog,
    ClinicalDeteriorationEvent,
    DialysisSession,
    News2Assessment,
    Patient,
)
from app.schemas import ClinicalDeteriorationEventCreate


class DeteriorationWorkflowError(Exception):
    pass


class DeteriorationAlertNotFoundError(DeteriorationWorkflowError):
    pass


class DeteriorationEventNotFoundError(DeteriorationWorkflowError):
    pass


class DeteriorationAlertClosedError(DeteriorationWorkflowError):
    pass


class DeteriorationTraceabilityError(DeteriorationWorkflowError):
    pass


def create_deterioration_event_from_alert(db: Session, payload: ClinicalDeteriorationEventCreate) -> dict[str, object]:
    alert = db.get(Alert, payload.alert_id)
    if alert is None:
        raise DeteriorationAlertNotFoundError("Alert not found")

    if alert.status in {AlertStatus.closed, AlertStatus.cancelled}:
        raise DeteriorationAlertClosedError("Closed or cancelled alert cannot create deterioration event")

    existing_event = db.query(ClinicalDeteriorationEvent).filter(ClinicalDeteriorationEvent.alert_id == alert.id).first()
    if existing_event is not None:
        _create_audit_log(
            db,
            action="clinical_deterioration_event_reused",
            event=existing_event,
            user_id=payload.created_by_user_id,
            new_value=f"Reused deterioration event for alert {alert.id}",
        )
        from app.services.response_tracking_service import upsert_response_tracking_for_alert

        upsert_response_tracking_for_alert(db, alert.id, audit_action="response_tracking_updated", commit=False)
        db.commit()
        return {
            "event": _event_to_dict(db, existing_event),
            "event_created": False,
            "message": "Existing clinical deterioration event returned for this alert",
        }

    patient = db.get(Patient, alert.patient_id)
    session = db.get(DialysisSession, alert.dialysis_session_id)
    assessment = db.get(News2Assessment, alert.news2_assessment_id)
    if patient is None or session is None or assessment is None:
        raise DeteriorationTraceabilityError("Alert traceability chain is incomplete")

    event = ClinicalDeteriorationEvent(
        patient_id=alert.patient_id,
        dialysis_session_id=alert.dialysis_session_id,
        news2_assessment_id=alert.news2_assessment_id,
        alert_id=alert.id,
        deterioration_time=payload.deterioration_time,
        time_from_session_start_minutes=_time_from_session_start_minutes(session.actual_start_time, payload.deterioration_time),
        deterioration_type=payload.deterioration_type,
        triggering_news2_score=assessment.total_score,
        description=payload.description,
    )
    db.add(event)
    db.flush()

    if alert.status in {AlertStatus.new, AlertStatus.viewed, AlertStatus.acknowledged}:
        alert.status = AlertStatus.in_progress
        alert.action_taken_at = datetime.now(timezone.utc).replace(microsecond=0)

    _create_audit_log(
        db,
        action="clinical_deterioration_event_created",
        event=event,
        user_id=payload.created_by_user_id,
        new_value=f"Created deterioration event from alert {alert.id}",
    )
    from app.services.response_tracking_service import upsert_response_tracking_for_alert

    upsert_response_tracking_for_alert(db, alert.id, audit_action="response_tracking_created", commit=False)
    db.commit()
    db.refresh(event)
    return {
        "event": _event_to_dict(db, event),
        "event_created": True,
        "message": "Clinical deterioration event created successfully",
    }


def get_deterioration_events(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    alert_id: int | None = None,
    deterioration_type: str | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    query = db.query(ClinicalDeteriorationEvent)
    if patient_id is not None:
        query = query.filter(ClinicalDeteriorationEvent.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(ClinicalDeteriorationEvent.dialysis_session_id == dialysis_session_id)
    if alert_id is not None:
        query = query.filter(ClinicalDeteriorationEvent.alert_id == alert_id)
    if deterioration_type is not None:
        query = query.filter(ClinicalDeteriorationEvent.deterioration_type == deterioration_type)
    events = query.order_by(ClinicalDeteriorationEvent.created_at.desc()).limit(limit).all()
    return [_event_to_dict(db, event) for event in events]


def get_deterioration_event(db: Session, event_id: int) -> dict[str, object]:
    event = db.get(ClinicalDeteriorationEvent, event_id)
    if event is None:
        raise DeteriorationEventNotFoundError("Clinical deterioration event not found")
    return _event_to_dict(db, event)


def _time_from_session_start_minutes(session_start: datetime | None, deterioration_time: datetime) -> int | None:
    if session_start is None:
        return None
    try:
        start = _as_utc_naive(session_start)
        event_time = _as_utc_naive(deterioration_time)
        return int((event_time - start).total_seconds() // 60)
    except (TypeError, ValueError, OverflowError):
        return None


def _as_utc_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _event_to_dict(db: Session, event: ClinicalDeteriorationEvent) -> dict[str, object]:
    patient = db.get(Patient, event.patient_id)
    session = db.get(DialysisSession, event.dialysis_session_id)
    assessment = db.get(News2Assessment, event.news2_assessment_id)
    alert = db.get(Alert, event.alert_id)
    return {
        "id": event.id,
        "patient_id": event.patient_id,
        "patient_code": patient.patient_code if patient else None,
        "dialysis_session_id": event.dialysis_session_id,
        "session_date": session.session_date if session else None,
        "news2_assessment_id": event.news2_assessment_id,
        "news2_total_score": assessment.total_score if assessment else event.triggering_news2_score,
        "alert_id": event.alert_id,
        "alert_status": alert.status if alert else "unknown",
        "risk_level": alert.risk_level if alert else None,
        "deterioration_time": event.deterioration_time,
        "time_from_session_start_minutes": event.time_from_session_start_minutes,
        "deterioration_type": event.deterioration_type,
        "triggering_news2_score": event.triggering_news2_score,
        "description": event.description,
        "is_locked": event.is_locked,
        "locked_at": event.locked_at,
        "locked_by_user_id": event.locked_by_user_id,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
    }


def _create_audit_log(
    db: Session,
    action: str,
    event: ClinicalDeteriorationEvent,
    new_value: str,
    user_id: int | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="clinical_deterioration_event",
            entity_id=str(event.id),
            new_value=new_value,
        )
    )
