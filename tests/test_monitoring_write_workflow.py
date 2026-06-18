from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Alert, DialysisSession, IntradialyticMeasurement, News2Assessment, Patient, StudyGroup, StudyPhase, User, UserRole
from app.schemas import NEWS2CalculationRequest
from app.services.news2_service import calculate_news2


@pytest.fixture()
def client_with_database(tmp_path):
    db_path = tmp_path / "monitoring_write.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Seed Nurse",
        email="nurse-write@example.local",
        password_hash="not-for-auth-phase",
        role=UserRole.nurse,
        department="Dialysis Unit",
    )
    patient = Patient(
        patient_code="TEST-P-1",
        full_name="Test Patient 1",
        age=55,
        gender="female",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    other_patient = Patient(
        patient_code="TEST-P-2",
        full_name="Test Patient 2",
        age=60,
        gender="male",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.control,
    )
    db.add_all([user, patient, other_patient])
    db.flush()
    session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 5),
        session_status="active",
        created_by_user_id=user.id,
    )
    other_session = DialysisSession(
        patient_id=other_patient.id,
        session_date=date(2026, 6, 5),
        session_status="active",
        created_by_user_id=user.id,
    )
    db.add_all([session, other_session])
    db.commit()
    ids = {
        "patient_id": patient.id,
        "other_patient_id": other_patient.id,
        "session_id": session.id,
        "other_session_id": other_session.id,
        "user_id": user.id,
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


def valid_payload(ids):
    return {
        "patient_id": ids["patient_id"],
        "dialysis_session_id": ids["session_id"],
        "measurement_time": "2026-06-05T10:30:00Z",
        "measurement_interval_minutes": 30,
        "respiratory_rate": 22,
        "spo2": 94,
        "oxygen_therapy": False,
        "systolic_bp": 105,
        "diastolic_bp": 65,
        "pulse_rate": 112,
        "temperature": 38.2,
        "consciousness_level": "alert",
        "confusion_status": False,
        "spo2_scale": "scale_1",
        "recorded_by_user_id": ids["user_id"],
    }


def test_valid_measurement_creates_measurement_and_news2_assessment(client_with_database):
    client, TestingSession, ids = client_with_database

    response = client.post("/api/monitoring/measurements", json=valid_payload(ids))

    assert response.status_code == 201
    payload = response.json()
    assert payload["message"] == "Measurement saved, NEWS2 calculated, and alert rules evaluated successfully"
    assert payload["measurement"]["id"] > 0
    assert payload["news2_assessment"]["intradialytic_measurement_id"] == payload["measurement"]["id"]

    db = TestingSession()
    try:
        assert db.query(IntradialyticMeasurement).count() == 1
        assert db.query(News2Assessment).count() == 1
    finally:
        db.close()


def test_invalid_patient_returns_404(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)
    payload["patient_id"] = 9999

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 404


def test_invalid_session_returns_404(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)
    payload["dialysis_session_id"] = 9999

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 404


def test_session_patient_mismatch_returns_400(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)
    payload["dialysis_session_id"] = ids["other_session_id"]

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 400


@pytest.mark.parametrize("patient_status", ["discharged", "archived", "deleted"])
def test_non_active_patients_cannot_receive_measurements(client_with_database, patient_status):
    client, TestingSession, ids = client_with_database
    db = TestingSession()
    try:
        patient = db.get(Patient, ids["patient_id"])
        patient.status = patient_status
        db.commit()
    finally:
        db.close()

    response = client.post("/api/monitoring/measurements", json=valid_payload(ids))

    assert response.status_code == 400
    assert response.json()["detail"] == "Patient is not active"
    db = TestingSession()
    try:
        assert db.query(IntradialyticMeasurement).count() == 0
        assert db.query(News2Assessment).count() == 0
        assert db.query(Alert).count() == 0
    finally:
        db.close()


def test_invalid_vital_signs_return_422(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)
    payload["spo2"] = 101

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 422


def test_created_news2_score_matches_engine_output(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)

    response = client.post("/api/monitoring/measurements", json=payload)

    expected = calculate_news2(
        NEWS2CalculationRequest(
            respiratory_rate=payload["respiratory_rate"],
            spo2=payload["spo2"],
            oxygen_therapy=payload["oxygen_therapy"],
            systolic_bp=payload["systolic_bp"],
            pulse_rate=payload["pulse_rate"],
            temperature=payload["temperature"],
            consciousness_level=payload["consciousness_level"],
            spo2_scale=payload["spo2_scale"],
        )
    )
    assert response.status_code == 201
    assessment = response.json()["news2_assessment"]
    assert assessment["total_score"] == expected.total_score
    assert assessment["risk_level"] == expected.risk_level
    assert assessment["alert_required"] == expected.alert_required


def test_measurement_with_hd2_fields_persists_hd2_mnews_result(client_with_database):
    client, TestingSession, ids = client_with_database
    payload = valid_payload(ids)
    payload.update(
        {
            "respiratory_rate": 18,
            "spo2": 96,
            "systolic_bp": 125,
            "pulse_rate": 88,
            "temperature": 37.0,
            "vascular_access_status": "normal",
            "pre_dialysis_weight": 71.0,
            "dry_weight": 70.0,
            "session_duration_hours": 4.0,
            "fluid_to_remove": 1000.0,
            "potassium": 4.5,
            "sbp_symptomatic_hypotension": False,
        }
    )

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 201
    assessment = response.json()["news2_assessment"]
    assert assessment["hd2_mnews_total_score"] == 0
    assert assessment["hd2_mnews_risk_color"] == "green"
    assert assessment["hd2_mnews_risk_label_ar"] == "أخضر / آمن"
    assert assessment["hd2_mnews_breakdown"]["idwg_percent"] == 1.43
    assert assessment["hd2_mnews_breakdown"]["ufr"] == 3.57

    db = TestingSession()
    try:
        measurement = db.query(IntradialyticMeasurement).first()
        stored_assessment = db.query(News2Assessment).first()
        assert measurement.vascular_access_status == "normal"
        assert measurement.idwg_percent == 1.43
        assert measurement.ufr == 3.57
        assert stored_assessment.hd2_mnews_total_score == 0
        assert stored_assessment.hd2_mnews_risk_color == "green"
    finally:
        db.close()


def test_hd2_automatic_red_creates_high_priority_alert(client_with_database):
    client, _, ids = client_with_database
    payload = valid_payload(ids)
    payload.update(
        {
            "respiratory_rate": 18,
            "spo2": 91,
            "systolic_bp": 125,
            "pulse_rate": 88,
            "temperature": 37.0,
            "vascular_access_status": "normal",
            "pre_dialysis_weight": 71.0,
            "dry_weight": 70.0,
            "session_duration_hours": 4.0,
            "fluid_to_remove": 1000.0,
            "potassium": 4.5,
        }
    )

    response = client.post("/api/monitoring/measurements", json=payload)

    assert response.status_code == 201
    alert = response.json()["alert"]
    assert alert["alert_created"] is True
    assert alert["risk_level"] == "high"
    assert alert["priority"] == "immediate"
    assert alert["trigger_reason"] == "HD2-mNEWS automatic red"


def test_alert_is_created_when_monitoring_score_requires_it(client_with_database):
    client, TestingSession, ids = client_with_database

    response = client.post("/api/monitoring/measurements", json=valid_payload(ids))

    assert response.status_code == 201
    assert response.json()["alert"]["alert_created"] is True
    db = TestingSession()
    try:
        assert db.query(Alert).count() == 1
    finally:
        db.close()
