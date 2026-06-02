from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base
from app.seed import seed_database


def test_required_models_exist():
    required = [
        "User",
        "Patient",
        "PatientVascularAccess",
        "DialysisSession",
        "IntradialyticMeasurement",
        "News2Assessment",
        "Alert",
        "ClinicalDeteriorationEvent",
        "ClinicalResponse",
        "ResponseTracking",
        "ClinicalOutcome",
        "ClinicalNote",
        "ResearchStudy",
        "AuditLog",
        "SystemSetting",
    ]

    for model_name in required:
        assert hasattr(models, model_name)


def test_models_can_create_tables():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    table_names = set(Base.metadata.tables.keys())
    assert "patients" in table_names
    assert "dialysis_sessions" in table_names
    assert "news2_assessments" in table_names
    assert "alerts" in table_names


def test_seed_flow_does_not_crash_with_test_database(monkeypatch, tmp_path):
    db_path = tmp_path / "seed_test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    monkeypatch.setattr("app.database.engine", engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    try:
        result = seed_database(db)
        assert result["status"] == "seeded"
        assert db.query(models.Patient).count() == 3
        assert db.query(models.Alert).count() == 1
    finally:
        db.close()
