from sqlalchemy.orm import Session

from app.models import News2Assessment
from app.schemas import NEWS2CalculationRequest, NEWS2CalculationResult


def list_recent_news2_assessments(db: Session, limit: int = 25) -> list[News2Assessment]:
    return db.query(News2Assessment).order_by(News2Assessment.created_at.desc()).limit(limit).all()


def list_news2_assessments(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    query = db.query(News2Assessment)
    if patient_id is not None:
        query = query.filter(News2Assessment.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(News2Assessment.dialysis_session_id == dialysis_session_id)
    rows = query.order_by(News2Assessment.created_at.desc()).limit(limit).all()
    return [_assessment_to_response(row) for row in rows]


ALLOWED_CONSCIOUSNESS_LEVELS = {"alert", "voice", "pain", "unresponsive", "new_confusion"}
ALLOWED_SPO2_SCALES = {"scale_1", "scale_2"}
SPO2_SCALE_2_CLINICAL_REVIEW_REQUIRED = True

TRIGGER_BELOW_THRESHOLD = "NEWS2 total score below alert threshold"
TRIGGER_ALERT_REQUIRED = "NEWS2 total score requires clinical alert"
TRIGGER_SINGLE_PARAMETER = "Single parameter scored 3"


def score_respiratory_rate(respiratory_rate: int) -> int:
    if respiratory_rate <= 8:
        return 3
    if respiratory_rate <= 11:
        return 1
    if respiratory_rate <= 20:
        return 0
    if respiratory_rate <= 24:
        return 2
    return 3


def score_spo2(spo2: int, spo2_scale: str = "scale_1") -> int:
    if spo2_scale == "scale_2":
        return score_spo2_scale_2(spo2)
    return score_spo2_scale_1(spo2)


def score_spo2_scale_1(spo2: int) -> int:
    if spo2 <= 91:
        return 3
    if spo2 <= 93:
        return 2
    if spo2 <= 95:
        return 1
    return 0


def score_spo2_scale_2(spo2: int) -> int:
    """Conservative placeholder path pending local clinical approval."""
    return score_spo2_scale_1(spo2)


def score_oxygen_therapy(oxygen_therapy: bool) -> int:
    return 2 if oxygen_therapy else 0


def score_systolic_bp(systolic_bp: int) -> int:
    if systolic_bp <= 90:
        return 3
    if systolic_bp <= 100:
        return 2
    if systolic_bp <= 110:
        return 1
    if systolic_bp <= 219:
        return 0
    return 3


def score_pulse_rate(pulse_rate: int) -> int:
    if pulse_rate <= 40:
        return 3
    if pulse_rate <= 50:
        return 1
    if pulse_rate <= 90:
        return 0
    if pulse_rate <= 110:
        return 1
    if pulse_rate <= 130:
        return 2
    return 3


def score_temperature(temperature: float) -> int:
    if temperature <= 35.0:
        return 3
    if temperature <= 36.0:
        return 1
    if temperature <= 38.0:
        return 0
    if temperature <= 39.0:
        return 1
    return 2


def score_consciousness(consciousness_level: str) -> int:
    return 0 if consciousness_level == "alert" else 3


def classify_risk(total_score: int) -> str:
    if total_score >= 7:
        return "high"
    if total_score >= 5:
        return "medium"
    return "low"


def calculate_news2(request: NEWS2CalculationRequest) -> NEWS2CalculationResult:
    respiratory_score = score_respiratory_rate(request.respiratory_rate)
    spo2_score = score_spo2(request.spo2, request.spo2_scale)
    oxygen_score = score_oxygen_therapy(request.oxygen_therapy)
    systolic_bp_score = score_systolic_bp(request.systolic_bp)
    pulse_score = score_pulse_rate(request.pulse_rate)
    temperature_score = score_temperature(request.temperature)
    consciousness_score = score_consciousness(request.consciousness_level)

    component_scores = [
        respiratory_score,
        spo2_score,
        oxygen_score,
        systolic_bp_score,
        pulse_score,
        temperature_score,
        consciousness_score,
    ]
    total_score = sum(component_scores)
    alert_required = total_score >= 5
    single_parameter_trigger = any(score == 3 for score in component_scores)

    if single_parameter_trigger:
        trigger_reason = TRIGGER_SINGLE_PARAMETER
    elif alert_required:
        trigger_reason = TRIGGER_ALERT_REQUIRED
    else:
        trigger_reason = TRIGGER_BELOW_THRESHOLD

    return NEWS2CalculationResult(
        respiratory_score=respiratory_score,
        spo2_score=spo2_score,
        oxygen_score=oxygen_score,
        systolic_bp_score=systolic_bp_score,
        pulse_score=pulse_score,
        temperature_score=temperature_score,
        consciousness_score=consciousness_score,
        total_score=total_score,
        risk_level=classify_risk(total_score),
        alert_required=alert_required,
        single_parameter_trigger=single_parameter_trigger,
        trigger_reason=trigger_reason,
    )


def _assessment_to_response(assessment: News2Assessment) -> dict[str, object]:
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
        "single_parameter_trigger": any(score == 3 for score in component_scores),
        "trigger_reason": assessment.trigger_reason,
        "created_by_user_id": assessment.created_by_user_id,
        "created_at": assessment.created_at,
    }
