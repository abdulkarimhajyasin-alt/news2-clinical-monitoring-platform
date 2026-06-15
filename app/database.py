from collections.abc import Generator
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _connect_args(database_url: str) -> dict[str, object]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


settings = get_settings()
engine = create_engine(
    settings.database_url,
    connect_args=_connect_args(settings.database_url),
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    ensure_runtime_columns()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_runtime_columns()


def ensure_runtime_columns() -> None:
    inspector = inspect(engine)
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
    with engine.begin() as connection:
        for column_name, sql_type in column_sql.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE patients ADD COLUMN {column_name} {sql_type}"))
        connection.execute(text("UPDATE patients SET status = 'active' WHERE status IS NULL OR status = ''"))
