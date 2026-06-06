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
    ClinicalOutcome,
    ClinicalResponse,
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
def analytics_client(tmp_path):
    db_path = tmp_path / "research_analytics.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    _seed_analytics_data(TestingSession())
    yield from _client_for(TestingSession, engine)


@pytest.fixture()
def empty_analytics_client(tmp_path):
    db_path = tmp_path / "empty_research_analytics.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    yield from _client_for(TestingSession, engine)


def test_kpi_summary_returns_expected_keys(analytics_client):
    response = analytics_client.get("/api/research/analytics/summary")

    assert response.status_code == 200
    kpis = response.json()["kpis"]
    expected = {
        "total_patients",
        "total_sessions",
        "total_measurements",
        "total_news2_assessments",
        "total_alerts",
        "total_deterioration_events",
        "total_responses",
        "total_outcomes",
        "average_news2_score",
        "average_response_time_minutes",
        "dataset_quality_score",
    }
    assert expected.issubset(kpis.keys())


def test_news2_distribution_works(analytics_client):
    response = analytics_client.get("/api/research/analytics/news2-distribution")

    assert response.status_code == 200
    payload = response.json()
    assert [item["bucket"] for item in payload] == ["0_2", "3_4", "5_6", "7_plus"]
    assert sum(item["count"] for item in payload) == 3


def test_outcome_analysis_works(analytics_client):
    response = analytics_client.get("/api/research/analytics/outcomes")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_outcomes"] == 1
    assert payload["adverse_outcome_rate"] == 100.0


def test_response_analysis_works(analytics_client):
    response = analytics_client.get("/api/research/analytics/response-times")

    assert response.status_code == 200
    payload = response.json()
    assert payload["average_time_to_response"] == 9.0
    assert payload["median_response"] == 9.0


def test_deterioration_analysis_works(analytics_client):
    response = analytics_client.get("/api/research/analytics/deterioration")

    assert response.status_code == 200
    payload = response.json()
    acute = next(item for item in payload if item["deterioration_type"] == "acute_hypotension")
    assert acute["count"] == 1
    assert acute["associated_outcomes"]["hospital_admission"] == 1


def test_empty_dataset_handled_safely(empty_analytics_client):
    response = empty_analytics_client.get("/api/research/analytics/summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["kpis"]["total_measurements"] == 0
    assert payload["kpis"]["average_news2_score"] is None
    assert payload["news2_distribution"][0]["percentage"] == 0


def test_group_comparison_safe_without_groups(empty_analytics_client):
    response = empty_analytics_client.get("/api/research/analytics/group-comparison")

    assert response.status_code == 200
    payload = response.json()
    assert payload["study_group"]["group_a"]["name"] is None
    assert payload["study_group"]["group_b"]["count"] == 0


def test_api_endpoints_return_valid_payloads(analytics_client):
    endpoints = [
        "/api/research/analytics/summary",
        "/api/research/analytics/news2-distribution",
        "/api/research/analytics/outcomes",
        "/api/research/analytics/response-times",
        "/api/research/analytics/deterioration",
        "/api/research/analytics/group-comparison",
    ]

    for endpoint in endpoints:
        response = analytics_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() is not None


def test_percentages_sum_correctly(analytics_client):
    response = analytics_client.get("/api/research/analytics/news2-distribution")

    assert response.status_code == 200
    total_percentage = sum(item["percentage"] for item in response.json())
    assert total_percentage == 100.0


def test_frontend_facing_structures_remain_stable(analytics_client):
    response = analytics_client.get("/api/research/analytics/summary")

    payload = response.json()
    assert {"kpis", "news2_distribution", "risk_level_distribution", "outcome_analysis", "response_time_analysis", "deterioration_analysis", "group_comparison"}.issubset(payload.keys())
    assert "distribution" in payload["outcome_analysis"]
    assert "study_group" in payload["group_comparison"]


def _client_for(TestingSession, engine):
    def override_get_db():
        test_db = TestingSession()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def _seed_analytics_data(db):
    user = User(full_name="Analytics Doctor", email="analytics@example.local", password_hash="not-for-auth", role=UserRole.doctor)
    patient = Patient(
        patient_code="ANALYTICS-P-1",
        full_name="Analytics Patient",
        age=66,
        gender="male",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add_all([user, patient])
    db.flush()
    session = DialysisSession(patient_id=patient.id, session_date=date(2026, 6, 5), actual_start_time=datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc), session_status="completed")
    db.add(session)
    db.flush()
    measurements = [
        IntradialyticMeasurement(patient_id=patient.id, dialysis_session_id=session.id, measurement_time=datetime(2026, 6, 5, 8, 30, tzinfo=timezone.utc), measurement_interval_minutes=30, respiratory_rate=18, spo2=97, oxygen_therapy=False, systolic_bp=136, diastolic_bp=76, pulse_rate=84, temperature=36.7, consciousness_level="alert", confusion_status="none"),
        IntradialyticMeasurement(patient_id=patient.id, dialysis_session_id=session.id, measurement_time=datetime(2026, 6, 5, 9, 0, tzinfo=timezone.utc), measurement_interval_minutes=30, respiratory_rate=20, spo2=95, oxygen_therapy=False, systolic_bp=130, diastolic_bp=74, pulse_rate=88, temperature=37.0, consciousness_level="alert", confusion_status="none"),
        IntradialyticMeasurement(patient_id=patient.id, dialysis_session_id=session.id, measurement_time=datetime(2026, 6, 5, 9, 15, tzinfo=timezone.utc), measurement_interval_minutes=30, respiratory_rate=25, spo2=90, oxygen_therapy=True, systolic_bp=88, diastolic_bp=54, pulse_rate=118, temperature=38.1, consciousness_level="alert", confusion_status="new_confusion"),
    ]
    db.add_all(measurements)
    db.flush()
    assessments = [
        News2Assessment(patient_id=patient.id, dialysis_session_id=session.id, intradialytic_measurement_id=measurements[0].id, respiratory_score=0, spo2_score=0, oxygen_score=0, systolic_bp_score=0, pulse_score=0, temperature_score=0, consciousness_score=0, total_score=0, risk_level="low", alert_required=False, trigger_reason="low"),
        News2Assessment(patient_id=patient.id, dialysis_session_id=session.id, intradialytic_measurement_id=measurements[1].id, respiratory_score=1, spo2_score=1, oxygen_score=0, systolic_bp_score=0, pulse_score=1, temperature_score=0, consciousness_score=0, total_score=3, risk_level="medium", alert_required=False, trigger_reason="medium"),
        News2Assessment(patient_id=patient.id, dialysis_session_id=session.id, intradialytic_measurement_id=measurements[2].id, respiratory_score=3, spo2_score=3, oxygen_score=2, systolic_bp_score=3, pulse_score=2, temperature_score=1, consciousness_score=3, total_score=17, risk_level="high", alert_required=True, trigger_reason="NEWS2 >= 7"),
    ]
    db.add_all(assessments)
    db.flush()
    alert = Alert(patient_id=patient.id, dialysis_session_id=session.id, news2_assessment_id=assessments[2].id, risk_level="high", severity_level="high", status=AlertStatus.in_progress, priority="immediate", trigger_reason="NEWS2 >= 7", created_at=datetime(2026, 6, 5, 9, 16, tzinfo=timezone.utc))
    db.add(alert)
    db.flush()
    event = ClinicalDeteriorationEvent(patient_id=patient.id, dialysis_session_id=session.id, news2_assessment_id=assessments[2].id, alert_id=alert.id, deterioration_time=datetime(2026, 6, 5, 9, 20, tzinfo=timezone.utc), time_from_session_start_minutes=80, deterioration_type="acute_hypotension", triggering_news2_score=17, description="Acute hypotension.")
    db.add(event)
    db.flush()
    response = ClinicalResponse(clinical_deterioration_event_id=event.id, alert_id=alert.id, digital_alert_time=alert.created_at, actual_response_start_time=datetime(2026, 6, 5, 9, 25, tzinfo=timezone.utc), response_delay_minutes=9, patient_actions='["give_oxygen"]', vascular_access_actions='["check_flow"]', responded_by_user_id=user.id, notes="Response.")
    outcome = ClinicalOutcome(patient_id=patient.id, dialysis_session_id=session.id, clinical_deterioration_event_id=event.id, outcome_type="hospital_admission", outcome_recorded_at=datetime(2026, 6, 6, 9, 20, tzinfo=timezone.utc), outcome_window_hours=24, description="Admitted.")
    tracking = ResponseTracking(alert_id=alert.id, dialysis_session_id=session.id, news2_assessment_id=assessments[2].id, clinical_deterioration_event_id=event.id, vital_signs_recorded_at=measurements[2].measurement_time, alert_created_at=alert.created_at, actual_response_start_time=response.actual_response_start_time, clinical_action_at=response.actual_response_start_time, time_to_alert_minutes=1, time_to_response_minutes=9, time_to_action_minutes=9, total_response_time_minutes=10)
    db.add_all([response, outcome, tracking])
    db.commit()
    db.close()
