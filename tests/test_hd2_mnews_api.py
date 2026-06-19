from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def hd2_payload(**overrides):
    payload = {
        "respiratory_rate": 18,
        "oxygen_saturation": 96,
        "temperature": 37.0,
        "systolic_bp": 125,
        "heart_rate": 80,
        "consciousness_level": "alert",
        "vascular_access_status": "normal",
        "pre_dialysis_weight": 71.0,
        "dry_weight": 70.0,
        "session_duration_hours": 4.0,
        "fluid_to_remove": 1000.0,
        "potassium": 4.5,
        "sbp_symptomatic_hypotension": False,
    }
    payload.update(overrides)
    return payload


def test_hd2_mnews_calculate_returns_full_breakdown():
    response = client.post("/api/hd2-mnews/calculate", json=hd2_payload())

    assert response.status_code == 200
    payload = response.json()
    assert payload["hd2_mnews_total_score"] == 0
    assert payload["hd2_mnews_risk_color"] == "green"
    assert payload["hd2_mnews_risk_label_ar"] == "أخضر / آمن"
    assert payload["idwg_percent"] == 1.43
    assert payload["ufr"] == 3.57
    assert payload["vascular_access_score"] == 0
    assert payload["nursing_protocol"]["risk_color"] == "green"
    assert payload["nursing_protocol"]["reassessment_interval_minutes_min"] == 60
    assert payload["protocol_actions_ar"]


def test_hd2_mnews_endpoint_automatic_red_for_spo2():
    response = client.post("/api/hd2-mnews/calculate", json=hd2_payload(oxygen_saturation=91))

    assert response.status_code == 200
    payload = response.json()
    assert payload["hd2_mnews_risk_color"] == "red"
    assert payload["hd2_mnews_critical_trigger"] is True
    assert payload["nursing_protocol"]["requires_physician_call"] is True
    assert payload["required_response_time_label_ar"] is not None
    assert "SpO2 ≤91%" in payload["hd2_mnews_critical_reasons"]


def test_hd2_mnews_endpoint_yellow_protocol_is_stable():
    response = client.post(
        "/api/hd2-mnews/calculate",
        json=hd2_payload(respiratory_rate=22, oxygen_saturation=94, systolic_bp=105, heart_rate=100, potassium=5.3),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["hd2_mnews_risk_color"] == "yellow"
    assert payload["nursing_protocol"]["reassessment_interval_minutes_min"] == 15
    assert payload["nursing_protocol"]["reassessment_interval_minutes_max"] == 30


def test_existing_standard_news2_endpoint_still_works():
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
    assert response.json()["total_score"] == 1
