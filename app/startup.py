from __future__ import annotations

import logging
from collections.abc import Callable

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
    logger.info("Database tables ready.")


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
