from datetime import datetime, timezone
from statistics import mean

from sqlalchemy.orm import Session

from app.models import (
    Alert,
    AuditLog,
    ClinicalDeteriorationEvent,
    ClinicalResponse,
    DialysisSession,
    IntradialyticMeasurement,
    News2Assessment,
    Patient,
    ResponseTracking,
)


class ResponseTrackingError(Exception):
    pass


class ResponseTrackingAlertNotFoundError(ResponseTrackingError):
    pass


class ResponseTrackingNotFoundError(ResponseTrackingError):
    pass


class ResponseTrackingTraceabilityError(ResponseTrackingError):
    pass


def calculate_response_tracking_for_alert(db: Session, alert_id: int) -> dict[str, object]:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise ResponseTrackingAlertNotFoundError("Alert not found")

    assessment = db.get(News2Assessment, alert.news2_assessment_id)
    if assessment is None:
        raise ResponseTrackingTraceabilityError("Alert NEWS2 assessment is missing")

    measurement = db.get(IntradialyticMeasurement, assessment.intradialytic_measurement_id)
    if measurement is None:
        raise ResponseTrackingTraceabilityError("NEWS2 measurement is missing")

    event = db.query(ClinicalDeteriorationEvent).filter(ClinicalDeteriorationEvent.alert_id == alert.id).first()
    response = (
        db.query(ClinicalResponse)
        .filter(ClinicalResponse.alert_id == alert.id)
        .order_by(ClinicalResponse.created_at.desc())
        .first()
    )

    vital_signs_recorded_at = measurement.measurement_time or measurement.created_at
    alert_created_at = alert.created_at
    warnings: list[str] = []

    if vital_signs_recorded_at is None:
        warnings.append("vital_signs_recorded_at is missing")
    if alert_created_at is None:
        warnings.append("alert_created_at is missing")

    clinical_action_at = response.actual_response_start_time if response else None
    values = {
        "alert_id": alert.id,
        "dialysis_session_id": alert.dialysis_session_id,
        "news2_assessment_id": alert.news2_assessment_id,
        "clinical_deterioration_event_id": event.id if event else None,
        "vital_signs_recorded_at": vital_signs_recorded_at,
        "alert_created_at": alert_created_at,
        "alert_viewed_at": alert.viewed_at,
        "actual_response_start_time": response.actual_response_start_time if response else None,
        "clinical_action_at": clinical_action_at,
        "alert_closed_at": alert.closed_at,
        "time_to_alert_minutes": _duration_minutes(vital_signs_recorded_at, alert_created_at, "time_to_alert_minutes", warnings),
        "time_to_view_minutes": _duration_minutes(alert_created_at, alert.viewed_at, "time_to_view_minutes", warnings),
        "time_to_response_minutes": _duration_minutes(
            alert_created_at,
            response.actual_response_start_time if response else None,
            "time_to_response_minutes",
            warnings,
        ),
        "time_to_action_minutes": _duration_minutes(alert_created_at, clinical_action_at, "time_to_action_minutes", warnings),
        "total_response_time_minutes": _duration_minutes(
            vital_signs_recorded_at,
            response.actual_response_start_time if response else None,
            "total_response_time_minutes",
            warnings,
        ),
    }
    return {"values": values, "warnings": warnings, "event": event}


def upsert_response_tracking_for_alert(
    db: Session,
    alert_id: int,
    audit_action: str | None = None,
    commit: bool = True,
    allow_missing_event: bool = False,
) -> dict[str, object] | None:
    calculated = calculate_response_tracking_for_alert(db, alert_id)
    values = calculated["values"]
    warnings = calculated["warnings"]
    event = calculated["event"]
    existing = db.query(ResponseTracking).filter(ResponseTracking.alert_id == alert_id).first()

    if event is None and existing is None:
        if allow_missing_event:
            return None
        raise ResponseTrackingTraceabilityError("Clinical deterioration event is required before response tracking can be persisted")

    tracking_created = existing is None
    tracking = existing or ResponseTracking(alert_id=alert_id)
    if tracking_created:
        db.add(tracking)

    for field, value in values.items():
        if field == "clinical_deterioration_event_id" and value is None:
            continue
        setattr(tracking, field, value)

    db.flush()
    _create_audit_log(
        db,
        action=audit_action or ("response_tracking_created" if tracking_created else "response_tracking_updated"),
        tracking=tracking,
        new_value=f"Response tracking {'created' if tracking_created else 'updated'} for alert {alert_id}",
    )
    if commit:
        db.commit()
        db.refresh(tracking)

    return {
        "tracking": _tracking_to_dict(db, tracking, warnings),
        "tracking_created": tracking_created,
        "warnings": warnings,
        "message": "Response tracking created" if tracking_created else "Response tracking updated",
    }


def get_response_tracking_records(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    alert_id: int | None = None,
    clinical_deterioration_event_id: int | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    query = db.query(ResponseTracking).join(Alert, ResponseTracking.alert_id == Alert.id)
    if patient_id is not None:
        query = query.filter(Alert.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(ResponseTracking.dialysis_session_id == dialysis_session_id)
    if alert_id is not None:
        query = query.filter(ResponseTracking.alert_id == alert_id)
    if clinical_deterioration_event_id is not None:
        query = query.filter(ResponseTracking.clinical_deterioration_event_id == clinical_deterioration_event_id)
    records = query.order_by(ResponseTracking.created_at.desc()).limit(limit).all()
    return [_tracking_to_dict(db, tracking, []) for tracking in records]


def get_response_tracking_record(db: Session, tracking_id: int) -> dict[str, object]:
    tracking = db.get(ResponseTracking, tracking_id)
    if tracking is None:
        raise ResponseTrackingNotFoundError("Response tracking record not found")
    return _tracking_to_dict(db, tracking, [])


def get_response_tracking_summary(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
) -> dict[str, int | float | None]:
    records = get_response_tracking_records(
        db,
        patient_id=patient_id,
        dialysis_session_id=dialysis_session_id,
        limit=10000,
    )
    response_values = _non_null_values(records, "time_to_response_minutes")
    return {
        "records_count": len(records),
        "average_time_to_alert_minutes": _average(records, "time_to_alert_minutes"),
        "average_time_to_view_minutes": _average(records, "time_to_view_minutes"),
        "average_time_to_response_minutes": _average(records, "time_to_response_minutes"),
        "average_time_to_action_minutes": _average(records, "time_to_action_minutes"),
        "average_total_response_time_minutes": _average(records, "total_response_time_minutes"),
        "fastest_response_minutes": min(response_values) if response_values else None,
        "slowest_response_minutes": max(response_values) if response_values else None,
        "alerts_without_response_count": sum(1 for record in records if record["time_to_response_minutes"] is None),
    }


def _tracking_to_dict(db: Session, tracking: ResponseTracking, warnings: list[str]) -> dict[str, object]:
    alert = db.get(Alert, tracking.alert_id)
    patient = db.get(Patient, alert.patient_id) if alert else None
    session = db.get(DialysisSession, tracking.dialysis_session_id)
    assessment = db.get(News2Assessment, tracking.news2_assessment_id)
    event = db.get(ClinicalDeteriorationEvent, tracking.clinical_deterioration_event_id)
    return {
        "id": tracking.id,
        "alert_id": tracking.alert_id,
        "patient_id": alert.patient_id if alert else 0,
        "patient_code": patient.patient_code if patient else None,
        "dialysis_session_id": tracking.dialysis_session_id,
        "session_date": session.session_date if session else None,
        "news2_assessment_id": tracking.news2_assessment_id,
        "news2_total_score": assessment.total_score if assessment else None,
        "risk_level": alert.risk_level if alert else None,
        "clinical_deterioration_event_id": tracking.clinical_deterioration_event_id,
        "deterioration_type": event.deterioration_type if event else None,
        "deterioration_event_created_at": event.created_at if event else None,
        "vital_signs_recorded_at": tracking.vital_signs_recorded_at,
        "alert_created_at": tracking.alert_created_at,
        "alert_viewed_at": tracking.alert_viewed_at,
        "actual_response_start_time": tracking.actual_response_start_time,
        "clinical_action_at": tracking.clinical_action_at,
        "alert_closed_at": tracking.alert_closed_at,
        "time_to_alert_minutes": tracking.time_to_alert_minutes,
        "time_to_view_minutes": tracking.time_to_view_minutes,
        "time_to_response_minutes": tracking.time_to_response_minutes,
        "time_to_action_minutes": tracking.time_to_action_minutes,
        "total_response_time_minutes": tracking.total_response_time_minutes,
        "warnings": warnings,
        "created_at": tracking.created_at,
        "updated_at": tracking.updated_at,
    }


def _duration_minutes(start: datetime | None, end: datetime | None, metric_name: str, warnings: list[str]) -> int | None:
    if start is None or end is None:
        return None
    try:
        start_value = _as_utc_naive(start)
        end_value = _as_utc_naive(end)
        minutes = int((end_value - start_value).total_seconds() // 60)
    except (TypeError, ValueError, OverflowError):
        warnings.append(f"{metric_name} could not be calculated from invalid timestamp values")
        return None
    if minutes < 0:
        warnings.append(f"{metric_name} is negative and was set to null")
        return None
    return minutes


def _as_utc_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _non_null_values(records: list[dict[str, object]], key: str) -> list[int]:
    return [int(record[key]) for record in records if record.get(key) is not None]


def _average(records: list[dict[str, object]], key: str) -> float | None:
    values = _non_null_values(records, key)
    return round(float(mean(values)), 1) if values else None


def _create_audit_log(db: Session, action: str, tracking: ResponseTracking, new_value: str) -> None:
    db.add(
        AuditLog(
            action=action,
            entity_type="response_tracking",
            entity_id=str(tracking.id),
            new_value=new_value,
        )
    )
