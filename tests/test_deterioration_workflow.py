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
def deterioration_client(tmp_path):
    db_path = tmp_path / "deterioration_workflow.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Deterioration Doctor",
        email="deterioration-doctor@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.doctor,
        department="Nephrology",
    )
    patient = Patient(
        patient_code="DET-P-1",
        full_name="Deterioration Patient",
        age=61,
        gender="male",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add_all([user, patient])
    db.flush()
    session_start = datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc)
    dialysis_session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 5),
        actual_start_time=session_start,
        session_status="active",
        created_by_user_id=user.id,
    )
    db.add(dialysis_session)
    db.flush()
    measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=dialysis_session.id,
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
        dialysis_session_id=dialysis_session.id,
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
    closed_measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=dialysis_session.id,
        measurement_time=datetime(2026, 6, 5, 9, 45, tzinfo=timezone.utc),
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
    db.add(closed_measurement)
    db.flush()
    closed_assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=dialysis_session.id,
        intradialytic_measurement_id=closed_measurement.id,
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
    db.add(closed_assessment)
    db.flush()
    alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=dialysis_session.id,
        news2_assessment_id=assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.new,
        priority="urgent",
        trigger_reason="NEWS2 >= 7",
    )
    closed_alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=dialysis_session.id,
        news2_assessment_id=closed_assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.closed,
        priority="urgent",
        trigger_reason="NEWS2 >= 7",
    )
    db.add_all([alert, closed_alert])
    db.commit()
    ids = {
        "user_id": user.id,
        "patient_id": patient.id,
        "session_id": dialysis_session.id,
        "assessment_id": assessment.id,
        "alert_id": alert.id,
        "closed_alert_id": closed_alert.id,
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


def event_payload(ids, **overrides):
    payload = {
        "alert_id": ids["alert_id"],
        "deterioration_time": "2026-06-05T09:30:00Z",
        "deterioration_type": "acute_hypotension",
        "description": "Acute hypotension during dialysis.",
        "created_by_user_id": ids["user_id"],
    }
    payload.update(overrides)
    return payload


def test_create_deterioration_event_from_valid_active_alert(deterioration_client):
    client, TestingSession, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids))

    assert response.status_code == 201
    payload = response.json()
    assert payload["event_created"] is True
    assert payload["event"]["alert_id"] == ids["alert_id"]
    assert payload["event"]["time_from_session_start_minutes"] == 90
    db = TestingSession()
    try:
        assert db.query(ClinicalDeteriorationEvent).count() == 1
    finally:
        db.close()


def test_duplicate_creation_reuses_existing_event(deterioration_client):
    client, TestingSession, ids = deterioration_client

    first = client.post("/api/deterioration/events", json=event_payload(ids))
    second = client.post("/api/deterioration/events", json=event_payload(ids, description="Duplicate attempt."))

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["event_created"] is False
    assert second.json()["event"]["id"] == first.json()["event"]["id"]
    db = TestingSession()
    try:
        assert db.query(ClinicalDeteriorationEvent).count() == 1
    finally:
        db.close()


def test_closed_alert_cannot_create_deterioration_event(deterioration_client):
    client, _, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids, alert_id=ids["closed_alert_id"]))

    assert response.status_code == 400


def test_invalid_alert_returns_404(deterioration_client):
    client, _, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids, alert_id=9999))

    assert response.status_code == 404


def test_event_derives_patient_session_and_assessment_from_alert(deterioration_client):
    client, _, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids))

    event = response.json()["event"]
    assert event["patient_id"] == ids["patient_id"]
    assert event["dialysis_session_id"] == ids["session_id"]
    assert event["news2_assessment_id"] == ids["assessment_id"]


def test_event_derives_triggering_news2_score_from_assessment(deterioration_client):
    client, _, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids))

    event = response.json()["event"]
    assert event["triggering_news2_score"] == 15
    assert event["news2_total_score"] == 15


def test_alert_status_moves_to_in_progress(deterioration_client):
    client, TestingSession, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids))

    assert response.status_code == 201
    db = TestingSession()
    try:
        alert = db.get(Alert, ids["alert_id"])
        assert alert.status == "in_progress"
        assert alert.action_taken_at is not None
    finally:
        db.close()


def test_list_endpoint_returns_created_events(deterioration_client):
    client, _, ids = deterioration_client
    client.post("/api/deterioration/events", json=event_payload(ids))

    response = client.get("/api/deterioration/events", params={"alert_id": ids["alert_id"]})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["alert_id"] == ids["alert_id"]


def test_detail_endpoint_returns_enriched_event_info(deterioration_client):
    client, _, ids = deterioration_client
    created = client.post("/api/deterioration/events", json=event_payload(ids)).json()["event"]

    response = client.get(f"/api/deterioration/events/{created['id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["patient_code"] == "DET-P-1"
    assert payload["session_date"] == "2026-06-05"
    assert payload["news2_total_score"] == 15
    assert payload["alert_status"] == "in_progress"


def test_audit_log_entry_is_created(deterioration_client):
    client, TestingSession, ids = deterioration_client

    response = client.post("/api/deterioration/events", json=event_payload(ids))

    assert response.status_code == 201
    db = TestingSession()
    try:
        assert db.query(AuditLog).filter(AuditLog.action == "clinical_deterioration_event_created").count() == 1
    finally:
        db.close()
