from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import AuditLog, StaffTrainingEvaluation, User, UserRole
from app.services.training_evaluation_service import (
    DEFAULT_ACCEPTANCE_SURVEY_ITEMS,
    DEFAULT_COMPETENCY_ITEMS,
    TrainingEvaluationValidationError,
    calculate_acceptance_score,
    calculate_knowledge_metrics,
    evaluate_competency,
)


def test_knowledge_metrics_calculate_improvement():
    metrics = calculate_knowledge_metrics(5, 10, 8, 10)

    assert metrics["pre_test_percent"] == 50.0
    assert metrics["post_test_percent"] == 80.0
    assert metrics["knowledge_improvement_score"] == 3
    assert metrics["knowledge_improvement_percent"] == 60.0


def test_score_validation_rejects_score_above_total():
    with pytest.raises(TrainingEvaluationValidationError):
        calculate_knowledge_metrics(11, 10, 8, 10)


def test_competency_pass_and_fail():
    passed = evaluate_competency({key: True for key in DEFAULT_COMPETENCY_ITEMS})
    failed = evaluate_competency({"news2_components": True})

    assert passed["competency_passed"] is True
    assert passed["competency_score"] == 100.0
    assert failed["competency_passed"] is False
    assert failed["competency_score"] == 20.0


def test_acceptance_levels():
    assert calculate_acceptance_score({key: 5 for key in DEFAULT_ACCEPTANCE_SURVEY_ITEMS})["acceptance_level"] == "high"
    assert calculate_acceptance_score({key: 3 for key in DEFAULT_ACCEPTANCE_SURVEY_ITEMS})["acceptance_level"] == "medium"
    assert calculate_acceptance_score({key: 2 for key in DEFAULT_ACCEPTANCE_SURVEY_ITEMS})["acceptance_level"] == "low"


@pytest.fixture()
def training_client(tmp_path):
    db_path = tmp_path / "training.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    db.add(User(full_name="Training Doctor", email="training@example.local", password_hash="x", role=UserRole.doctor))
    db.commit()
    db.close()

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


def test_training_api_create_list_update_summary_and_export(training_client):
    client, TestingSession = training_client
    payload = _training_payload()

    create_response = client.post("/api/training/evaluations", json=payload)

    assert create_response.status_code == 201
    created = create_response.json()["evaluation"]
    assert created["knowledge_improvement_score"] == 4
    assert created["competency_passed"] is True
    assert created["acceptance_level"] == "high"

    list_response = client.get("/api/training/evaluations")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    updated_payload = {**payload, "post_test_score": 7, "updated_by_user_id": 1}
    update_response = client.put(f"/api/training/evaluations/{created['id']}", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["evaluation"]["knowledge_improvement_score"] == 2

    summary_response = client.get("/api/training/summary")
    assert summary_response.status_code == 200
    assert summary_response.json()["total_evaluated_staff"] == 1
    assert summary_response.json()["competency_pass_rate_percent"] == 100.0

    export_response = client.get("/api/training/export/csv")
    assert export_response.status_code == 200
    assert "staff_role" in export_response.text
    assert "knowledge_improvement_percent" in export_response.text

    db = TestingSession()
    try:
        assert db.query(StaffTrainingEvaluation).count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "staff_training_evaluation_created").count() == 1
        assert db.query(AuditLog).filter(AuditLog.action == "staff_training_evaluation_updated").count() == 1
    finally:
        db.close()


def test_training_api_rejects_invalid_scores(training_client):
    client, _ = training_client
    payload = _training_payload(pre_test_score=12, pre_test_total=10)

    response = client.post("/api/training/evaluations", json=payload)

    assert response.status_code == 400


def test_training_api_requires_permissions(training_client):
    client, _ = training_client

    create_response = client.post("/api/training/evaluations", json=_training_payload(), headers={"X-Dev-Role": "nurse"})
    view_response = client.get("/api/training/summary", headers={"X-Dev-Role": "nurse"})

    assert create_response.status_code == 403
    assert view_response.status_code == 403


def _training_payload(**overrides):
    payload = {
        "staff_name": "Nurse A",
        "staff_role": "nurse",
        "training_date": date(2026, 6, 19).isoformat(),
        "pre_test_score": 5,
        "pre_test_total": 10,
        "post_test_score": 9,
        "post_test_total": 10,
        "competency_items": {key: True for key in DEFAULT_COMPETENCY_ITEMS},
        "competency_notes": "Passed practical checklist.",
        "acceptance_survey": {key: 5 for key in DEFAULT_ACCEPTANCE_SURVEY_ITEMS},
        "general_notes": "Ready for supervised use.",
        "created_by_user_id": 1,
    }
    payload.update(overrides)
    return payload
