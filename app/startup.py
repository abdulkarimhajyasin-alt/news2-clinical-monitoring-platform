from __future__ import annotations

import logging
from collections.abc import Callable

from sqlalchemy import inspect, or_, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import Patient, User, UserRole
from app.seed import seed_database
from app.security.passwords import hash_password, is_password_hash_usable


logger = logging.getLogger("news2.startup")


def initialize_database(db_engine: Engine = engine) -> None:
    from app import models  # noqa: F401

    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=db_engine)
    ensure_user_management_columns(db_engine)
    ensure_patient_lifecycle_columns(db_engine)
    ensure_hd2_mnews_columns(db_engine)
    logger.info("Database tables ready.")


def ensure_user_management_columns(db_engine: Engine = engine) -> None:
    inspector = inspect(db_engine)
    if "users" not in inspector.get_table_names():
        return
    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    column_sql = {
        "username": "VARCHAR(80)",
        "job_title": "VARCHAR(120)",
        "is_active": "BOOLEAN DEFAULT TRUE NOT NULL",
    }
    with db_engine.begin() as connection:
        for column_name, sql_type in column_sql.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {sql_type}"))
        connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username)"))


def ensure_patient_lifecycle_columns(db_engine: Engine = engine) -> None:
    inspector = inspect(db_engine)
    if "patients" not in inspector.get_table_names():
        return
    existing_columns = {column["name"] for column in inspector.get_columns("patients")}
    column_sql = {
        "status": "VARCHAR(40) DEFAULT 'active' NOT NULL",
        "discharged_at": "TIMESTAMP",
        "discharge_reason": "VARCHAR(255)",
        "discharge_notes": "TEXT",
        "archived_at": "TIMESTAMP",
        "archived_by_user_id": "INTEGER",
        "deleted_at": "TIMESTAMP",
        "deleted_by_user_id": "INTEGER",
        "delete_reason": "TEXT",
    }
    with db_engine.begin() as connection:
        for column_name, sql_type in column_sql.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE patients ADD COLUMN {column_name} {sql_type}"))
        connection.execute(text("UPDATE patients SET status = 'active' WHERE status IS NULL OR status = ''"))


def ensure_hd2_mnews_columns(db_engine: Engine = engine) -> None:
    inspector = inspect(db_engine)
    table_names = set(inspector.get_table_names())
    column_sql_by_table = {
        "intradialytic_measurements": {
            "vascular_access_status": "VARCHAR(40)",
            "pre_dialysis_weight": "FLOAT",
            "dry_weight": "FLOAT",
            "session_duration_hours": "FLOAT",
            "fluid_to_remove": "FLOAT",
            "potassium": "FLOAT",
            "idwg_percent": "FLOAT",
            "ufr": "FLOAT",
            "sbp_symptomatic_hypotension": "BOOLEAN DEFAULT FALSE NOT NULL",
        },
        "news2_assessments": {
            "hd2_mnews_total_score": "INTEGER",
            "hd2_mnews_risk_color": "VARCHAR(40)",
            "hd2_mnews_risk_label_ar": "VARCHAR(80)",
            "hd2_mnews_critical_trigger": "BOOLEAN",
            "hd2_mnews_critical_reasons": "TEXT",
            "hd2_mnews_breakdown_json": "TEXT",
        },
    }
    with db_engine.begin() as connection:
        for table_name, column_sql in column_sql_by_table.items():
            if table_name not in table_names:
                continue
            existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, sql_type in column_sql.items():
                if column_name not in existing_columns:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sql_type}"))


def seed_database_if_empty(
    session_factory: Callable[[], Session] | sessionmaker[Session] = SessionLocal,
    *,
    auto_seed: bool | None = None,
) -> dict[str, object]:
    should_seed = get_settings().auto_seed if auto_seed is None else auto_seed
    if not should_seed:
        logger.info("Automatic seed disabled.")
        return {"status": "auto_seed_disabled"}

    logger.info("Checking seed data...")
    db = session_factory()
    try:
        users_count = db.query(User).count()
        patients_count = db.query(Patient).count()
        if users_count or patients_count:
            logger.info("Seed data already exists.")
            return {
                "status": "already_seeded",
                "users": users_count,
                "patients": patients_count,
            }
        result = seed_database(db, ensure_schema=False)
        logger.info("Seed data created.")
        return result
    finally:
        db.close()


def ensure_initial_admin(
    session_factory: Callable[[], Session] | sessionmaker[Session] = SessionLocal,
) -> dict[str, object]:
    return ensure_default_admin_user(session_factory)


def ensure_default_admin_user(
    session_factory: Callable[[], Session] | sessionmaker[Session] = SessionLocal,
) -> dict[str, object]:
    settings = get_settings()
    username = settings.default_admin_username.strip().lower()
    admin_email = f"{username}@example.local"
    default_password = settings.default_admin_password
    if not username:
        raise ValueError("NEWS2_DEFAULT_ADMIN_USERNAME must not be empty")
    if not default_password:
        raise ValueError("NEWS2_DEFAULT_ADMIN_PASSWORD must not be empty")

    logger.info("Ensuring default admin user...")
    db = session_factory()
    try:
        existing_admin = db.query(User).filter(or_(User.username == username, User.email == admin_email)).first()
        if existing_admin:
            repaired_fields: list[str] = []
            if existing_admin.username != username:
                existing_admin.username = username
                repaired_fields.append("username")
            if existing_admin.role != UserRole.admin:
                existing_admin.role = UserRole.admin
                repaired_fields.append("role")
            if not existing_admin.is_active:
                existing_admin.is_active = True
                repaired_fields.append("is_active")
            if existing_admin.status != "active":
                existing_admin.status = "active"
                repaired_fields.append("status")
            if settings.force_admin_password_reset or not is_password_hash_usable(existing_admin.password_hash):
                existing_admin.password_hash = hash_password(default_password)
                repaired_fields.append("password_hash")
            if repaired_fields:
                db.commit()
                db.refresh(existing_admin)
                logger.info("Default admin repaired for staging login.")
                return {
                    "status": "admin_repaired",
                    "admin_id": existing_admin.id,
                    "repaired_fields": repaired_fields,
                }
            logger.info("Default admin already usable.")
            return {"status": "admin_usable", "admin_id": existing_admin.id}
        admin = User(
            full_name="System Administrator",
            username=username,
            email=admin_email,
            password_hash=hash_password(default_password),
            role=UserRole.admin,
            department="Information Technology",
            job_title="Platform Administrator",
            is_active=True,
            status="active",
            preferred_language="ar",
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info("Default admin created.")
        return {"status": "admin_created", "admin_id": admin.id}
    finally:
        db.close()


def initialize_application_database() -> dict[str, object]:
    initialize_database()
    seed_result = seed_database_if_empty()
    admin_result = ensure_initial_admin()
    return {"seed": seed_result, "admin": admin_result}
