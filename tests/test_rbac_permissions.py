from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog
from app.rbac import PERMISSIONS, ROLE_PERMISSIONS, role_has_permission


@pytest.fixture()
def rbac_client(tmp_path):
    db_path = tmp_path / "rbac.db"
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


def test_role_permission_matrix_contains_all_roles():
    assert set(ROLE_PERMISSIONS) == {"admin", "doctor", "on_call_doctor", "nurse", "researcher"}


def test_admin_has_all_permissions():
    assert ROLE_PERMISSIONS["admin"] == PERMISSIONS


def test_researcher_can_export():
    assert role_has_permission("researcher", "research:export")


def test_nurse_cannot_export():
    assert not role_has_permission("nurse", "research:export")


def test_nurse_cannot_create_deterioration_event():
    assert not role_has_permission("nurse", "deterioration:create")


def test_doctor_can_create_deterioration_event():
    assert role_has_permission("doctor", "deterioration:create")


def test_on_call_doctor_can_manage_alerts():
    assert role_has_permission("on_call_doctor", "alerts:manage")


def test_restricted_export_endpoint_returns_403_for_nurse(rbac_client):
    client, TestingSession = rbac_client
    response = client.get("/api/research/export/csv", headers={"X-Dev-Role": "nurse"})

    assert response.status_code == 403
    db = TestingSession()
    try:
        assert db.query(AuditLog).filter(AuditLog.action == "permission_denied").count() == 1
    finally:
        db.close()


def test_export_endpoint_succeeds_for_researcher_and_admin(rbac_client):
    client, _ = rbac_client

    researcher_response = client.get("/api/research/export/csv", headers={"X-Dev-Role": "researcher"})
    admin_response = client.get("/api/research/export/csv", headers={"X-Dev-Role": "admin"})

    assert researcher_response.status_code == 200
    assert admin_response.status_code == 200


def test_rbac_me_returns_role_and_permissions(rbac_client):
    client, _ = rbac_client
    response = client.get("/api/rbac/me", headers={"X-Dev-Role": "researcher"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "researcher"
    assert "research:export" in payload["permissions"]
    assert payload["is_dev_context"] is True


def test_invalid_dev_role_returns_safe_error(rbac_client):
    client, _ = rbac_client
    response = client.get("/api/rbac/me", headers={"X-Dev-Role": "superuser"})

    assert response.status_code == 400


def test_clinical_write_endpoint_blocks_unauthorized_role(rbac_client):
    client, _ = rbac_client
    response = client.post(
        "/api/deterioration/events",
        headers={"X-Dev-Role": "nurse"},
        json={
            "alert_id": 1,
            "deterioration_time": datetime(2026, 6, 6, 10, 0, tzinfo=timezone.utc).isoformat(),
            "deterioration_type": "acute_hypotension",
        },
    )

    assert response.status_code == 403
