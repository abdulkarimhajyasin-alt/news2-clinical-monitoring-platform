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
    ClinicalOutcome,
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
def outcome_client(tmp_path):
    db_path = tmp_path / "outcome_workflow.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Outcome Doctor",
        email="outcome-doctor@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.doctor,
        department="Nephrology",
    )
    patient = Patient(
        patient_code="OUT-P-1",
        full_name="Outcome Patient",
        age=68,
        gender="male",
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
    alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.in_progress,
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
    db.add(event)
    db.commit()
    ids = {
        "user_id": user.id,
        "patient_id": patient.id,
        "session_id": session.id,
        "assessment_id": assessment.id,
        "alert_id": alert.id,
        "event_id": event.id,
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


def outcome_payload(ids, **overrides):
    payload = {
        "clinical_deterioration_event_id": ids["event_id"],
        "outcome_type": "hospital_admission",
        "outcome_window_hours": 24,
        "description": "Admitted for post-dialysis monitoring.",
        "recorded_by_user_id": ids["user_id"],
    }
    payload.update(overrides)
    return payload


def test_create_outcome_successfully(outcome_client):
    client, TestingSession, ids = outcome_client

    response = client.post("/api/outcomes", json=outcome_payload(ids))

    assert response.status_code == 201
    assert response.json()["outcome_created"] is True
    assert response.json()["outcome"]["clinical_deterioration_event_id"] == ids["event_id"]
    db = TestingSession()
    try:
        assert db.query(ClinicalOutcome).count() == 1
    finally:
        db.close()


def test_duplicate_window_prevented(outcome_client):
    client, TestingSession, ids = outcome_client

    first = client.post("/api/outcomes", json=outcome_payload(ids))
    second = client.post("/api/outcomes", json=outcome_payload(ids, outcome_type="death"))

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["outcome_created"] is False
    assert second.json()["outcome"]["id"] == first.json()["outcome"]["id"]
    db = TestingSession()
    try:
        assert db.query(ClinicalOutcome).count() == 1
    finally:
        db.close()


def test_different_windows_allowed(outcome_client):
    client, TestingSession, ids = outcome_client

    first = client.post("/api/outcomes", json=outcome_payload(ids, outcome_window_hours=24))
    second = client.post("/api/outcomes", json=outcome_payload(ids, outcome_window_hours=48))

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["outcome_created"] is True
    db = TestingSession()
    try:
        assert db.query(ClinicalOutcome).count() == 2
    finally:
        db.close()


def test_invalid_event_returns_404(outcome_client):
    client, _, ids = outcome_client

    response = client.post("/api/outcomes", json=outcome_payload(ids, clinical_deterioration_event_id=9999))

    assert response.status_code == 404


def test_outcome_derives_patient_and_session_from_event(outcome_client):
    client, _, ids = outcome_client

    response = client.post("/api/outcomes", json=outcome_payload(ids))

    assert response.status_code == 201
    outcome = response.json()["outcome"]
    assert outcome["patient_id"] == ids["patient_id"]
    assert outcome["dialysis_session_id"] == ids["session_id"]


def test_outcome_summary_returns_expected_counts(outcome_client):
    client, _, ids = outcome_client
    client.post("/api/outcomes", json=outcome_payload(ids, outcome_type="hospital_admission"))

    response = client.get("/api/outcomes/summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_outcomes"] == 1
    assert payload["hospital_admission_count"] == 1
    assert payload["death_count"] == 0


def test_audit_logs_created(outcome_client):
    client, TestingSession, ids = outcome_client

    client.post("/api/outcomes", json=outcome_payload(ids))
    client.post("/api/outcomes", json=outcome_payload(ids))

    db = TestingSession()
    try:
        assert db.query(AuditLog).filter(AuditLog.action == "clinical_outcome_created").count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "clinical_outcome_reused").count() == 1
    finally:
        db.close()


def test_list_endpoint_returns_outcomes(outcome_client):
    client, _, ids = outcome_client
    client.post("/api/outcomes", json=outcome_payload(ids))

    response = client.get("/api/outcomes", params={"clinical_deterioration_event_id": ids["event_id"]})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["alert_id"] == ids["alert_id"]


def test_detail_endpoint_returns_enriched_outcome(outcome_client):
    client, _, ids = outcome_client
    created = client.post("/api/outcomes", json=outcome_payload(ids)).json()["outcome"]

    response = client.get(f"/api/outcomes/{created['id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["patient_code"] == "OUT-P-1"
    assert payload["session_date"] == "2026-06-05"
    assert payload["alert_id"] == ids["alert_id"]
    assert payload["news2_total_score"] == 15
    assert payload["deterioration_type"] == "acute_hypotension"


def test_outcome_analytics_updates_research_summary(outcome_client):
    client, _, ids = outcome_client
    client.post("/api/outcomes", json=outcome_payload(ids, outcome_type="icu_admission"))

    response = client.get("/api/research/summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["outcomes_count"] == 1
    assert payload["total_outcomes"] == 1
    assert payload["icu_admission_count"] == 1
