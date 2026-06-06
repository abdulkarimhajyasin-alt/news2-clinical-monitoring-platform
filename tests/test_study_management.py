from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, DialysisSession, IntradialyticMeasurement, News2Assessment, Patient, StudyGroup, StudyPhase


@pytest.fixture()
def study_client(tmp_path):
    db_path = tmp_path / "study_management.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        test_db = TestingSession()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), TestingSession, engine
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_create_study(study_client):
    client, _, _ = study_client
    response = client.post("/api/studies", json=_study_payload())

    assert response.status_code == 200
    payload = response.json()
    assert payload["study_code"] == "NEWS2-HD-013"
    assert payload["study_status"] == "draft"


def test_update_study(study_client):
    client, _, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]

    response = client.put(f"/api/studies/{study_id}", json={"study_status": "active", "target_sample_size": 90})

    assert response.status_code == 200
    assert response.json()["study_status"] == "active"
    assert response.json()["target_sample_size"] == 90


def test_list_studies(study_client):
    client, _, _ = study_client
    client.post("/api/studies", json=_study_payload())

    response = client.get("/api/studies")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_readiness_calculation(study_client):
    client, TestingSession, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]
    _seed_dataset_row(TestingSession())

    response = client.get(f"/api/studies/{study_id}/readiness")

    assert response.status_code == 200
    payload = response.json()
    assert payload["readiness_score"] >= 50
    assert payload["checks"]["dataset_available"] is True
    assert payload["checks"]["analytics_available"] is True


def test_missing_requirement_detection(study_client):
    client, _, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]

    response = client.get(f"/api/studies/{study_id}/readiness")

    assert response.status_code == 200
    payload = response.json()
    assert "dataset_available" in payload["missing_requirements"]
    assert "outcomes_available" in payload["missing_requirements"]


def test_api_endpoint_validation(study_client):
    client, _, _ = study_client
    response = client.post("/api/studies", json={**_study_payload(), "study_design": "unsupported"})

    assert response.status_code == 422


def test_empty_safe_behavior(study_client):
    client, _, _ = study_client
    list_response = client.get("/api/studies")
    missing_response = client.get("/api/studies/999/readiness")

    assert list_response.status_code == 200
    assert list_response.json() == []
    assert missing_response.status_code == 404


def test_dashboard_payload_stability(study_client):
    client, _, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]

    response = client.get(f"/api/studies/{study_id}/readiness")

    dashboard = response.json()["dashboard"]
    expected = {
        "study_title",
        "principal_investigator",
        "study_status",
        "study_design",
        "target_sample_size",
        "current_patients",
        "dataset_rows",
        "analytics_status",
        "export_readiness",
        "readiness_score",
    }
    assert expected.issubset(dashboard.keys())


def test_status_transitions(study_client):
    client, _, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]

    for status in ["active", "paused", "completed", "archived"]:
        response = client.put(f"/api/studies/{study_id}", json={"study_status": status})
        assert response.status_code == 200
        assert response.json()["study_status"] == status


def test_audit_log_creation(study_client):
    client, TestingSession, _ = study_client
    study_id = client.post("/api/studies", json=_study_payload()).json()["id"]
    client.put(f"/api/studies/{study_id}", json={"study_status": "active"})
    client.get(f"/api/studies/{study_id}/readiness")

    db = TestingSession()
    try:
        actions = [row.action for row in db.query(AuditLog).order_by(AuditLog.id).all()]
    finally:
        db.close()
    assert "study_created" in actions
    assert "study_updated" in actions
    assert "study_readiness_viewed" in actions


def _study_payload():
    return {
        "study_code": "news2-hd-013",
        "study_title": "NEWS2 Hemodialysis Protocol Study",
        "study_description": "Research governance protocol for NEWS2 hemodialysis monitoring.",
        "principal_investigator": "Principal Investigator",
        "study_design": "before_after",
        "study_status": "draft",
        "study_group_a_name": "Control",
        "study_group_b_name": "Intervention",
        "baseline_period_start": "2026-01-01",
        "baseline_period_end": "2026-03-31",
        "intervention_period_start": "2026-04-01",
        "intervention_period_end": "2026-12-31",
        "study_start_date": "2026-01-01",
        "study_end_date": "2026-12-31",
        "target_sample_size": 80,
        "inclusion_notes": "Adult hemodialysis sessions.",
        "exclusion_notes": "Incomplete anonymized identifiers.",
        "notes": "Protocol notes.",
    }


def _seed_dataset_row(db):
    patient = Patient(
        patient_code="STUDY-P-1",
        full_name="Study Patient",
        age=61,
        gender="female",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add(patient)
    db.flush()
    session = DialysisSession(patient_id=patient.id, session_date=date(2026, 6, 5), actual_start_time=datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc), session_status="completed")
    db.add(session)
    db.flush()
    measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 5, 8, 30, tzinfo=timezone.utc),
        measurement_interval_minutes=30,
        respiratory_rate=18,
        spo2=97,
        oxygen_therapy=False,
        systolic_bp=136,
        diastolic_bp=76,
        pulse_rate=84,
        temperature=36.7,
        consciousness_level="alert",
        confusion_status="none",
    )
    db.add(measurement)
    db.flush()
    assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=measurement.id,
        respiratory_score=0,
        spo2_score=0,
        oxygen_score=0,
        systolic_bp_score=0,
        pulse_score=0,
        temperature_score=0,
        consciousness_score=0,
        total_score=0,
        risk_level="low",
        alert_required=False,
        trigger_reason="low",
    )
    db.add(assessment)
    db.commit()
    db.close()
