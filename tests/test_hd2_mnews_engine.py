import pytest

from app.schemas import HD2MNEWSCalculationRequest
from app.services.hd2_mnews_service import calculate_hd2_mnews


def make_request(**overrides):
    payload = {
        "respiratory_rate": 18,
        "oxygen_saturation": 96,
        "temperature": 37.0,
        "systolic_bp": 125,
        "heart_rate": 80,
        "consciousness_level": "alert",
        "vascular_access_status": "normal",
        "pre_dialysis_weight": 72.0,
        "dry_weight": 70.0,
        "session_duration_hours": 4.0,
        "fluid_to_remove": 2.0,
        "potassium": 4.5,
        "sbp_symptomatic_hypotension": False,
    }
    payload.update(overrides)
    return HD2MNEWSCalculationRequest(**payload)


def test_normal_values_are_green_with_zero_score():
    result = calculate_hd2_mnews(make_request(pre_dialysis_weight=71.0, fluid_to_remove=1.0))

    assert result.hd2_mnews_total_score == 0
    assert result.hd2_mnews_risk_color == "green"
    assert result.hd2_mnews_risk_label_ar == "أخضر / آمن"
    assert result.hd2_mnews_critical_trigger is False


def test_score_five_to_six_is_yellow():
    result = calculate_hd2_mnews(make_request(respiratory_rate=22, oxygen_saturation=94, systolic_bp=105, heart_rate=100, potassium=5.3))

    assert result.hd2_mnews_total_score == 5
    assert result.hd2_mnews_risk_color == "yellow"


def test_total_score_seven_or_more_is_red():
    result = calculate_hd2_mnews(
        make_request(respiratory_rate=25, temperature=39.2, systolic_bp=100, heart_rate=111, vascular_access_status="disturbed")
    )

    assert result.hd2_mnews_total_score == 10
    assert result.hd2_mnews_risk_color == "red"
    assert result.hd2_mnews_critical_trigger is False


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"oxygen_saturation": 91}, "SpO2 ≤91%"),
        ({"consciousness_level": "unresponsive"}, "AVPU unresponsive"),
        ({"systolic_bp": 88, "sbp_symptomatic_hypotension": True}, "Symptomatic hypotension with SBP ≤90"),
        ({"potassium": 6.2}, "Potassium critical range"),
        ({"vascular_access_status": "critical"}, "Critical vascular access status"),
    ],
)
def test_critical_variables_force_automatic_red(overrides, reason):
    result = calculate_hd2_mnews(make_request(**overrides))

    assert result.hd2_mnews_risk_color == "red"
    assert result.hd2_mnews_risk_label_ar == "أحمر تلقائي"
    assert result.hd2_mnews_critical_trigger is True
    assert reason in result.hd2_mnews_critical_reasons


def test_idwg_formula_and_score_are_calculated():
    result = calculate_hd2_mnews(make_request(pre_dialysis_weight=74.2, dry_weight=70.0))

    assert result.idwg_percent == 6.0
    assert result.idwg_score == 2


def test_ufr_formula_and_score_are_calculated():
    result = calculate_hd2_mnews(make_request(fluid_to_remove=4.0, dry_weight=70.0, session_duration_hours=4.0))

    assert result.ufr == 0.01
    assert result.ufr_score == 0


def test_ufr_uses_same_units_as_doctor_form_formula():
    result = calculate_hd2_mnews(make_request(fluid_to_remove=4000.0, dry_weight=70.0, session_duration_hours=4.0))

    assert result.ufr == 14.29
    assert result.ufr_score == 2
