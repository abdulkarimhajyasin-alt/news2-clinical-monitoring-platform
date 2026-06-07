from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Patient, User
from app.startup import initialize_database, seed_database_if_empty


def test_initialize_database_can_be_called_without_crashing(tmp_path):
    engine = _engine(tmp_path, "startup_basic.db")

    initialize_database(engine)

    assert "patients" in inspect(engine).get_table_names()


def test_initialize_database_creates_tables_in_empty_database(tmp_path):
    engine = _engine(tmp_path, "startup_tables.db")

    initialize_database(engine)

    table_names = set(inspect(engine).get_table_names())
    assert {"users", "patients", "alerts", "research_studies"}.issubset(table_names)


def test_initialize_database_twice_is_safe(tmp_path):
    engine = _engine(tmp_path, "startup_twice.db")

    initialize_database(engine)
    initialize_database(engine)

    assert "alerts" in inspect(engine).get_table_names()


def test_seed_flow_does_not_duplicate_data(tmp_path):
    engine = _engine(tmp_path, "startup_seed.db")
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    initialize_database(engine)

    first = seed_database_if_empty(TestingSession, auto_seed=True)
    second = seed_database_if_empty(TestingSession, auto_seed=True)

    db = TestingSession()
    try:
        assert first["status"] == "seeded"
        assert second["status"] == "already_seeded"
        assert db.query(User).count() == 5
        assert db.query(Patient).count() == 3
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_seed_flow_can_be_disabled(tmp_path):
    engine = _engine(tmp_path, "startup_seed_disabled.db")
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    initialize_database(engine)

    result = seed_database_if_empty(TestingSession, auto_seed=False)

    db = TestingSession()
    try:
        assert result["status"] == "auto_seed_disabled"
        assert db.query(User).count() == 0
        assert db.query(Patient).count() == 0
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def _engine(tmp_path, name):
    return create_engine(f"sqlite:///{tmp_path / name}", connect_args={"check_same_thread": False})
