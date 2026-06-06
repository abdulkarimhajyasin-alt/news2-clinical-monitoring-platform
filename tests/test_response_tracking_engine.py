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
    ClinicalDeteriorationEvent,
    DialysisSession,
    IntradialyticMeasurement,
    News2Assessment,
    Patient,
    ResponseTracking,
    StudyGroup,
    StudyPhase,
    User,
    UserRole,
)


@pytest.fixture()
def tracking_client(tmp_path):
    db_path = tmp_path / "response_tracking.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Tracking Doctor",
        email="tracking-doctor@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.doctor,
        department="Nephrology",
    )
    patient = Patient(
        patient_code="TRACK-P-1",
        full_name="Tracking Patient",
        age=64,
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
    db.add(event)
    db.commit()
    ids = {
        "user_id": user.id,
        "patient_id": patient.id,
        "session_id": session.id,
        "measurement_id": measurement.id,
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


def response_payload(ids, **overrides):
    payload = {
        "clinical_deterioration_event_id": ids["event_id"],
        "actual_response_start_time": "2026-06-05T09:30:00Z",
        "patient_actions": ["stop_ultrafiltration", "give_oxygen"],
        "vascular_access_actions": ["check_flow"],
        "responded_by_user_id": ids["user_id"],
        "notes": "Tracking response test.",
    }
    payload.update(overrides)
    return payload


def test_tracking_created_after_clinical_response_creation(tracking_client):
    client, TestingSession, ids = tracking_client

    response = client.post("/api/responses", json=response_payload(ids))

    assert response.status_code == 201
    db = TestingSession()
    try:
        tracking = db.query(ResponseTracking).filter(ResponseTracking.alert_id == ids["alert_id"]).one()
        assert tracking.actual_response_start_time is not None
    finally:
        db.close()


def test_time_to_alert_is_calculated(tracking_client):
    client, _, ids = tracking_client

    client.post("/api/responses", json=response_payload(ids))
    response = client.get("/api/response-tracking", params={"alert_id": ids["alert_id"]})

    assert response.status_code == 200
    assert response.json()[0]["time_to_alert_minutes"] == 5


def test_time_to_response_is_calculated(tracking_client):
    client, _, ids = tracking_client

    client.post("/api/responses", json=response_payload(ids))
    response = client.get("/api/response-tracking", params={"alert_id": ids["alert_id"]})

    assert response.status_code == 200
    assert response.json()[0]["time_to_response_minutes"] == 10


def test_optional_null_timestamps_do_not_crash(tracking_client):
    client, _, ids = tracking_client

    response = client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")

    assert response.status_code == 200
    tracking = response.json()["tracking"]
    assert tracking["alert_viewed_at"] is None
    assert tracking["time_to_view_minutes"] is None
    assert tracking["time_to_response_minutes"] is None


def test_negative_duration_sets_metric_null_and_returns_warning(tracking_client):
    client, TestingSession, ids = tracking_client
    db = TestingSession()
    try:
        alert = db.get(Alert, ids["alert_id"])
        alert.viewed_at = datetime(2026, 6, 5, 9, 10, tzinfo=timezone.utc)
        db.commit()
    finally:
        db.close()

    response = client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["tracking"]["time_to_view_minutes"] is None
    assert any("negative" in warning for warning in payload["warnings"])


def test_duplicate_tracking_rows_are_prevented(tracking_client):
    client, TestingSession, ids = tracking_client

    first = client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")
    second = client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")

    assert first.status_code == 200
    assert second.status_code == 200
    db = TestingSession()
    try:
        assert db.query(ResponseTracking).filter(ResponseTracking.alert_id == ids["alert_id"]).count() == 1
    finally:
        db.close()


def test_recalculate_endpoint_updates_tracking(tracking_client):
    client, _, ids = tracking_client

    response = client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")

    assert response.status_code == 200
    assert response.json()["tracking"]["alert_id"] == ids["alert_id"]
    assert response.json()["tracking"]["clinical_deterioration_event_id"] == ids["event_id"]


def test_summary_endpoint_returns_expected_keys(tracking_client):
    client, _, ids = tracking_client
    client.post("/api/responses", json=response_payload(ids))

    response = client.get("/api/response-tracking/summary")

    assert response.status_code == 200
    payload = response.json()
    expected = {
        "records_count",
        "average_time_to_alert_minutes",
        "average_time_to_view_minutes",
        "average_time_to_response_minutes",
        "average_time_to_action_minutes",
        "average_total_response_time_minutes",
        "fastest_response_minutes",
        "slowest_response_minutes",
        "alerts_without_response_count",
    }
    assert expected.issubset(payload.keys())


def test_alert_lifecycle_update_refreshes_tracking(tracking_client):
    client, _, ids = tracking_client
    client.post(f"/api/response-tracking/recalculate/{ids['alert_id']}")

    view_response = client.post(f"/api/alerts/{ids['alert_id']}/view")
    list_response = client.get("/api/response-tracking", params={"alert_id": ids["alert_id"]})

    assert view_response.status_code == 200
    assert list_response.status_code == 200
    assert list_response.json()[0]["alert_viewed_at"] is not None
    assert list_response.json()[0]["time_to_view_minutes"] is not None


def test_list_endpoint_returns_enriched_fields(tracking_client):
    client, _, ids = tracking_client
    client.post("/api/responses", json=response_payload(ids))

    response = client.get("/api/response-tracking", params={"alert_id": ids["alert_id"]})

    assert response.status_code == 200
    payload = response.json()[0]
    assert payload["patient_code"] == "TRACK-P-1"
    assert payload["session_date"] == "2026-06-05"
    assert payload["news2_total_score"] == 15
    assert payload["risk_level"] == "high"
    assert payload["deterioration_type"] == "acute_hypotension"
