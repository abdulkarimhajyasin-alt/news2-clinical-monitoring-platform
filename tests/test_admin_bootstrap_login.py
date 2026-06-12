import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database import Base, get_db
from app.main import app
from app.models import User, UserRole
from app.security.passwords import hash_password, verify_password
from app.startup import ensure_default_admin_user


@pytest.fixture()
def admin_bootstrap_context(tmp_path, monkeypatch):
    monkeypatch.setenv("NEWS2_DEFAULT_ADMIN_USERNAME", "admin")
    monkeypatch.setenv("NEWS2_DEFAULT_ADMIN_PASSWORD", "Admin@12345")
    monkeypatch.setenv("NEWS2_FORCE_ADMIN_PASSWORD_RESET", "false")
    monkeypatch.setenv("NEWS2_SESSION_SECRET", "test-session-secret")
    monkeypatch.setenv("NEWS2_ALLOW_DEV_ROLE", "false")
    get_settings.cache_clear()

    engine = create_engine(f"sqlite:///{tmp_path / 'admin_bootstrap.db'}", connect_args={"check_same_thread": False})
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
        yield TestingSession, TestClient(app), monkeypatch
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        get_settings.cache_clear()


def test_no_admin_exists_creates_active_admin(admin_bootstrap_context):
    TestingSession, _client, _monkeypatch = admin_bootstrap_context

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_created"
        assert admin.role == UserRole.admin
        assert admin.is_active is True
        assert admin.status == "active"
        assert verify_password("Admin@12345", admin.password_hash)
    finally:
        db.close()


def test_existing_admin_with_missing_password_hash_is_repaired(admin_bootstrap_context):
    TestingSession, _client, _monkeypatch = admin_bootstrap_context
    _add_user(TestingSession, password_hash="")

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_repaired"
        assert "password_hash" in result["repaired_fields"]
        assert verify_password("Admin@12345", admin.password_hash)
    finally:
        db.close()


def test_existing_inactive_admin_is_activated(admin_bootstrap_context):
    TestingSession, _client, _monkeypatch = admin_bootstrap_context
    _add_user(TestingSession, is_active=False, status="inactive")

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_repaired"
        assert admin.is_active is True
        assert admin.status == "active"
    finally:
        db.close()


def test_existing_non_admin_role_is_repaired(admin_bootstrap_context):
    TestingSession, _client, _monkeypatch = admin_bootstrap_context
    _add_user(TestingSession, role=UserRole.nurse)

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_repaired"
        assert admin.role == UserRole.admin
    finally:
        db.close()


def test_existing_valid_admin_password_is_not_overwritten_without_force_reset(admin_bootstrap_context):
    TestingSession, _client, _monkeypatch = admin_bootstrap_context
    existing_hash = hash_password("CustomAdmin@12345")
    _add_user(TestingSession, password_hash=existing_hash)

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_usable"
        assert admin.password_hash == existing_hash
        assert verify_password("CustomAdmin@12345", admin.password_hash)
    finally:
        db.close()


def test_force_reset_updates_admin_password_hash(admin_bootstrap_context):
    TestingSession, _client, monkeypatch = admin_bootstrap_context
    existing_hash = hash_password("CustomAdmin@12345")
    _add_user(TestingSession, password_hash=existing_hash)
    monkeypatch.setenv("NEWS2_FORCE_ADMIN_PASSWORD_RESET", "true")
    get_settings.cache_clear()

    result = ensure_default_admin_user(TestingSession)

    db = TestingSession()
    try:
        admin = db.query(User).filter(User.username == "admin").one()
        assert result["status"] == "admin_repaired"
        assert admin.password_hash != existing_hash
        assert verify_password("Admin@12345", admin.password_hash)
        assert not verify_password("CustomAdmin@12345", admin.password_hash)
    finally:
        db.close()


def test_login_succeeds_after_bootstrap(admin_bootstrap_context):
    TestingSession, client, _monkeypatch = admin_bootstrap_context
    _add_user(TestingSession, password_hash="not-for-auth-phase", role=UserRole.nurse, is_active=False, status="inactive")

    ensure_default_admin_user(TestingSession)
    response = client.post("/api/auth/login", json={"username_or_email": "admin", "password": "Admin@12345"})

    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert response.json()["role"] == "admin"


def test_password_hash_is_never_returned_after_bootstrap_login(admin_bootstrap_context):
    TestingSession, client, _monkeypatch = admin_bootstrap_context
    ensure_default_admin_user(TestingSession)

    response = client.post("/api/auth/login", json={"username_or_email": "admin", "password": "Admin@12345"})

    assert response.status_code == 200
    assert "password_hash" not in response.text


def _add_user(
    TestingSession,
    *,
    password_hash: str | None = None,
    role: str = UserRole.admin,
    is_active: bool = True,
    status: str = "active",
) -> None:
    db = TestingSession()
    try:
        db.add(
            User(
                full_name="Existing Admin",
                username="admin",
                email="admin@example.local",
                password_hash=hash_password("Admin@12345") if password_hash is None else password_hash,
                role=role,
                is_active=is_active,
                status=status,
            )
        )
        db.commit()
    finally:
        db.close()
