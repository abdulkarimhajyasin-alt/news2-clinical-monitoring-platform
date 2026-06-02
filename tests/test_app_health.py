from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_reports_database_connected():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "news2-hemodialysis-monitoring"
    assert payload["database"] == "connected"


def test_frontend_root_serves_html():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "NEWS2 Hemodialysis Monitoring" in response.text
