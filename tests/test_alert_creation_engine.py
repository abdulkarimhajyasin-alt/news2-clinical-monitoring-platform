from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Alert, AuditLog, DialysisSession, Patient, StudyGroup, StudyPhase, User, UserRole


@pytest.fixture()
def alert_client(tmp_path):
    db_path = tmp_path / "alert_engine.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Alert Nurse",
        email="alert-nurse@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.nurse,
        department="Dialysis Unit",
    )
    patient = Patient(
        patient_code="ALERT-P-1",
        full_name="Alert Test Patient",
        age=57,
        gender="female",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add_all([user, patient])
    db.flush()
    session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 5),
        session_status="active",
        created_by_user_id=user.id,
    )
    db.add(session)
    db.commit()
    ids = {"patient_id": patient.id, "session_id": session.id, "user_id": user.id}
    db.close()

    def override_get_db():
        test_db = TestingSession()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), TestingSession, ids
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def measurement_payload(ids, **overrides):
    payload = {
        "patient_id": ids["patient_id"],
        "dialysis_session_id": ids["session_id"],
        "measurement_time": "2026-06-05T10:30:00Z",
        "measurement_interval_minutes": 30,
        "respiratory_rate": 18,
        "spo2": 96,
        "oxygen_therapy": False,
        "systolic_bp": 125,
        "diastolic_bp": 75,
        "pulse_rate": 88,
        "temperature": 37.2,
        "consciousness_level": "alert",
        "confusion_status": False,
        "spo2_scale": "scale_1",
        "recorded_by_user_id": ids["user_id"],
    }
    payload.update(overrides)
    return payload


def post_measurement(client, ids, **overrides):
    return client.post("/api/monitoring/measurements", json=measurement_payload(ids, **overrides))


def test_news2_below_5_creates_no_alert(alert_client):
    client, TestingSession, ids = alert_client

    response = post_measurement(client, ids)

    assert response.status_code == 201
    assert response.json()["alert"] is None
    db = TestingSession()
    try:
        assert db.query(Alert).count() == 0
    finally:
        db.close()


def test_news2_5_to_6_creates_medium_alert(alert_client):
    client, _, ids = alert_client

    response = post_measurement(client, ids, respiratory_rate=21, spo2=94, systolic_bp=105, pulse_rate=100)

    assert response.status_code == 201
    alert = response.json()["alert"]
    assert alert["alert_created"] is True
    assert alert["risk_level"] == "medium"
    assert alert["severity_level"] == "medium"
    assert alert["priority"] == "normal"


def test_news2_7_or_higher_creates_high_alert(alert_client):
    client, _, ids = alert_client

    response = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2)

    assert response.status_code == 201
    alert = response.json()["alert"]
    assert alert["alert_created"] is True
    assert alert["risk_level"] == "high"
    assert alert["severity_level"] == "high"
    assert alert["priority"] == "urgent"
    assert alert["trigger_reason"] == "NEWS2 >= 7"


def test_single_parameter_trigger_creates_alert(alert_client):
    client, _, ids = alert_client

    response = post_measurement(client, ids, respiratory_rate=8)

    assert response.status_code == 201
    payload = response.json()
    assert payload["news2_assessment"]["total_score"] == 3
    assert payload["news2_assessment"]["single_parameter_trigger"] is True
    assert payload["alert"]["risk_level"] == "medium"
    assert payload["alert"]["trigger_reason"] == "single_parameter_trigger"


def test_duplicate_prevention_reuses_active_alert(alert_client):
    client, TestingSession, ids = alert_client

    first = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2)
    second = post_measurement(client, ids, respiratory_rate=25, spo2=91, oxygen_therapy=True)

    assert first.status_code == 201
    assert second.status_code == 201
    first_alert = first.json()["alert"]
    second_alert = second.json()["alert"]
    assert second_alert["alert_created"] is False
    assert second_alert["reused_existing"] is True
    assert second_alert["alert_id"] == first_alert["alert_id"]
    db = TestingSession()
    try:
        assert db.query(Alert).count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "alert_reused").count() == 1
    finally:
        db.close()


def test_duplicate_prevention_upgrades_existing_alert_severity(alert_client):
    client, TestingSession, ids = alert_client

    medium = post_measurement(client, ids, respiratory_rate=21, spo2=94, systolic_bp=105, pulse_rate=100)
    high = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2)

    assert medium.status_code == 201
    assert high.status_code == 201
    assert high.json()["alert"]["alert_created"] is False
    assert high.json()["alert"]["reused_existing"] is True
    assert high.json()["alert"]["alert_id"] == medium.json()["alert"]["alert_id"]
    assert high.json()["alert"]["risk_level"] == "high"
    assert high.json()["alert"]["priority"] == "urgent"
    db = TestingSession()
    try:
        assert db.query(Alert).count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "alert_updated").count() == 1
    finally:
        db.close()


def test_view_endpoint_updates_status(alert_client):
    client, _, ids = alert_client
    alert_id = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2).json()["alert"]["alert_id"]

    response = client.post(f"/api/alerts/{alert_id}/view")

    assert response.status_code == 200
    assert response.json()["status"] == "viewed"
    assert response.json()["viewed_at"] is not None


def test_acknowledge_endpoint_updates_status(alert_client):
    client, _, ids = alert_client
    alert_id = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2).json()["alert"]["alert_id"]

    response = client.post(f"/api/alerts/{alert_id}/acknowledge")

    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"
    assert response.json()["acknowledged_at"] is not None


def test_start_endpoint_updates_status(alert_client):
    client, _, ids = alert_client
    alert_id = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2).json()["alert"]["alert_id"]

    response = client.post(f"/api/alerts/{alert_id}/start")

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["action_taken_at"] is not None


def test_close_endpoint_updates_status(alert_client):
    client, _, ids = alert_client
    alert_id = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2).json()["alert"]["alert_id"]

    response = client.post(f"/api/alerts/{alert_id}/close")

    assert response.status_code == 200
    assert response.json()["status"] == "closed"
    assert response.json()["closed_at"] is not None


def test_monitoring_workflow_returns_alert_when_required(alert_client):
    client, _, ids = alert_client

    response = post_measurement(client, ids, respiratory_rate=22, spo2=94, systolic_bp=105, pulse_rate=112, temperature=38.2)

    assert response.status_code == 201
    assert response.json()["alert"]["alert_id"] > 0
