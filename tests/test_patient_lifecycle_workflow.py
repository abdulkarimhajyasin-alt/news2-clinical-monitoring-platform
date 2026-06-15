from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, DialysisSession, Patient


@pytest.fixture()
def lifecycle_client(tmp_path):
    db_path = tmp_path / "patient_lifecycle.db"
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
    _seed_patients(TestingSession)
    try:
        yield TestClient(app), TestingSession
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_discharge_active_patient(lifecycle_client):
    client, _ = lifecycle_client

    response = client.post(
        "/api/patients/1/discharge",
        headers={"X-Dev-Role": "doctor"},
        json={"discharge_reason": "Transferred to another unit", "discharge_notes": "Stable at discharge."},
    )

    assert response.status_code == 200
    payload = response.json()["patient"]
    assert payload["status"] == "discharged"
    assert payload["discharge_reason"] == "Transferred to another unit"
    assert payload["discharged_at"] is not None


def test_discharged_patient_is_hidden_from_default_patient_list(lifecycle_client):
    client, _ = lifecycle_client
    client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})

    response = client.get("/api/patients", headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 200
    assert [row["patient_code"] for row in response.json()] == ["LIFE-P-2", "LIFE-P-3"]


def test_status_filter_shows_discharged_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})

    response = client.get("/api/patients?status=discharged", headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 200
    assert [row["patient_code"] for row in response.json()] == ["LIFE-P-1"]


def test_archive_patient(lifecycle_client):
    client, _ = lifecycle_client

    response = client.post("/api/patients/2/archive", headers={"X-Dev-Role": "technical_admin"}, json={})

    assert response.status_code == 200
    patient = response.json()["patient"]
    assert patient["status"] == "archived"
    assert patient["archived_at"] is not None


def test_doctor_can_restore_archived_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post("/api/patients/1/archive", headers={"X-Dev-Role": "admin"}, json={})

    response = client.post("/api/patients/1/restore", headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 200
    assert response.json()["patient"]["status"] == "active"


def test_doctor_cannot_restore_deleted_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    response = client.post("/api/patients/1/restore", headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 403


def test_doctor_cannot_restore_discharged_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})

    response = client.post("/api/patients/1/restore", headers={"X-Dev-Role": "doctor"})

    assert response.status_code == 403


def test_admin_can_restore_deleted_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    response = client.post("/api/patients/1/restore", headers={"X-Dev-Role": "admin"})

    assert response.status_code == 200
    assert response.json()["patient"]["status"] == "active"


def test_technical_admin_can_restore_deleted_patient(lifecycle_client):
    client, _ = lifecycle_client
    client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    response = client.post("/api/patients/1/restore", headers={"X-Dev-Role": "technical_admin"})

    assert response.status_code == 200
    assert response.json()["patient"]["status"] == "active"


def test_soft_delete_requires_admin_permission(lifecycle_client):
    client, _ = lifecycle_client

    response = client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "doctor"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    assert response.status_code == 403


def test_doctor_can_discharge_but_cannot_delete(lifecycle_client):
    client, _ = lifecycle_client

    discharge = client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})
    delete = client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "doctor"},
        json={"delete_reason": "Duplicate", "confirmation_text": "DELETE PATIENT"},
    )

    assert discharge.status_code == 200
    assert delete.status_code == 403


def test_nurse_cannot_discharge_or_delete(lifecycle_client):
    client, _ = lifecycle_client

    discharge = client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "nurse"}, json={"discharge_reason": "Completed"})
    delete = client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "nurse"},
        json={"delete_reason": "Duplicate", "confirmation_text": "DELETE PATIENT"},
    )

    assert discharge.status_code == 403
    assert delete.status_code == 403


def test_delete_requires_confirmation_text(lifecycle_client):
    client, _ = lifecycle_client

    response = client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "wrong"},
    )

    assert response.status_code == 400


def test_admin_soft_delete_hides_patient_from_default_list_and_can_include_deleted(lifecycle_client):
    client, _ = lifecycle_client
    delete_response = client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    default_response = client.get("/api/patients", headers={"X-Dev-Role": "admin"})
    deleted_response = client.get("/api/patients?status=deleted&include_deleted=true", headers={"X-Dev-Role": "admin"})

    assert delete_response.status_code == 200
    assert delete_response.json()["patient"]["status"] == "deleted"
    assert "LIFE-P-1" not in [row["patient_code"] for row in default_response.json()]
    assert [row["patient_code"] for row in deleted_response.json()] == ["LIFE-P-1"]


def test_audit_logs_created(lifecycle_client):
    client, TestingSession = lifecycle_client
    client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})
    client.post("/api/patients/1/restore", headers={"X-Dev-Role": "admin"})
    client.post("/api/patients/1/archive", headers={"X-Dev-Role": "technical_admin"}, json={})
    client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate", "confirmation_text": "DELETE PATIENT"},
    )

    db = TestingSession()
    try:
        actions = {row.action for row in db.query(AuditLog).filter(AuditLog.entity_type == "patient").all()}
        assert {"patient_discharged", "patient_restored", "patient_archived", "patient_soft_deleted"}.issubset(actions)
    finally:
        db.close()


def test_research_summary_does_not_crash_with_discharged_archived_patients(lifecycle_client):
    client, _ = lifecycle_client
    client.post("/api/patients/1/discharge", headers={"X-Dev-Role": "doctor"}, json={"discharge_reason": "Completed"})
    client.post("/api/patients/2/archive", headers={"X-Dev-Role": "technical_admin"}, json={})

    response = client.get("/api/research/summary", headers={"X-Dev-Role": "researcher"})

    assert response.status_code == 200
    assert response.json()["patients_count"] == 3


def _seed_patients(TestingSession):
    db = TestingSession()
    try:
        patients = [
            Patient(patient_code="LIFE-P-1", full_name="Lifecycle One", age=61, gender="female", study_phase="post_implementation", study_group="intervention", is_anonymized=True),
            Patient(patient_code="LIFE-P-2", full_name="Lifecycle Two", age=55, gender="male", study_phase="post_implementation", study_group="intervention", is_anonymized=True),
            Patient(patient_code="LIFE-P-3", full_name="Lifecycle Three", age=48, gender="female", study_phase="pre_implementation", study_group="control", is_anonymized=True),
        ]
        db.add_all(patients)
        db.flush()
        db.add(DialysisSession(patient_id=patients[0].id, session_date=date(2026, 6, 6), actual_start_time=datetime(2026, 6, 6, 8, 0, tzinfo=timezone.utc), session_status="completed"))
        db.commit()
    finally:
        db.close()
