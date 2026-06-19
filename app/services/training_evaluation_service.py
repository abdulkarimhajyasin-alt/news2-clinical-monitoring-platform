from __future__ import annotations

import csv
import io
import json
from collections import Counter
from datetime import date

from sqlalchemy.orm import Session

from app.models import AuditLog, ResearchStudy, StaffTrainingEvaluation, User
from app.schemas import StaffTrainingEvaluationCreate, StaffTrainingEvaluationUpdate


DEFAULT_COMPETENCY_ITEMS: dict[str, str] = {
    "news2_components": "تحديد مكونات NEWS2 بشكل صحيح",
    "hd2_mnews_color": "تفسير لون خطورة HD2-MNEWS",
    "vital_signs_entry": "إدخال العلامات الحيوية دون أخطاء",
    "nursing_protocol": "اتباع بروتوكول التمريض حسب اللون",
    "escalation_documentation": "توثيق التصعيد والاستجابة",
}

DEFAULT_ACCEPTANCE_SURVEY_ITEMS: dict[str, str] = {
    "ease_of_use": "سهولة استخدام المنصة",
    "workflow_fit": "ملاءمة النظام لسير العمل",
    "clinical_confidence": "زيادة الثقة في التقييم السريري",
    "alert_usefulness": "فائدة التنبيهات في التصعيد",
    "training_satisfaction": "الرضا عن التدريب",
}

ACCEPTANCE_LEVEL_LABELS_AR = {
    "low": "قبول منخفض",
    "medium": "قبول متوسط",
    "high": "قبول مرتفع",
}

TRAINING_EXPORT_FIELDS = [
    "id",
    "staff_name",
    "staff_role",
    "training_date",
    "pre_test_percent",
    "post_test_percent",
    "knowledge_improvement_score",
    "knowledge_improvement_percent",
    "competency_passed",
    "competency_score",
    "acceptance_mean_score",
    "acceptance_level",
]


class TrainingEvaluationError(Exception):
    pass


class TrainingEvaluationNotFoundError(TrainingEvaluationError):
    pass


class TrainingEvaluationValidationError(TrainingEvaluationError):
    pass


class TrainingEvaluationTraceabilityError(TrainingEvaluationError):
    pass


def calculate_knowledge_metrics(pre_score: int, pre_total: int, post_score: int, post_total: int) -> dict[str, float | int]:
    _validate_score("pre_test", pre_score, pre_total)
    _validate_score("post_test", post_score, post_total)
    pre_percent = round((pre_score / pre_total) * 100, 1)
    post_percent = round((post_score / post_total) * 100, 1)
    improvement_score = post_score - pre_score
    if pre_score > 0:
        improvement_percent = round((improvement_score / pre_score) * 100, 1)
    else:
        improvement_percent = 100.0 if post_score > 0 else 0.0
    return {
        "pre_test_percent": pre_percent,
        "post_test_percent": post_percent,
        "knowledge_improvement_score": improvement_score,
        "knowledge_improvement_percent": improvement_percent,
    }


def evaluate_competency(items: dict[str, bool] | None) -> dict[str, object]:
    normalized = {key: bool((items or {}).get(key, False)) for key in DEFAULT_COMPETENCY_ITEMS}
    completed = sum(1 for passed in normalized.values() if passed)
    total = len(DEFAULT_COMPETENCY_ITEMS)
    score = round((completed / total) * 100, 1) if total else 0.0
    return {
        "competency_items": normalized,
        "competency_passed": completed == total and score >= 80,
        "competency_score": score,
    }


def calculate_acceptance_score(survey: dict[str, int] | None) -> dict[str, object]:
    normalized: dict[str, int] = {}
    for key in DEFAULT_ACCEPTANCE_SURVEY_ITEMS:
        value = int((survey or {}).get(key, 0))
        if value < 1 or value > 5:
            raise TrainingEvaluationValidationError(f"Acceptance survey item '{key}' must be between 1 and 5")
        normalized[key] = value
    total = sum(normalized.values())
    mean = round(total / len(DEFAULT_ACCEPTANCE_SURVEY_ITEMS), 2) if DEFAULT_ACCEPTANCE_SURVEY_ITEMS else 0.0
    if mean >= 4:
        level = "high"
    elif mean >= 3:
        level = "medium"
    else:
        level = "low"
    return {
        "acceptance_survey": normalized,
        "acceptance_total_score": total,
        "acceptance_mean_score": mean,
        "acceptance_level": level,
    }


def list_training_evaluations(db: Session, study_id: int | None = None, staff_user_id: int | None = None, limit: int = 200) -> list[dict[str, object]]:
    query = db.query(StaffTrainingEvaluation)
    if study_id is not None:
        query = query.filter(StaffTrainingEvaluation.study_id == study_id)
    if staff_user_id is not None:
        query = query.filter(StaffTrainingEvaluation.staff_user_id == staff_user_id)
    rows = query.order_by(StaffTrainingEvaluation.training_date.desc(), StaffTrainingEvaluation.id.desc()).limit(limit).all()
    return [training_to_dict(row) for row in rows]


def get_training_evaluation(db: Session, evaluation_id: int) -> dict[str, object]:
    evaluation = db.get(StaffTrainingEvaluation, evaluation_id)
    if evaluation is None:
        raise TrainingEvaluationNotFoundError("Training evaluation not found")
    return training_to_dict(evaluation)


def create_training_evaluation(db: Session, payload: StaffTrainingEvaluationCreate) -> dict[str, object]:
    _validate_references(db, payload)
    evaluation = _payload_to_model(payload)
    db.add(evaluation)
    db.flush()
    _create_audit_log(db, "staff_training_evaluation_created", evaluation, payload.created_by_user_id)
    db.commit()
    db.refresh(evaluation)
    return {
        "evaluation": training_to_dict(evaluation),
        "evaluation_created": True,
        "message": "Staff training evaluation created successfully",
    }


def update_training_evaluation(db: Session, evaluation_id: int, payload: StaffTrainingEvaluationUpdate) -> dict[str, object]:
    evaluation = db.get(StaffTrainingEvaluation, evaluation_id)
    if evaluation is None:
        raise TrainingEvaluationNotFoundError("Training evaluation not found")
    _validate_references(db, payload)
    updated = _payload_to_model(payload, evaluation)
    _create_audit_log(db, "staff_training_evaluation_updated", updated, payload.updated_by_user_id or payload.created_by_user_id)
    db.commit()
    db.refresh(updated)
    return {
        "evaluation": training_to_dict(updated),
        "evaluation_created": False,
        "message": "Staff training evaluation updated successfully",
    }


def build_training_summary(db: Session) -> dict[str, object]:
    rows = db.query(StaffTrainingEvaluation).all()
    if not rows:
        return {
            "total_evaluated_staff": 0,
            "average_pre_test_percent": None,
            "average_post_test_percent": None,
            "average_knowledge_improvement_percent": None,
            "competency_pass_rate_percent": None,
            "average_competency_score": None,
            "average_acceptance_score": None,
            "acceptance_level_counts": {"low": 0, "medium": 0, "high": 0},
        }
    dicts = [training_to_dict(row) for row in rows]
    count = len(dicts)
    passed = sum(1 for row in rows if row.competency_passed)
    level_counts = Counter(row.acceptance_level for row in rows)
    return {
        "total_evaluated_staff": count,
        "average_pre_test_percent": _average(row["pre_test_percent"] for row in dicts),
        "average_post_test_percent": _average(row["post_test_percent"] for row in dicts),
        "average_knowledge_improvement_percent": _average(row.knowledge_improvement_percent for row in rows),
        "competency_pass_rate_percent": round((passed / count) * 100, 1),
        "average_competency_score": _average(row.competency_score for row in rows),
        "average_acceptance_score": _average(row.acceptance_mean_score for row in rows),
        "acceptance_level_counts": {level: level_counts.get(level, 0) for level in ("low", "medium", "high")},
    }


def export_training_csv(db: Session) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=TRAINING_EXPORT_FIELDS)
    writer.writeheader()
    for row in list_training_evaluations(db, limit=10000):
        writer.writerow({field: row.get(field) for field in TRAINING_EXPORT_FIELDS})
    return output.getvalue()


def training_to_dict(evaluation: StaffTrainingEvaluation) -> dict[str, object]:
    metrics = calculate_knowledge_metrics(
        evaluation.pre_test_score,
        evaluation.pre_test_total,
        evaluation.post_test_score,
        evaluation.post_test_total,
    )
    acceptance_level = evaluation.acceptance_level or "low"
    return {
        "id": evaluation.id,
        "staff_user_id": evaluation.staff_user_id,
        "staff_name": evaluation.staff_name,
        "staff_role": evaluation.staff_role,
        "study_id": evaluation.study_id,
        "training_date": evaluation.training_date,
        "pre_test_score": evaluation.pre_test_score,
        "pre_test_total": evaluation.pre_test_total,
        "post_test_score": evaluation.post_test_score,
        "post_test_total": evaluation.post_test_total,
        "pre_test_percent": metrics["pre_test_percent"],
        "post_test_percent": metrics["post_test_percent"],
        "knowledge_improvement_score": evaluation.knowledge_improvement_score,
        "knowledge_improvement_percent": evaluation.knowledge_improvement_percent,
        "competency_items": _json_dict(evaluation.competency_items_json),
        "competency_passed": evaluation.competency_passed,
        "competency_score": evaluation.competency_score,
        "competency_notes": evaluation.competency_notes,
        "acceptance_survey": _json_dict(evaluation.acceptance_survey_json),
        "acceptance_total_score": evaluation.acceptance_total_score,
        "acceptance_mean_score": evaluation.acceptance_mean_score,
        "acceptance_level": acceptance_level,
        "acceptance_level_label_ar": ACCEPTANCE_LEVEL_LABELS_AR.get(acceptance_level, acceptance_level),
        "general_notes": evaluation.general_notes,
        "created_by_user_id": evaluation.created_by_user_id,
        "updated_by_user_id": evaluation.updated_by_user_id,
        "created_at": evaluation.created_at,
        "updated_at": evaluation.updated_at,
    }


def _payload_to_model(
    payload: StaffTrainingEvaluationCreate | StaffTrainingEvaluationUpdate,
    evaluation: StaffTrainingEvaluation | None = None,
) -> StaffTrainingEvaluation:
    metrics = calculate_knowledge_metrics(
        payload.pre_test_score,
        payload.pre_test_total,
        payload.post_test_score,
        payload.post_test_total,
    )
    competency = evaluate_competency(payload.competency_items)
    acceptance = calculate_acceptance_score(payload.acceptance_survey)
    evaluation = evaluation or StaffTrainingEvaluation()
    evaluation.staff_user_id = payload.staff_user_id
    evaluation.staff_name = payload.staff_name
    evaluation.staff_role = payload.staff_role
    evaluation.study_id = payload.study_id
    evaluation.training_date = payload.training_date
    evaluation.pre_test_score = payload.pre_test_score
    evaluation.pre_test_total = payload.pre_test_total
    evaluation.post_test_score = payload.post_test_score
    evaluation.post_test_total = payload.post_test_total
    evaluation.knowledge_improvement_score = int(metrics["knowledge_improvement_score"])
    evaluation.knowledge_improvement_percent = float(metrics["knowledge_improvement_percent"])
    evaluation.competency_items_json = json.dumps(competency["competency_items"], ensure_ascii=False)
    evaluation.competency_passed = bool(competency["competency_passed"])
    evaluation.competency_score = float(competency["competency_score"])
    evaluation.competency_notes = payload.competency_notes
    evaluation.acceptance_survey_json = json.dumps(acceptance["acceptance_survey"], ensure_ascii=False)
    evaluation.acceptance_total_score = int(acceptance["acceptance_total_score"])
    evaluation.acceptance_mean_score = float(acceptance["acceptance_mean_score"])
    evaluation.acceptance_level = str(acceptance["acceptance_level"])
    evaluation.general_notes = payload.general_notes
    if payload.created_by_user_id is not None:
        evaluation.created_by_user_id = payload.created_by_user_id
    evaluation.updated_by_user_id = payload.updated_by_user_id or payload.created_by_user_id
    return evaluation


def _validate_score(name: str, score: int, total: int) -> None:
    if total <= 0:
        raise TrainingEvaluationValidationError(f"{name}_total must be greater than zero")
    if score < 0:
        raise TrainingEvaluationValidationError(f"{name}_score must not be negative")
    if score > total:
        raise TrainingEvaluationValidationError(f"{name}_score must not exceed {name}_total")


def _validate_references(db: Session, payload: StaffTrainingEvaluationCreate | StaffTrainingEvaluationUpdate) -> None:
    if payload.staff_user_id is not None and db.get(User, payload.staff_user_id) is None:
        raise TrainingEvaluationTraceabilityError("Staff user not found")
    if payload.study_id is not None and db.get(ResearchStudy, payload.study_id) is None:
        raise TrainingEvaluationTraceabilityError("Research study not found")


def _json_dict(value: str | None) -> dict[str, object]:
    if not value:
        return {}
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _average(values) -> float | None:
    numbers = [float(value) for value in values if value is not None]
    return round(sum(numbers) / len(numbers), 1) if numbers else None


def _create_audit_log(db: Session, action: str, evaluation: StaffTrainingEvaluation, user_id: int | None = None) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="staff_training_evaluation",
            entity_id=str(evaluation.id),
            new_value=f"Training evaluation for {evaluation.staff_name or evaluation.staff_user_id} on {evaluation.training_date}",
        )
    )
