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
    table_names = set(inspector.get_table_names())
    if "patients" not in table_names:
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

        hd2_columns_by_table = {
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
                "hd2_protocol_json": "TEXT",
                "hd2_reassessment_interval_min": "INTEGER",
                "hd2_reassessment_interval_max": "INTEGER",
                "hd2_required_response_time_minutes": "INTEGER",
                "hd2_requires_physician_call": "BOOLEAN",
                "hd2_requires_emergency_preparation": "BOOLEAN",
                "hd2_requires_close_monitoring": "BOOLEAN",
            },
        }
        for table_name, hd2_columns in hd2_columns_by_table.items():
            if table_name not in table_names:
                continue
            table_columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, sql_type in hd2_columns.items():
                if column_name not in table_columns:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sql_type}"))

        baseline_columns_by_table = {
            "patients": {
                "education_level": "VARCHAR(80)",
                "comorbid_heart_failure": "BOOLEAN",
                "comorbid_diabetes": "BOOLEAN",
                "comorbid_hypertension": "BOOLEAN",
                "comorbidities_notes": "TEXT",
                "vascular_access_type": "VARCHAR(60)",
                "vascular_access_location": "VARCHAR(120)",
                "vascular_access_placement_date": "DATE",
            },
            "dialysis_sessions": {
                "target_fluid_removal_ml": "FLOAT",
            },
        }
        for table_name, baseline_columns in baseline_columns_by_table.items():
            if table_name not in table_names:
                continue
            table_columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, sql_type in baseline_columns.items():
                if column_name not in table_columns:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sql_type}"))

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS outcome_validations_72h (
                    id INTEGER PRIMARY KEY,
                    patient_id INTEGER NOT NULL,
                    dialysis_session_id INTEGER NOT NULL,
                    deterioration_occurred BOOLEAN NOT NULL,
                    deterioration_types TEXT,
                    type_specific_details TEXT,
                    deterioration_timing_category VARCHAR(80),
                    deterioration_time VARCHAR(20),
                    deterioration_datetime TIMESTAMP,
                    platform_prediction_status VARCHAR(80),
                    interventions TEXT,
                    doctor_response_time_minutes INTEGER,
                    final_result VARCHAR(80),
                    verification_sources TEXT,
                    notes TEXT,
                    completed_by_user_id INTEGER,
                    completed_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    UNIQUE (dialysis_session_id)
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS staff_training_evaluations (
                    id INTEGER PRIMARY KEY,
                    staff_user_id INTEGER,
                    staff_name VARCHAR(160),
                    staff_role VARCHAR(40) NOT NULL,
                    study_id INTEGER,
                    training_date DATE NOT NULL,
                    pre_test_score INTEGER NOT NULL,
                    pre_test_total INTEGER NOT NULL,
                    post_test_score INTEGER NOT NULL,
                    post_test_total INTEGER NOT NULL,
                    knowledge_improvement_score INTEGER NOT NULL,
                    knowledge_improvement_percent FLOAT NOT NULL,
                    competency_items_json TEXT,
                    competency_passed BOOLEAN DEFAULT FALSE NOT NULL,
                    competency_score FLOAT NOT NULL,
                    competency_notes TEXT,
                    acceptance_survey_json TEXT,
                    acceptance_total_score INTEGER NOT NULL,
                    acceptance_mean_score FLOAT NOT NULL,
                    acceptance_level VARCHAR(40) NOT NULL,
                    general_notes TEXT,
                    created_by_user_id INTEGER,
                    updated_by_user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
                """
            )
        )
