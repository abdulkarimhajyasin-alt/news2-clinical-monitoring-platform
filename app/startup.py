from __future__ import annotations

import logging
from collections.abc import Callable

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import Patient, User
from app.seed import seed_database


logger = logging.getLogger("news2.startup")


def initialize_database(db_engine: Engine = engine) -> None:
    from app import models  # noqa: F401

    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=db_engine)
    ensure_user_management_columns(db_engine)
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


def initialize_application_database() -> dict[str, object]:
    initialize_database()
    return seed_database_if_empty()
