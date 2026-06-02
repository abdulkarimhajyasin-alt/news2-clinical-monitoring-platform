from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_patients_endpoint_shape():
    response = client.get("/api/patients")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert "patient_code" in payload[0]
        assert "dialysis_vintage_months" in payload[0]
        assert "weekly_sessions_count" in payload[0]


def test_dialysis_sessions_endpoint_shape():
    response = client.get("/api/dialysis-sessions")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert "patient_code" in payload[0]
        assert "session_date" in payload[0]
        assert "session_status" in payload[0]


def test_alerts_endpoint_shape():
    response = client.get("/api/alerts")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert "patient_code" in payload[0]
        assert "risk_level" in payload[0]
        assert "severity_level" in payload[0]


def test_research_summary_endpoint_shape():
    response = client.get("/api/research/summary")

    assert response.status_code == 200
    payload = response.json()
    assert "patients_count" in payload
    assert "sessions_count" in payload
    assert "alerts_count" in payload
    assert "outcomes_count" in payload
