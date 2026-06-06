from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_news2_calculate_valid_request_returns_expected_score():
    response = client.post(
        "/api/news2/calculate",
        json={
            "respiratory_rate": 18,
            "spo2": 95,
            "oxygen_therapy": False,
            "systolic_bp": 125,
            "pulse_rate": 88,
            "temperature": 37.2,
            "consciousness_level": "alert",
            "spo2_scale": "scale_1",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["spo2_score"] == 1
    assert payload["total_score"] == 1
    assert payload["risk_level"] == "low"
    assert payload["alert_required"] is False


def test_news2_calculate_invalid_vitals_return_422():
    response = client.post(
        "/api/news2/calculate",
        json={
            "respiratory_rate": 0,
            "spo2": 101,
            "oxygen_therapy": False,
            "systolic_bp": 125,
            "pulse_rate": 88,
            "temperature": 37.2,
            "consciousness_level": "alert",
        },
    )

    assert response.status_code == 422


def test_news2_calculate_high_score_requires_alert():
    response = client.post(
        "/api/news2/calculate",
        json={
            "respiratory_rate": 25,
            "spo2": 91,
            "oxygen_therapy": True,
            "systolic_bp": 90,
            "pulse_rate": 131,
            "temperature": 39.1,
            "consciousness_level": "new_confusion",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_score"] == 19
    assert payload["risk_level"] == "high"
    assert payload["alert_required"] is True
    assert payload["single_parameter_trigger"] is True
