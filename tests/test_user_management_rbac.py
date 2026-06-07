from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, User
from app.rbac import ROLE_PERMISSIONS, role_has_permission


@pytest.fixture()
def user_management_client(tmp_path):
    db_path = tmp_path / "user_management.db"
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


def _staff_payload(username: str = "staff.user", email: str = "staff.user@example.local", role: str = "doctor"):
    return {
        "full_name": "Staff User",
        "username": username,
        "email": email,
        "phone": "+100000000",
        "department": "Nephrology",
        "job_title": "طبيب كلى",
        "role": role,
        "temporary_password": "temporary-secret",
        "is_active": True,
    }


def test_technical_admin_role_exists():
    assert "technical_admin" in ROLE_PERMISSIONS


def test_technical_admin_has_user_and_settings_permissions():
    assert role_has_permission("technical_admin", "users:manage")
    assert role_has_permission("technical_admin", "users:create")
    assert role_has_permission("technical_admin", "settings:manage")
    assert role_has_permission("technical_admin", "rbac:view")


def test_technical_admin_cannot_create_clinical_response(user_management_client):
    client, _ = user_management_client
    response = client.post(
        "/api/responses",
        headers={"X-Dev-Role": "technical_admin"},
        json={
            "clinical_deterioration_event_id": 1,
            "actual_response_start_time": datetime(2026, 6, 6, 10, 0, tzinfo=timezone.utc).isoformat(),
            "patient_actions": ["give_oxygen"],
            "vascular_access_actions": ["check_flow"],
        },
    )
    assert response.status_code == 403


def test_admin_can_create_staff_user(user_management_client):
    client, TestingSession = user_management_client
    response = client.post("/api/users", headers={"X-Dev-Role": "admin"}, json=_staff_payload())

    assert response.status_code == 201
    payload = response.json()
    assert payload["user_created"] is True
    assert payload["user"]["username"] == "staff.user"
    assert "password_hash" not in response.text
    assert "temporary-secret" not in response.text

    db = TestingSession()
    try:
        user = db.query(User).filter(User.username == "staff.user").one()
        assert user.password_hash != "temporary-secret"
        assert db.query(AuditLog).filter(AuditLog.action == "staff_user_created").count() == 1
    finally:
        db.close()


def test_technical_admin_can_create_staff_user(user_management_client):
    client, _ = user_management_client
    response = client.post(
        "/api/users",
        headers={"X-Dev-Role": "technical_admin"},
        json=_staff_payload("tech.created", "tech.created@example.local", "nurse"),
    )
    assert response.status_code == 201


def test_nurse_cannot_create_staff_user(user_management_client):
    client, _ = user_management_client
    response = client.post("/api/users", headers={"X-Dev-Role": "nurse"}, json=_staff_payload())
    assert response.status_code == 403


def test_doctor_cannot_access_users(user_management_client):
    client, _ = user_management_client
    response = client.get("/api/users", headers={"X-Dev-Role": "doctor"})
    assert response.status_code == 403


def test_duplicate_username_returns_conflict(user_management_client):
    client, _ = user_management_client
    payload = _staff_payload("duplicate.user", "duplicate.user@example.local")
    client.post("/api/users", headers={"X-Dev-Role": "admin"}, json=payload)
    response = client.post(
        "/api/users",
        headers={"X-Dev-Role": "admin"},
        json=_staff_payload("duplicate.user", "other@example.local"),
    )
    assert response.status_code == 409


def test_invalid_role_returns_validation_error(user_management_client):
    client, _ = user_management_client
    response = client.post("/api/users", headers={"X-Dev-Role": "admin"}, json=_staff_payload(role="superuser"))
    assert response.status_code == 422


def test_deactivate_user_endpoint_works(user_management_client):
    client, _ = user_management_client
    create_response = client.post(
        "/api/users",
        headers={"X-Dev-Role": "admin"},
        json=_staff_payload("deactivate.user", "deactivate.user@example.local"),
    )
    user_id = create_response.json()["user"]["id"]

    response = client.post(f"/api/users/{user_id}/status", headers={"X-Dev-Role": "admin"}, json={"is_active": False})
    assert response.status_code == 200
    assert response.json()["is_active"] is False
    assert response.json()["status"] == "inactive"


def test_rbac_me_supports_technical_admin(user_management_client):
    client, _ = user_management_client
    response = client.get("/api/rbac/me", headers={"X-Dev-Role": "technical_admin"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "technical_admin"
    assert "users:create" in payload["permissions"]


def test_administration_navigation_permissions_are_role_compatible():
    admin_permissions = {"users:view", "users:manage", "rbac:view", "audit:view", "settings:view"}
    assert ROLE_PERMISSIONS["admin"] & admin_permissions
    assert ROLE_PERMISSIONS["technical_admin"] & admin_permissions
    assert not ROLE_PERMISSIONS["doctor"] & admin_permissions
    assert not ROLE_PERMISSIONS["nurse"] & admin_permissions
    assert not ROLE_PERMISSIONS["researcher"] & admin_permissions
