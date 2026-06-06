from sqlalchemy.orm import Session

from app.models import DialysisSession, IntradialyticMeasurement, News2Assessment, Patient
from app.schemas import MonitoringMeasurementCreate, NEWS2CalculationRequest
from app.services.alert_service import create_alert_from_news2_assessment
from app.services.news2_service import calculate_news2


class MonitoringWorkflowError(Exception):
    pass


class PatientNotFoundError(MonitoringWorkflowError):
    pass


class DialysisSessionNotFoundError(MonitoringWorkflowError):
    pass


class SessionPatientMismatchError(MonitoringWorkflowError):
    pass


def list_recent_measurements(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    limit: int = 25,
) -> list[IntradialyticMeasurement]:
    query = db.query(IntradialyticMeasurement)
    if patient_id is not None:
        query = query.filter(IntradialyticMeasurement.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(IntradialyticMeasurement.dialysis_session_id == dialysis_session_id)
    return query.order_by(IntradialyticMeasurement.measurement_time.desc()).limit(limit).all()


def create_measurement_with_news2(db: Session, payload: MonitoringMeasurementCreate) -> dict[str, object]:
    patient = db.get(Patient, payload.patient_id)
    if patient is None:
        raise PatientNotFoundError("Patient not found")

    session = db.get(DialysisSession, payload.dialysis_session_id)
    if session is None:
        raise DialysisSessionNotFoundError("Dialysis session not found")

    if session.patient_id != payload.patient_id:
        raise SessionPatientMismatchError("Dialysis session does not belong to patient")

    try:
        confusion_status = _normalize_confusion_status(payload.confusion_status)
        calculation_consciousness = (
            "new_confusion"
            if confusion_status == "new_confusion"
            else payload.consciousness_level
        )

        measurement = IntradialyticMeasurement(
            patient_id=payload.patient_id,
            dialysis_session_id=payload.dialysis_session_id,
            measurement_time=payload.measurement_time,
            measurement_interval_minutes=payload.measurement_interval_minutes,
            respiratory_rate=payload.respiratory_rate,
            spo2=payload.spo2,
            oxygen_therapy=payload.oxygen_therapy,
            systolic_bp=payload.systolic_bp,
            diastolic_bp=payload.diastolic_bp,
            pulse_rate=payload.pulse_rate,
            temperature=payload.temperature,
            consciousness_level=payload.consciousness_level,
            confusion_status=confusion_status,
            recorded_by_user_id=payload.recorded_by_user_id,
        )
        db.add(measurement)
        db.flush()

        news2_result = calculate_news2(
            NEWS2CalculationRequest(
                respiratory_rate=payload.respiratory_rate,
                spo2=payload.spo2,
                oxygen_therapy=payload.oxygen_therapy,
                systolic_bp=payload.systolic_bp,
                pulse_rate=payload.pulse_rate,
                temperature=payload.temperature,
                consciousness_level=calculation_consciousness,
                spo2_scale=payload.spo2_scale,
            )
        )

        assessment = News2Assessment(
            patient_id=payload.patient_id,
            dialysis_session_id=payload.dialysis_session_id,
            intradialytic_measurement_id=measurement.id,
            respiratory_score=news2_result.respiratory_score,
            spo2_score=news2_result.spo2_score,
            oxygen_score=news2_result.oxygen_score,
            systolic_bp_score=news2_result.systolic_bp_score,
            pulse_score=news2_result.pulse_score,
            temperature_score=news2_result.temperature_score,
            consciousness_score=news2_result.consciousness_score,
            total_score=news2_result.total_score,
            risk_level=news2_result.risk_level,
            alert_required=news2_result.alert_required,
            trigger_reason=news2_result.trigger_reason,
            created_by_user_id=payload.recorded_by_user_id,
        )
        db.add(assessment)
        db.flush()
        alert_result = create_alert_from_news2_assessment(
            db,
            assessment,
            single_parameter_trigger=news2_result.single_parameter_trigger,
            created_by_user_id=payload.recorded_by_user_id,
        )
        db.commit()
        db.refresh(measurement)
        db.refresh(assessment)

        return {
            "measurement": measurement,
            "news2_assessment": _assessment_to_response(assessment, news2_result.single_parameter_trigger),
            "alert": alert_result,
            "message": "Measurement saved, NEWS2 calculated, and alert rules evaluated successfully",
        }
    except Exception:
        db.rollback()
        raise


def _normalize_confusion_status(value: bool | str | None) -> str:
    if value is True:
        return "new_confusion"
    if value is False or value is None:
        return "none"

    normalized = value.strip().lower()
    if normalized in {"true", "yes", "new_confusion", "present"}:
        return "new_confusion"
    if normalized in {"false", "no", "none", "absent"}:
        return "none"
    return normalized


def _assessment_to_response(assessment: News2Assessment, single_parameter_trigger: bool | None = None) -> dict[str, object]:
    component_scores = [
        assessment.respiratory_score,
        assessment.spo2_score,
        assessment.oxygen_score,
        assessment.systolic_bp_score,
        assessment.pulse_score,
        assessment.temperature_score,
        assessment.consciousness_score,
    ]
    return {
        "id": assessment.id,
        "patient_id": assessment.patient_id,
        "dialysis_session_id": assessment.dialysis_session_id,
        "intradialytic_measurement_id": assessment.intradialytic_measurement_id,
        "respiratory_score": assessment.respiratory_score,
        "spo2_score": assessment.spo2_score,
        "oxygen_score": assessment.oxygen_score,
        "systolic_bp_score": assessment.systolic_bp_score,
        "pulse_score": assessment.pulse_score,
        "temperature_score": assessment.temperature_score,
        "consciousness_score": assessment.consciousness_score,
        "total_score": assessment.total_score,
        "risk_level": assessment.risk_level,
        "alert_required": assessment.alert_required,
        "single_parameter_trigger": single_parameter_trigger if single_parameter_trigger is not None else any(score == 3 for score in component_scores),
        "trigger_reason": assessment.trigger_reason,
        "created_by_user_id": assessment.created_by_user_id,
        "created_at": assessment.created_at,
    }
