from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import Alert, AlertStatus, AuditLog, News2Assessment, Patient
from app.schemas import AlertCreationResult


ACTIVE_ALERT_STATUSES = {
    AlertStatus.new,
    AlertStatus.viewed,
    AlertStatus.acknowledged,
    AlertStatus.in_progress,
}


class AlertNotFoundError(Exception):
    pass


def create_alert_from_news2_assessment(
    db: Session,
    assessment: News2Assessment,
    single_parameter_trigger: bool = False,
    created_by_user_id: int | None = None,
) -> AlertCreationResult | None:
    alert_rule = _evaluate_alert_rule(assessment, single_parameter_trigger)
    if alert_rule is None:
        return None

    existing_alert = _find_active_alert(
        db,
        patient_id=assessment.patient_id,
        dialysis_session_id=assessment.dialysis_session_id,
    )
    if existing_alert is not None:
        upgraded = _upgrade_existing_alert_if_needed(existing_alert, alert_rule)
        _create_audit_log(
            db,
            action="alert_updated" if upgraded else "alert_reused",
            alert=existing_alert,
            user_id=created_by_user_id,
            new_value=(
                f"Updated active alert severity for NEWS2 assessment {assessment.id}"
                if upgraded
                else f"Reused active alert for NEWS2 assessment {assessment.id}"
            ),
        )
        _refresh_response_tracking_if_safe(db, existing_alert.id)
        return _alert_creation_result(existing_alert, alert_created=False, reused_existing=True)

    alert = Alert(
        patient_id=assessment.patient_id,
        dialysis_session_id=assessment.dialysis_session_id,
        news2_assessment_id=assessment.id,
        risk_level=alert_rule["risk_level"],
        severity_level=alert_rule["severity_level"],
        status=AlertStatus.new,
        priority=alert_rule["priority"],
        trigger_reason=alert_rule["trigger_reason"],
    )
    db.add(alert)
    db.flush()
    _create_audit_log(
        db,
        action="alert_created",
        alert=alert,
        user_id=created_by_user_id,
        new_value=f"Created alert from NEWS2 assessment {assessment.id}",
    )
    _refresh_response_tracking_if_safe(db, alert.id)
    return _alert_creation_result(alert, alert_created=True, reused_existing=False)


def list_alerts(
    db: Session,
    status: str | None = None,
    risk_level: str | None = None,
    severity_level: str | None = None,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
) -> list[dict[str, object]]:
    query = db.query(Alert, Patient.patient_code).join(Patient, Alert.patient_id == Patient.id)
    if status is not None:
        query = query.filter(Alert.status == status)
    if risk_level is not None:
        query = query.filter(Alert.risk_level == risk_level)
    if severity_level is not None:
        query = query.filter(Alert.severity_level == severity_level)
    if patient_id is not None:
        query = query.filter(Alert.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(Alert.dialysis_session_id == dialysis_session_id)
    rows = (
        query
        .order_by(Alert.created_at.desc())
        .all()
    )
    return [_alert_to_dict(alert, patient_code) for alert, patient_code in rows]


def get_alert(db: Session, alert_id: int) -> dict[str, object]:
    row = (
        db.query(Alert, Patient.patient_code)
        .join(Patient, Alert.patient_id == Patient.id)
        .filter(Alert.id == alert_id)
        .first()
    )
    if row is None:
        raise AlertNotFoundError("Alert not found")
    alert, patient_code = row
    return _alert_to_dict(alert, patient_code)


def view_alert(db: Session, alert_id: int) -> dict[str, object]:
    return _transition_alert(db, alert_id, status=AlertStatus.viewed, timestamp_field="viewed_at", action="alert_viewed")


def acknowledge_alert(db: Session, alert_id: int) -> dict[str, object]:
    return _transition_alert(db, alert_id, status=AlertStatus.acknowledged, timestamp_field="acknowledged_at", action="alert_acknowledged")


def start_alert_action(db: Session, alert_id: int) -> dict[str, object]:
    return _transition_alert(db, alert_id, status=AlertStatus.in_progress, timestamp_field="action_taken_at", action="alert_started")


def close_alert(db: Session, alert_id: int) -> dict[str, object]:
    return _transition_alert(db, alert_id, status=AlertStatus.closed, timestamp_field="closed_at", action="alert_closed")


def _evaluate_alert_rule(assessment: News2Assessment, single_parameter_trigger: bool) -> dict[str, str] | None:
    if assessment.hd2_mnews_risk_color == "red":
        return {
            "risk_level": "high",
            "severity_level": "high",
            "priority": "immediate" if assessment.hd2_mnews_critical_trigger else "urgent",
            "trigger_reason": "HD2-mNEWS automatic red" if assessment.hd2_mnews_critical_trigger else "HD2-mNEWS >= 7",
        }
    if assessment.total_score >= 7:
        return {
            "risk_level": "high",
            "severity_level": "high",
            "priority": "urgent",
            "trigger_reason": "NEWS2 >= 7",
        }
    if assessment.total_score >= 5:
        return {
            "risk_level": "medium",
            "severity_level": "medium",
            "priority": "normal",
            "trigger_reason": "NEWS2 5-6",
        }
    if single_parameter_trigger:
        return {
            "risk_level": "medium",
            "severity_level": "medium",
            "priority": "normal",
            "trigger_reason": "single_parameter_trigger",
        }
    return None


def _find_active_alert(db: Session, patient_id: int, dialysis_session_id: int) -> Alert | None:
    return (
        db.query(Alert)
        .filter(
            Alert.patient_id == patient_id,
            Alert.dialysis_session_id == dialysis_session_id,
            Alert.status.in_([status.value for status in ACTIVE_ALERT_STATUSES]),
        )
        .order_by(Alert.created_at.desc())
        .first()
    )


def _upgrade_existing_alert_if_needed(alert: Alert, alert_rule: dict[str, str]) -> bool:
    severity_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    priority_rank = {"normal": 1, "urgent": 2, "immediate": 3}
    upgraded = False

    if severity_rank.get(alert_rule["severity_level"], 0) > severity_rank.get(alert.severity_level, 0):
        alert.risk_level = alert_rule["risk_level"]
        alert.severity_level = alert_rule["severity_level"]
        upgraded = True

    if priority_rank.get(alert_rule["priority"], 0) > priority_rank.get(alert.priority, 0):
        alert.priority = alert_rule["priority"]
        upgraded = True

    if upgraded:
        alert.trigger_reason = alert_rule["trigger_reason"]
    return upgraded


def _transition_alert(db: Session, alert_id: int, status: str, timestamp_field: str, action: str) -> dict[str, object]:
    row = (
        db.query(Alert, Patient.patient_code)
        .join(Patient, Alert.patient_id == Patient.id)
        .filter(Alert.id == alert_id)
        .first()
    )
    if row is None:
        raise AlertNotFoundError("Alert not found")

    alert, patient_code = row
    now = datetime.now(timezone.utc).replace(microsecond=0)
    alert.status = status
    setattr(alert, timestamp_field, now)
    _create_audit_log(
        db,
        action=action,
        alert=alert,
        new_value=f"Alert status set to {status}",
    )
    _refresh_response_tracking_if_safe(db, alert.id)
    db.commit()
    db.refresh(alert)
    return _alert_to_dict(alert, patient_code)


def _alert_creation_result(alert: Alert, alert_created: bool, reused_existing: bool) -> AlertCreationResult:
    return AlertCreationResult(
        alert_created=alert_created,
        alert_id=alert.id,
        reused_existing=reused_existing,
        status=alert.status,
        risk_level=alert.risk_level,
        severity_level=alert.severity_level,
        priority=alert.priority,
        trigger_reason=alert.trigger_reason,
    )


def _alert_to_dict(alert: Alert, patient_code: str | None = None) -> dict[str, object]:
    return {
        "id": alert.id,
        "patient_id": alert.patient_id,
        "patient_code": patient_code,
        "dialysis_session_id": alert.dialysis_session_id,
        "news2_assessment_id": alert.news2_assessment_id,
        "risk_level": alert.risk_level,
        "severity_level": alert.severity_level,
        "status": alert.status,
        "priority": alert.priority,
        "trigger_reason": alert.trigger_reason,
        "created_at": alert.created_at,
        "viewed_at": alert.viewed_at,
        "acknowledged_at": alert.acknowledged_at,
        "action_taken_at": alert.action_taken_at,
        "closed_at": alert.closed_at,
    }


def _create_audit_log(db: Session, action: str, alert: Alert, new_value: str, user_id: int | None = None) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="alert",
            entity_id=str(alert.id),
            new_value=new_value,
        )
    )


def _refresh_response_tracking_if_safe(db: Session, alert_id: int) -> None:
    from app.services.response_tracking_service import ResponseTrackingError, upsert_response_tracking_for_alert

    try:
        upsert_response_tracking_for_alert(db, alert_id, audit_action="response_tracking_updated", commit=False, allow_missing_event=True)
    except ResponseTrackingError:
        return
