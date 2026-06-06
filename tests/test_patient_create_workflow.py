from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import DialysisSession, IntradialyticMeasurement, News2Assessment, Patient


@pytest.fixture()
def patient_client(tmp_path):
    db_path = tmp_path / "patient_create.db"
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


def test_create_patient_succeeds(patient_client):
    client, _, _ = patient_client

    response = client.post("/api/patients", json=_patient_payload("CREATE-P-1"), headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["patient_created"] is True
    assert payload["patient"]["patient_code"] == "CREATE-P-1"


def test_created_patient_appears_in_patient_list(patient_client):
    client, _, _ = patient_client
    client.post("/api/patients", json=_patient_payload("CREATE-P-2"), headers={"X-Dev-Role": "doctor"})

    response = client.get("/api/patients")

    assert response.status_code == 200
    assert any(row["patient_code"] == "CREATE-P-2" for row in response.json())


def test_duplicate_patient_code_returns_409(patient_client):
    client, _, _ = patient_client
    payload = _patient_payload("DUP-P-1")
    client.post("/api/patients", json=payload, headers={"X-Dev-Role": "doctor"})

    response = client.post("/api/patients", json=payload, headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 409


def test_invalid_patient_payload_returns_422(patient_client):
    client, _, _ = patient_client

    response = client.post("/api/patients", json={"patient_code": "BAD"}, headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 422


def test_nurse_cannot_create_patient(patient_client):
    client, _, _ = patient_client

    response = client.post("/api/patients", json=_patient_payload("NURSE-P-1"), headers={"X-Dev-Role": "nurse"})

    assert response.status_code == 403


def test_doctor_and_admin_can_create_patient(patient_client):
    client, _, _ = patient_client

    doctor_response = client.post("/api/patients", json=_patient_payload("DOC-P-1"), headers={"X-Dev-Role": "doctor"})
    admin_response = client.post("/api/patients", json=_patient_payload("ADMIN-P-1"), headers={"X-Dev-Role": "admin"})

    assert doctor_response.status_code == 201
    assert admin_response.status_code == 201


def test_research_export_excludes_patient_full_name(patient_client):
    client, TestingSession, _ = patient_client
    response = client.post("/api/patients", json=_patient_payload("PRIVATE-P-1", full_name="Sensitive Created Patient"), headers={"X-Dev-Role": "doctor"})
    patient_id = response.json()["patient"]["id"]
    _seed_assessment_for_patient(TestingSession(), patient_id)

    export_response = client.get("/api/research/export/csv", headers={"X-Dev-Role": "researcher"})

    assert export_response.status_code == 200
    assert "PRIVATE-P-1" in export_response.text
    assert "Sensitive Created Patient" not in export_response.text
    assert "full_name" not in export_response.text


def _patient_payload(patient_code: str, full_name: str = "Created Test Patient"):
    return {
        "patient_code": patient_code,
        "full_name": full_name,
        "age": 62,
        "gender": "female",
        "weekly_sessions_count": 3,
        "comorbidities": "Hypertension",
        "study_phase": "post_implementation",
        "study_group": "intervention",
        "is_anonymized": True,
    }


def _seed_assessment_for_patient(db, patient_id: int):
    patient = db.get(Patient, patient_id)
    session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 6),
        actual_start_time=datetime(2026, 6, 6, 8, 0, tzinfo=timezone.utc),
        session_status="completed",
    )
    db.add(session)
    db.flush()
    measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 6, 8, 30, tzinfo=timezone.utc),
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
