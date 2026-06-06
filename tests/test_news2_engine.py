import pytest

from app.schemas import NEWS2CalculationRequest
from app.services.news2_service import (
    calculate_news2,
    score_consciousness,
    score_oxygen_therapy,
    score_pulse_rate,
    score_respiratory_rate,
    score_spo2_scale_1,
    score_systolic_bp,
    score_temperature,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(8, 3), (9, 1), (11, 1), (12, 0), (20, 0), (21, 2), (24, 2), (25, 3)],
)
def test_respiratory_rate_boundaries(value, expected):
    assert score_respiratory_rate(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(91, 3), (92, 2), (93, 2), (94, 1), (95, 1), (96, 0)],
)
def test_spo2_scale_1_boundaries(value, expected):
    assert score_spo2_scale_1(value) == expected


@pytest.mark.parametrize(("value", "expected"), [(True, 2), (False, 0)])
def test_oxygen_therapy_score(value, expected):
    assert score_oxygen_therapy(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(90, 3), (91, 2), (100, 2), (101, 1), (110, 1), (111, 0), (219, 0), (220, 3)],
)
def test_systolic_bp_boundaries(value, expected):
    assert score_systolic_bp(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(40, 3), (41, 1), (50, 1), (51, 0), (90, 0), (91, 1), (110, 1), (111, 2), (130, 2), (131, 3)],
)
def test_pulse_rate_boundaries(value, expected):
    assert score_pulse_rate(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(35.0, 3), (35.1, 1), (36.0, 1), (36.1, 0), (38.0, 0), (38.1, 1), (39.0, 1), (39.1, 2)],
)
def test_temperature_boundaries(value, expected):
    assert score_temperature(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("alert", 0), ("voice", 3), ("pain", 3), ("unresponsive", 3), ("new_confusion", 3)],
)
def test_consciousness_scores(value, expected):
    assert score_consciousness(value) == expected


def make_request(**overrides):
    payload = {
        "respiratory_rate": 18,
        "spo2": 96,
        "oxygen_therapy": False,
        "systolic_bp": 125,
        "pulse_rate": 88,
        "temperature": 37.2,
        "consciousness_level": "alert",
    }
    payload.update(overrides)
    return NEWS2CalculationRequest(**payload)


@pytest.mark.parametrize(
    ("calculation_request", "risk_level", "alert_required"),
    [
        (make_request(), "low", False),
        (make_request(spo2=93, oxygen_therapy=True, pulse_rate=100), "medium", True),
        (make_request(respiratory_rate=25, spo2=91, oxygen_therapy=True), "high", True),
    ],
)
def test_total_score_risk_classifications(calculation_request, risk_level, alert_required):
    result = calculate_news2(calculation_request)

    assert result.risk_level == risk_level
    assert result.alert_required is alert_required


def test_single_parameter_trigger_below_total_alert_threshold():
    result = calculate_news2(make_request(respiratory_rate=8))

    assert result.total_score == 3
    assert result.risk_level == "low"
    assert result.alert_required is False
    assert result.single_parameter_trigger is True
    assert result.trigger_reason == "Single parameter scored 3"


def test_spo2_scale_2_uses_explicit_placeholder_path():
    result = calculate_news2(make_request(spo2=95, spo2_scale="scale_2"))

    assert result.spo2_score == 1
