from datetime import date, datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, DialysisSession, OutcomeValidation72h, Patient, StudyGroup, StudyPhase, User, UserRole


@pytest.fixture()
def validation_client(tmp_path):
    db_path = tmp_path / "outcome_validation_72h.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(full_name="Outcome Doctor", email="validation-doctor@example.local", password_hash="x", role=UserRole.doctor)
    patient = Patient(patient_code="VAL-P-1", full_name="Validation Patient", age=61, gender="female", study_phase=StudyPhase.post_implementation, study_group=StudyGroup.intervention)
    db.add_all([user, patient])
    db.flush()
    eligible_session = DialysisSession(
        patient_id=patient.id,
        session_date=date.today(),
        actual_start_time=datetime.now(timezone.utc) - timedelta(hours=78),
        actual_end_time=datetime.now(timezone.utc) - timedelta(hours=74),
        session_duration_minutes=240,
        session_status="completed",
    )
    early_session = DialysisSession(
        patient_id=patient.id,
        session_date=date.today(),
        actual_start_time=datetime.now(timezone.utc) - timedelta(hours=10),
        actual_end_time=datetime.now(timezone.utc) - timedelta(hours=6),
        session_duration_minutes=240,
        session_status="completed",
    )
    db.add_all([eligible_session, early_session])
    db.commit()
    ids = {"patient_id": patient.id, "eligible_session_id": eligible_session.id, "early_session_id": early_session.id, "user_id": user.id}
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


def no_deterioration_payload(ids, **overrides):
    payload = {
        "patient_id": ids["patient_id"],
        "dialysis_session_id": ids["eligible_session_id"],
        "deterioration_occurred": False,
        "verification_sources": ["medical_record_reviewed"],
        "notes": "No deterioration documented after 72 hours.",
        "completed_by_user_id": ids["user_id"],
    }
    payload.update(overrides)
    return payload


def yes_deterioration_payload(ids, **overrides):
    payload = {
        "patient_id": ids["patient_id"],
        "dialysis_session_id": ids["eligible_session_id"],
        "deterioration_occurred": True,
        "deterioration_types": ["severe_hypotension", "cardiac_arrhythmia", "electrolyte_disorder"],
        "type_specific_details": {
            "lowest_sbp": 78,
            "required_treatment": True,
            "arrhythmia_type": "tachycardia",
            "potassium_value": 6.1,
        },
        "deterioration_timing_category": "within_24_72h",
        "deterioration_datetime": (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat(),
        "platform_prediction_status": "predicted_before",
        "interventions": ["doctor_called", "fluids_given"],
        "doctor_response_time_minutes": 4,
        "final_result": "partial_improvement",
        "verification_sources": ["medical_record_reviewed", "nurse_interviewed"],
        "notes": "Deterioration validated from chart review.",
        "completed_by_user_id": ids["user_id"],
    }
    payload.update(overrides)
    return payload


def test_cannot_create_validation_before_72_hours(validation_client):
    client, _, ids = validation_client
    payload = no_deterioration_payload(ids, dialysis_session_id=ids["early_session_id"])

    response = client.post("/api/outcome-validations", json=payload)

    assert response.status_code == 400
    assert "72" in response.json()["detail"]


def test_can_create_no_deterioration_validation_after_72_hours(validation_client):
    client, TestingSession, ids = validation_client

    response = client.post("/api/outcome-validations", json=no_deterioration_payload(ids))

    assert response.status_code == 201
    payload = response.json()["validation"]
    assert payload["deterioration_occurred"] is False
    assert payload["verification_sources"] == ["medical_record_reviewed"]
    db = TestingSession()
    try:
        assert db.query(OutcomeValidation72h).count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "outcome_validation_72h_created").count() == 1
    finally:
        db.close()


def test_no_deterioration_requires_notes_and_verification_source(validation_client):
    client, _, ids = validation_client

    response = client.post("/api/outcome-validations", json=no_deterioration_payload(ids, notes=None, verification_sources=[]))

    assert response.status_code == 422


def test_yes_deterioration_requires_core_followup_fields(validation_client):
    client, _, ids = validation_client

    response = client.post(
        "/api/outcome-validations",
        json=yes_deterioration_payload(ids, deterioration_types=[], platform_prediction_status=None),
    )

    assert response.status_code == 422


def test_type_specific_details_persist(validation_client):
    client, _, ids = validation_client

    response = client.post("/api/outcome-validations", json=yes_deterioration_payload(ids))

    assert response.status_code == 201
    details = response.json()["validation"]["type_specific_details"]
    assert details["lowest_sbp"] == 78
    assert details["arrhythmia_type"] == "tachycardia"
    assert details["potassium_value"] == 6.1


def test_doctor_response_time_required_when_doctor_called(validation_client):
    client, _, ids = validation_client

    response = client.post("/api/outcome-validations", json=yes_deterioration_payload(ids, doctor_response_time_minutes=None))

    assert response.status_code == 422


def test_duplicate_session_validation_is_rejected(validation_client):
    client, _, ids = validation_client

    first = client.post("/api/outcome-validations", json=no_deterioration_payload(ids))
    second = client.post("/api/outcome-validations", json=no_deterioration_payload(ids))

    assert first.status_code == 201
    assert second.status_code == 409


def test_session_lookup_returns_eligibility_or_existing_validation(validation_client):
    client, _, ids = validation_client

    early = client.get(f"/api/outcome-validations/session/{ids['early_session_id']}")
    assert early.status_code == 200
    assert early.json()["eligible_for_completion"] is False

    client.post("/api/outcome-validations", json=no_deterioration_payload(ids))
    existing = client.get(f"/api/outcome-validations/session/{ids['eligible_session_id']}")
    assert existing.status_code == 200
    assert existing.json()["deterioration_occurred"] is False
