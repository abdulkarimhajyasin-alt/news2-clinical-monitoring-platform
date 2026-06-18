from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import DialysisSession, IntradialyticMeasurement, News2Assessment, Patient


@pytest.fixture()
def baseline_client(tmp_path):
    db_path = tmp_path / "baseline_context.db"
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
        yield TestClient(app), TestingSession
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def baseline_patient_payload(patient_code: str = "BASE-P-1"):
    return {
        "patient_code": patient_code,
        "full_name": "Baseline Context Patient",
        "age": 64,
        "gender": "female",
        "education_level": "secondary",
        "dry_weight_kg": 68.5,
        "dialysis_start_date": "2021-03-12",
        "weekly_dialysis_sessions": 3,
        "comorbid_heart_failure": True,
        "comorbid_diabetes": True,
        "comorbid_hypertension": False,
        "comorbidities": "Diabetes mellitus; heart failure",
        "comorbidities_notes": "Doctor form baseline notes",
        "vascular_access_type": "av_fistula",
        "vascular_access_location": "left forearm",
        "vascular_access_placement_date": "2022-02-01",
        "study_phase": "post_implementation",
        "study_group": "intervention",
    }


def test_patient_create_update_read_includes_baseline_fields(baseline_client):
    client, _ = baseline_client

    create_response = client.post("/api/patients", json=baseline_patient_payload(), headers={"X-Dev-Role": "doctor"})

    assert create_response.status_code == 201
    patient = create_response.json()["patient"]
    assert patient["patient_code"] == "BASE-P-1"
    assert patient["medical_code"] == "BASE-P-1"
    assert patient["education_level"] == "secondary"
    assert patient["dry_weight_kg"] == 68.5
    assert patient["weekly_dialysis_sessions"] == 3
    assert patient["comorbid_heart_failure"] is True
    assert patient["comorbid_diabetes"] is True
    assert patient["vascular_access_type"] == "av_fistula"

    update_response = client.patch(
        f"/api/patients/{patient['id']}",
        json={"education_level": "university", "comorbid_hypertension": True, "vascular_access_location": "right upper arm"},
        headers={"X-Dev-Role": "doctor"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["education_level"] == "university"
    assert update_response.json()["comorbid_hypertension"] is True
    assert update_response.json()["vascular_access_location"] == "right upper arm"

    list_response = client.get("/api/patients", headers={"X-Dev-Role": "doctor"})
    assert list_response.status_code == 200
    listed = list_response.json()[0]
    assert listed["education_level"] == "university"
    assert listed["dry_weight_kg"] == 68.5


def test_dialysis_session_create_read_includes_context_fields(baseline_client):
    client, _ = baseline_client
    patient = client.post("/api/patients", json=baseline_patient_payload("BASE-P-2"), headers={"X-Dev-Role": "doctor"}).json()["patient"]

    response = client.post(
        "/api/dialysis-sessions",
        json={
            "patient_id": patient["id"],
            "session_date": "2026-06-18",
            "actual_start_time": "2026-06-18T08:00:00Z",
            "target_fluid_removal_ml": 2400,
            "session_duration_minutes": 240,
            "session_status": "active",
        },
        headers={"X-Dev-Role": "doctor"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["session_date"] == "2026-06-18"
    assert payload["session_day_of_week"] == "Thursday"
    assert payload["target_fluid_removal_ml"] == 2400

    list_response = client.get("/api/dialysis-sessions", headers={"X-Dev-Role": "doctor"})
    assert list_response.status_code == 200
    assert list_response.json()[0]["target_fluid_removal_ml"] == 2400


def test_research_dataset_includes_baseline_and_session_context(baseline_client):
    client, TestingSession = baseline_client
    patient = client.post("/api/patients", json=baseline_patient_payload("BASE-P-3"), headers={"X-Dev-Role": "doctor"}).json()["patient"]
    session = client.post(
        "/api/dialysis-sessions",
        json={
            "patient_id": patient["id"],
            "session_date": "2026-06-18",
            "actual_start_time": "2026-06-18T08:00:00Z",
            "target_fluid_removal_ml": 2500,
            "session_duration_minutes": 240,
            "session_status": "completed",
        },
        headers={"X-Dev-Role": "doctor"},
    ).json()
    _seed_assessment(TestingSession(), patient["id"], session["id"])

    response = client.get("/api/research/dataset", headers={"X-Dev-Role": "researcher"})

    assert response.status_code == 200
    row = response.json()[0]
    assert row["education_level"] == "secondary"
    assert row["dry_weight_kg"] == 68.5
    assert row["weekly_dialysis_sessions"] == 3
    assert row["comorbid_heart_failure"] is True
    assert row["vascular_access_type"] == "av_fistula"
    assert row["vascular_access_location"] == "left forearm"
    assert row["vascular_access_placement_date"] == "2022-02-01"
    assert row["session_day_of_week"] == "Thursday"
    assert row["target_fluid_removal_ml"] == 2500


def test_deleted_patients_remain_excluded_from_research_dataset(baseline_client):
    client, TestingSession = baseline_client
    patient = client.post("/api/patients", json=baseline_patient_payload("BASE-P-4"), headers={"X-Dev-Role": "doctor"}).json()["patient"]
    session = client.post(
        "/api/dialysis-sessions",
        json={"patient_id": patient["id"], "session_date": "2026-06-18", "target_fluid_removal_ml": 2500},
        headers={"X-Dev-Role": "doctor"},
    ).json()
    _seed_assessment(TestingSession(), patient["id"], session["id"])

    delete_response = client.post(
        f"/api/patients/{patient['id']}/delete",
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
        headers={"X-Dev-Role": "admin"},
    )
    dataset_response = client.get("/api/research/dataset", headers={"X-Dev-Role": "researcher"})

    assert delete_response.status_code == 200
    assert dataset_response.status_code == 200
    assert dataset_response.json() == []


def _seed_assessment(db, patient_id: int, session_id: int) -> None:
    measurement = IntradialyticMeasurement(
        patient_id=patient_id,
        dialysis_session_id=session_id,
        measurement_time=datetime(2026, 6, 18, 8, 30, tzinfo=timezone.utc),
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
        patient_id=patient_id,
        dialysis_session_id=session_id,
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
