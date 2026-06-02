from sqlalchemy.orm import Session

from app.models import Alert, Patient


def list_alerts(db: Session) -> list[dict[str, object]]:
    rows = (
        db.query(Alert, Patient.patient_code)
        .join(Patient, Alert.patient_id == Patient.id)
        .order_by(Alert.created_at.desc())
        .all()
    )
    return [
        {
            "id": alert.id,
            "patient_id": alert.patient_id,
            "patient_code": patient_code,
            "dialysis_session_id": alert.dialysis_session_id,
            "risk_level": alert.risk_level,
            "severity_level": alert.severity_level,
            "status": alert.status,
            "priority": alert.priority,
            "trigger_reason": alert.trigger_reason,
            "created_at": alert.created_at,
        }
        for alert, patient_code in rows
    ]
