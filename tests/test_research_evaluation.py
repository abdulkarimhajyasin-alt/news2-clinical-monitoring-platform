import json
from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import DialysisSession, IntradialyticMeasurement, News2Assessment, OutcomeValidation72h, Patient, StudyGroup, StudyPhase, User, UserRole
from app.services.research_evaluation_service import build_prediction_summary, classify_session_prediction


def test_classify_true_positive_early():
    result = classify_session_prediction(validation_completed=True, deterioration_occurred=True, prediction_status="predicted_before", red_alert_present=True)

    assert result["prediction_classification"] == "true_positive_early"


def test_classify_true_positive_concurrent():
    result = classify_session_prediction(validation_completed=True, deterioration_occurred=True, prediction_status="predicted_concurrent", red_alert_present=True)

    assert result["prediction_classification"] == "true_positive_concurrent"


def test_classify_false_negative():
    result = classify_session_prediction(validation_completed=True, deterioration_occurred=True, prediction_status="false_negative", red_alert_present=False)

    assert result["prediction_classification"] == "false_negative"


def test_classify_true_negative():
    result = classify_session_prediction(validation_completed=True, deterioration_occurred=False, prediction_status=None, red_alert_present=False)

    assert result["prediction_classification"] == "true_negative"


def test_classify_false_positive():
    result = classify_session_prediction(validation_completed=True, deterioration_occurred=False, prediction_status=None, red_alert_present=True)

    assert result["prediction_classification"] == "false_positive"


def test_classify_incomplete():
    result = classify_session_prediction(validation_completed=False, deterioration_occurred=None, prediction_status=None, red_alert_present=False)

    assert result["prediction_classification"] == "incomplete"


@pytest.fixture()
def evaluation_client(tmp_path):
    db_path = tmp_path / "research_evaluation.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    _seed_evaluation_data(db)
    db.close()

    def override_get_db():
        test_db = TestingSession()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), TestingSession
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_prediction_summary_returns_expected_metrics(evaluation_client):
    client, _ = evaluation_client

    response = client.get("/api/research/evaluation/prediction-summary")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_sessions"] == 6
    assert payload["validated_sessions"] == 5
    assert payload["true_positive_early"] == 1
    assert payload["true_positive_concurrent"] == 1
    assert payload["false_negative"] == 1
    assert payload["true_negative"] == 1
    assert payload["false_positive"] == 1
    assert payload["sensitivity"] == 66.7
    assert payload["specificity"] == 50.0


def test_prediction_summary_safe_division_with_empty_database(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'empty_eval.db'}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    try:
        payload = build_prediction_summary(db)
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

    assert payload["total_sessions"] == 0
    assert payload["sensitivity"] is None
    assert payload["specificity"] is None


def test_prediction_dataset_excludes_deleted_patients(evaluation_client):
    client, _ = evaluation_client

    response = client.get("/api/research/evaluation/prediction-dataset")

    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 6
    assert "DEL-P" not in {row["patient_code"] for row in rows}


def test_by_risk_color_grouping_works(evaluation_client):
    client, _ = evaluation_client

    response = client.get("/api/research/evaluation/by-risk-color")

    assert response.status_code == 200
    red = next(row for row in response.json() if row["risk_color"] == "red")
    assert red["false_positive"] == 1


def test_by_deterioration_type_grouping_works(evaluation_client):
    client, _ = evaluation_client

    response = client.get("/api/research/evaluation/by-deterioration-type")

    assert response.status_code == 200
    hypotension = next(row for row in response.json() if row["deterioration_type"] == "severe_hypotension")
    assert hypotension["true_positive_early"] == 1


def test_research_evaluation_requires_analytics_permission(evaluation_client):
    client, _ = evaluation_client

    response = client.get("/api/research/evaluation/prediction-summary", headers={"X-Dev-Role": "nurse"})

    assert response.status_code == 403


def _seed_evaluation_data(db):
    user = User(full_name="Evaluation Doctor", email="evaluation@example.local", password_hash="x", role=UserRole.doctor)
    patient = Patient(patient_code="EVAL-P", full_name="Evaluation Patient", age=60, gender="male", study_phase=StudyPhase.post_implementation, study_group=StudyGroup.intervention)
    deleted = Patient(patient_code="DEL-P", full_name="Deleted Patient", age=60, gender="male", study_phase=StudyPhase.post_implementation, study_group=StudyGroup.intervention, status="deleted")
    db.add_all([user, patient, deleted])
    db.flush()
    _session_case(db, patient.id, "predicted_before", True, "red", ["severe_hypotension"])
    _session_case(db, patient.id, "predicted_concurrent", True, "yellow", ["cardiac_arrhythmia"])
    _session_case(db, patient.id, "false_negative", True, "green", ["electrolyte_disorder"])
    _session_case(db, patient.id, None, False, "green", [])
    _session_case(db, patient.id, None, False, "red", [])
    _session_case(db, patient.id, None, None, "yellow", [], validation=False)
    _session_case(db, deleted.id, "predicted_before", True, "red", ["death"])
    db.commit()


def _session_case(db, patient_id, prediction_status, deterioration_occurred, hd2_color, deterioration_types, validation=True):
    session = DialysisSession(patient_id=patient_id, session_date=date(2026, 6, 5), actual_start_time=datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc), session_status="completed")
    db.add(session)
    db.flush()
    measurement = IntradialyticMeasurement(patient_id=patient_id, dialysis_session_id=session.id, measurement_time=datetime(2026, 6, 5, 9, 0, tzinfo=timezone.utc), measurement_interval_minutes=30, respiratory_rate=18, spo2=96, oxygen_therapy=False, systolic_bp=120, diastolic_bp=70, pulse_rate=80, temperature=37.0, consciousness_level="alert")
    db.add(measurement)
    db.flush()
    score = {"green": 2, "yellow": 5, "red": 8}[hd2_color]
    assessment = News2Assessment(
        patient_id=patient_id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=measurement.id,
        respiratory_score=0,
        spo2_score=0,
        oxygen_score=0,
        systolic_bp_score=0,
        pulse_score=0,
        temperature_score=0,
        consciousness_score=0,
        total_score=score,
        risk_level="high" if hd2_color == "red" else "low",
        alert_required=hd2_color == "red",
        trigger_reason="test",
        hd2_mnews_total_score=score,
        hd2_mnews_risk_color=hd2_color,
        hd2_mnews_risk_label_ar=hd2_color,
        hd2_mnews_critical_trigger=hd2_color == "red",
        hd2_mnews_critical_reasons=json.dumps(["test"]) if hd2_color == "red" else None,
    )
    db.add(assessment)
    db.flush()
    if validation:
        db.add(
            OutcomeValidation72h(
                patient_id=patient_id,
                dialysis_session_id=session.id,
                deterioration_occurred=bool(deterioration_occurred),
                deterioration_types=json.dumps(deterioration_types),
                type_specific_details=json.dumps({}),
                deterioration_timing_category="within_24_72h" if deterioration_occurred else None,
                platform_prediction_status=prediction_status,
                interventions=json.dumps(["doctor_called"]) if deterioration_occurred else json.dumps([]),
                doctor_response_time_minutes=5 if deterioration_occurred else None,
                final_result="partial_improvement" if deterioration_occurred else None,
                verification_sources=json.dumps(["medical_record_reviewed"]),
                notes="validated",
                completed_at=datetime(2026, 6, 8, 12, 0, tzinfo=timezone.utc),
            )
        )
