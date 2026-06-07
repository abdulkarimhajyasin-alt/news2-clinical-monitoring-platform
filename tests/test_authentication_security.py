from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, AuthSession, User, UserRole
from app.security.passwords import hash_password


@pytest.fixture()
def auth_client(tmp_path, monkeypatch):
    monkeypatch.setenv("NEWS2_ALLOW_DEV_ROLE", "false")
    monkeypatch.setenv("NEWS2_SESSION_SECRET", "test-session-secret")
    get_settings.cache_clear()
    db_path = tmp_path / "auth.db"
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
    db = TestingSession()
    db.add_all(
        [
            User(
                full_name="Admin User",
                username="admin",
                email="admin@example.local",
                password_hash=hash_password("Admin@12345"),
                role=UserRole.admin,
                is_active=True,
                status="active",
            ),
            User(
                full_name="Nurse User",
                username="nurse",
                email="nurse@example.local",
                password_hash=hash_password("Nurse@12345"),
                role=UserRole.nurse,
                is_active=True,
                status="active",
            ),
            User(
                full_name="Inactive User",
                username="inactive",
                email="inactive@example.local",
                password_hash=hash_password("Inactive@12345"),
                role=UserRole.doctor,
                is_active=False,
                status="inactive",
            ),
        ]
    )
    db.commit()
    db.close()

    try:
        yield TestClient(app), TestingSession
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        get_settings.cache_clear()


def test_login_success_sets_http_only_cookie_and_returns_user(auth_client):
    client, TestingSession = auth_client
    response = client.post("/api/auth/login", json={"username_or_email": "admin", "password": "Admin@12345"})

    assert response.status_code == 200
    assert "httponly" in response.headers["set-cookie"].lower()
    assert "news2_session=" in response.headers["set-cookie"]
    payload = response.json()
    assert payload["username"] == "admin"
    assert payload["role"] == "admin"
    assert "users:create" in payload["permissions"]
    assert "password_hash" not in response.text

    db = TestingSession()
    try:
        assert db.query(AuthSession).count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "auth_login_success").count() == 1
    finally:
        db.close()


def test_login_failed_writes_audit_without_session(auth_client):
    client, TestingSession = auth_client
    response = client.post("/api/auth/login", json={"username_or_email": "admin", "password": "wrong-pass"})

    assert response.status_code == 401
    db = TestingSession()
    try:
        assert db.query(AuthSession).count() == 0
        assert db.query(AuditLog).filter(AuditLog.action == "auth_login_failed").count() == 1
    finally:
        db.close()


def test_inactive_user_cannot_login(auth_client):
    client, _ = auth_client
    response = client.post("/api/auth/login", json={"username_or_email": "inactive", "password": "Inactive@12345"})

    assert response.status_code == 403


def test_me_requires_session_and_protected_reads_reject_anonymous(auth_client):
    client, TestingSession = auth_client
    me_response = client.get("/api/auth/me")
    patients_response = client.get("/api/patients")

    assert me_response.status_code == 401
    assert patients_response.status_code == 401
    db = TestingSession()
    try:
        assert db.query(AuditLog).filter(AuditLog.action == "auth_unauthorized_access").count() >= 1
    finally:
        db.close()


def test_authenticated_session_allows_protected_read(auth_client):
    client, _ = auth_client
    client.post("/api/auth/login", json={"username_or_email": "admin", "password": "Admin@12345"})

    response = client.get("/api/patients")

    assert response.status_code == 200
    assert response.json() == []


def test_logout_deletes_session_and_clears_cookie(auth_client):
    client, TestingSession = auth_client
    client.post("/api/auth/login", json={"username_or_email": "admin", "password": "Admin@12345"})

    response = client.post("/api/auth/logout")

    assert response.status_code == 200
    assert "news2_session=" in response.headers["set-cookie"]
    db = TestingSession()
    try:
        assert db.query(AuthSession).count() == 0
        assert db.query(AuditLog).filter(AuditLog.action == "auth_logout").count() == 1
    finally:
        db.close()


def test_frontend_role_header_is_ignored_when_dev_role_disabled(auth_client):
    client, _ = auth_client
    response = client.get("/api/rbac/me", headers={"X-Dev-Role": "admin"})

    assert response.status_code == 401


def test_authenticated_user_role_controls_rbac_not_header(auth_client):
    client, _ = auth_client
    client.post("/api/auth/login", json={"username_or_email": "nurse", "password": "Nurse@12345"})

    response = client.post("/api/users", headers={"X-Dev-Role": "admin"}, json={})

    assert response.status_code == 403


def test_dev_role_header_is_available_only_when_enabled(auth_client, monkeypatch):
    client, _ = auth_client
    monkeypatch.setenv("NEWS2_ALLOW_DEV_ROLE", "true")
    get_settings.cache_clear()

    response = client.get("/api/rbac/me", headers={"X-Dev-Role": "technical_admin"})

    assert response.status_code == 200
    assert response.json()["role"] == "technical_admin"
    assert response.json()["is_dev_context"] is True


def test_production_frontend_does_not_send_role_header_by_default():
    source = Path("app/static/app.js").read_text(encoding="utf-8")

    assert '"X-Dev-Role": appState.currentRole || "admin"' not in source
    assert "appState.allowDevRole && appState.currentRole" in source
