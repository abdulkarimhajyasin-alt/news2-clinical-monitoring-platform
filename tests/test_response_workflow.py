from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import (
    Alert,
    AlertStatus,
    AuditLog,
    ClinicalDeteriorationEvent,
    ClinicalResponse,
    DialysisSession,
    IntradialyticMeasurement,
    News2Assessment,
    Patient,
    StudyGroup,
    StudyPhase,
    User,
    UserRole,
)


@pytest.fixture()
def response_client(tmp_path):
    db_path = tmp_path / "response_workflow.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Response Doctor",
        email="response-doctor@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.doctor,
        department="Nephrology",
    )
    patient = Patient(
        patient_code="RESP-P-1",
        full_name="Response Patient",
        age=63,
        gender="female",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add_all([user, patient])
    db.flush()
    session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 5),
        actual_start_time=datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc),
        session_status="active",
        created_by_user_id=user.id,
    )
    db.add(session)
    db.flush()
    measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 5, 9, 15, tzinfo=timezone.utc),
        measurement_interval_minutes=30,
        respiratory_rate=24,
        spo2=91,
        oxygen_therapy=True,
        systolic_bp=92,
        diastolic_bp=58,
        pulse_rate=112,
        temperature=37.9,
        consciousness_level="alert",
        confusion_status="new_confusion",
        recorded_by_user_id=user.id,
    )
    db.add(measurement)
    db.flush()
    assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=measurement.id,
        respiratory_score=2,
        spo2_score=3,
        oxygen_score=2,
        systolic_bp_score=3,
        pulse_score=2,
        temperature_score=0,
        consciousness_score=3,
        total_score=15,
        risk_level="high",
        alert_required=True,
        trigger_reason="NEWS2 >= 7",
        created_by_user_id=user.id,
    )
    db.add(assessment)
    db.flush()
    locked_measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 5, 9, 18, tzinfo=timezone.utc),
        measurement_interval_minutes=30,
        respiratory_rate=25,
        spo2=90,
        oxygen_therapy=True,
        systolic_bp=90,
        diastolic_bp=55,
        pulse_rate=120,
        temperature=38.1,
        consciousness_level="alert",
        confusion_status="none",
        recorded_by_user_id=user.id,
    )
    db.add(locked_measurement)
    db.flush()
    locked_assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=locked_measurement.id,
        respiratory_score=3,
        spo2_score=3,
        oxygen_score=2,
        systolic_bp_score=3,
        pulse_score=2,
        temperature_score=1,
        consciousness_score=0,
        total_score=14,
        risk_level="high",
        alert_required=True,
        trigger_reason="NEWS2 >= 7",
        created_by_user_id=user.id,
    )
    db.add(locked_assessment)
    db.flush()
    alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.acknowledged,
        priority="urgent",
        trigger_reason="NEWS2 >= 7",
        created_at=datetime(2026, 6, 5, 9, 20, tzinfo=timezone.utc),
    )
    db.add(alert)
    db.flush()
    event = ClinicalDeteriorationEvent(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=assessment.id,
        alert_id=alert.id,
        deterioration_time=datetime(2026, 6, 5, 9, 25, tzinfo=timezone.utc),
        time_from_session_start_minutes=85,
        deterioration_type="acute_hypotension",
        triggering_news2_score=assessment.total_score,
        description="Acute hypotension.",
    )
    locked_event = ClinicalDeteriorationEvent(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=assessment.id,
        alert_id=alert.id,
        deterioration_time=datetime(2026, 6, 5, 9, 30, tzinfo=timezone.utc),
        time_from_session_start_minutes=90,
        deterioration_type="other",
        triggering_news2_score=assessment.total_score,
        description="Locked event.",
        is_locked=True,
    )
    db.add(event)
    db.flush()
    # Avoid alert_id uniqueness conflict for the locked-event test by assigning after main event flush.
    locked_alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=locked_assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.acknowledged,
        priority="urgent",
        trigger_reason="NEWS2 >= 7",
        created_at=datetime(2026, 6, 5, 9, 22, tzinfo=timezone.utc),
    )
    db.add(locked_alert)
    db.flush()
    locked_event.alert_id = locked_alert.id
    db.add(locked_event)
    db.commit()
    ids = {
        "user_id": user.id,
        "patient_id": patient.id,
        "session_id": session.id,
        "event_id": event.id,
        "locked_event_id": locked_event.id,
        "alert_id": alert.id,
    }
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


def response_payload(ids, **overrides):
    payload = {
        "clinical_deterioration_event_id": ids["event_id"],
        "actual_response_start_time": "2026-06-05T09:30:00Z",
        "patient_actions": ["stop_ultrafiltration", "give_oxygen", "doctor_called"],
        "vascular_access_actions": ["check_flow", "inspect_access_site"],
        "responded_by_user_id": ids["user_id"],
        "notes": "Response documented in test.",
    }
    payload.update(overrides)
    return payload


def test_create_response_from_valid_deterioration_event(response_client):
    client, TestingSession, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    assert response.json()["response_created"] is True
    assert response.json()["response"]["clinical_deterioration_event_id"] == ids["event_id"]
    db = TestingSession()
    try:
        assert db.query(ClinicalResponse).count() == 1
    finally:
        db.close()


def test_duplicate_response_reuses_existing_record(response_client):
    client, TestingSession, ids = response_client

    first = client.post("/api/responses", json=response_payload(ids))
    second = client.post("/api/responses", json=response_payload(ids, notes="Duplicate attempt."))

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["response_created"] is False
    assert second.json()["response"]["id"] == first.json()["response"]["id"]
    db = TestingSession()
    try:
        assert db.query(ClinicalResponse).count() == 1
    finally:
        db.close()


def test_invalid_event_returns_404(response_client):
    client, _, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids, clinical_deterioration_event_id=9999))

    assert response.status_code == 404


def test_locked_event_cannot_create_response(response_client):
    client, _, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids, clinical_deterioration_event_id=ids["locked_event_id"]))

    assert response.status_code == 400


def test_response_derives_alert_id_from_event(response_client):
    client, _, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    assert response.json()["response"]["alert_id"] == ids["alert_id"]


def test_response_delay_is_calculated_correctly(response_client):
    client, _, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    assert response.json()["response"]["response_delay_minutes"] == 10


def test_alert_status_moves_to_in_progress(response_client):
    client, TestingSession, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    db = TestingSession()
    try:
        alert = db.get(Alert, ids["alert_id"])
        assert alert.status == "in_progress"
    finally:
        db.close()


def test_list_endpoint_returns_responses(response_client):
    client, _, ids = response_client
    client.post("/api/responses", json=response_payload(ids))

    response = client.get("/api/responses", params={"clinical_deterioration_event_id": ids["event_id"]})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["alert_id"] == ids["alert_id"]


def test_detail_endpoint_returns_enriched_response(response_client):
    client, _, ids = response_client
    created = client.post("/api/responses", json=response_payload(ids)).json()["response"]

    response = client.get(f"/api/responses/{created['id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["patient_code"] == "RESP-P-1"
    assert payload["session_date"] == "2026-06-05"
    assert payload["news2_total_score"] == 15
    assert payload["deterioration_type"] == "acute_hypotension"
    assert "give_oxygen" in payload["patient_actions"]


def test_audit_log_entry_is_created(response_client):
    client, TestingSession, ids = response_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    db = TestingSession()
    try:
        assert db.query(AuditLog).filter(AuditLog.action == "clinical_response_created").count() == 1
    finally:
        db.close()
