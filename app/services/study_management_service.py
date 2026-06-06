from __future__ import annotations

from datetime import date

from fastapi import HTTPException
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.models import AuditLog, ClinicalOutcome, Patient, ResearchStudy, ResponseTracking
from app.schemas import ResearchStudyCreate, ResearchStudyUpdate
from app.services.export_service import build_research_dataset, dataset_statistics, validate_research_dataset
from app.services.research_analytics_service import build_analytics_summary


STUDY_STATUS_LABELS = {
    "draft": "مسودة",
    "active": "نشطة",
    "paused": "متوقفة مؤقتا",
    "completed": "مكتملة",
    "archived": "مؤرشفة",
}

STUDY_DESIGN_LABELS = {
    "observational": "رصدية",
    "prospective": "استباقية",
    "retrospective": "استرجاعية",
    "before_after": "قبل وبعد",
    "cohort": "أترابية",
    "pilot": "تجريبية أولية",
}

READINESS_CHECK_LABELS = {
    "study_defined": "تعريف الدراسة",
    "dataset_available": "Dataset",
    "analytics_available": "التحليلات",
    "exports_available": "التصدير",
    "outcomes_available": "المآلات",
    "response_tracking_available": "تتبع الاستجابة",
}

STUDY_COLUMNS = {
    "study_code": "VARCHAR(80)",
    "study_title": "VARCHAR(255)",
    "study_description": "TEXT",
    "principal_investigator": "VARCHAR(160)",
    "study_design": "VARCHAR(80)",
    "study_phase": "VARCHAR(80)",
    "study_status": "VARCHAR(40) DEFAULT 'draft' NOT NULL",
    "study_group_a_name": "VARCHAR(160)",
    "study_group_b_name": "VARCHAR(160)",
    "baseline_period_start": "DATE",
    "baseline_period_end": "DATE",
    "intervention_period_start": "DATE",
    "intervention_period_end": "DATE",
    "study_start_date": "DATE",
    "study_end_date": "DATE",
    "target_sample_size": "INTEGER",
    "inclusion_notes": "TEXT",
    "exclusion_notes": "TEXT",
    "notes": "TEXT",
}


def ensure_research_study_schema(db: Session, db_engine: Engine | None = None) -> None:
    db_engine = db_engine or db.get_bind()
    inspector = inspect(db_engine)
    if "research_studies" not in inspector.get_table_names():
        ResearchStudy.metadata.create_all(bind=db_engine, tables=[ResearchStudy.__table__])
        return

    existing_columns = {column["name"] for column in inspector.get_columns("research_studies")}
    missing = [(name, sql_type) for name, sql_type in STUDY_COLUMNS.items() if name not in existing_columns]
    for name, sql_type in missing:
        db.execute(text(f"ALTER TABLE research_studies ADD COLUMN {name} {sql_type}"))
    if missing:
        db.execute(
            text(
                """
                UPDATE research_studies
                SET
                    study_title = COALESCE(study_title, title),
                    study_description = COALESCE(study_description, description),
                    study_start_date = COALESCE(study_start_date, start_date),
                    study_end_date = COALESCE(study_end_date, end_date),
                    study_status = COALESCE(study_status, status, 'draft')
                """
            )
        )
        db.commit()


def create_study(db: Session, payload: ResearchStudyCreate) -> ResearchStudy:
    ensure_research_study_schema(db)
    existing = db.query(ResearchStudy).filter(ResearchStudy.study_code == payload.study_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="study_code already exists")
    study = ResearchStudy(**payload.model_dump())
    _sync_legacy_fields(study)
    db.add(study)
    db.flush()
    db.add(AuditLog(action="study_created", entity_type="research_study", entity_id=str(study.id), new_value=study.study_code))
    db.commit()
    db.refresh(study)
    return study


def update_study(db: Session, study_id: int, payload: ResearchStudyUpdate) -> ResearchStudy:
    ensure_research_study_schema(db)
    study = get_study(db, study_id)
    changes = payload.model_dump(exclude_unset=True)
    if "study_code" in changes:
        existing = db.query(ResearchStudy).filter(ResearchStudy.study_code == changes["study_code"], ResearchStudy.id != study_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="study_code already exists")
    old_status = study.study_status
    for key, value in changes.items():
        setattr(study, key, value)
    _validate_study_dates(study)
    _sync_legacy_fields(study)
    db.add(AuditLog(action="study_updated", entity_type="research_study", entity_id=str(study.id), old_value=old_status, new_value=study.study_status))
    db.commit()
    db.refresh(study)
    return study


def get_study(db: Session, study_id: int) -> ResearchStudy:
    ensure_research_study_schema(db)
    study = db.get(ResearchStudy, study_id)
    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")
    _hydrate_legacy_fields(study)
    return study


def list_studies(db: Session) -> list[ResearchStudy]:
    ensure_research_study_schema(db)
    studies = db.query(ResearchStudy).order_by(ResearchStudy.created_at.desc(), ResearchStudy.id.desc()).all()
    for study in studies:
        _hydrate_legacy_fields(study)
    return studies


def build_study_readiness_report(db: Session, study_id: int) -> dict[str, object]:
    ensure_research_study_schema(db)
    study = get_study(db, study_id)
    rows = build_research_dataset(db)
    quality = validate_research_dataset(rows)
    stats = dataset_statistics(rows, quality)
    analytics = build_analytics_summary(db)
    kpis = analytics.get("kpis", {})

    checks = {
        "study_defined": bool(study.study_code and study.study_title and study.study_design and study.study_status),
        "dataset_available": bool(rows),
        "analytics_available": bool(kpis.get("total_news2_assessments")),
        "exports_available": bool(rows and quality.get("quality_score", 0) >= 50),
        "outcomes_available": db.query(ClinicalOutcome).count() > 0,
        "response_tracking_available": db.query(ResponseTracking).count() > 0,
    }
    readiness_score = round((sum(1 for value in checks.values() if value) / len(checks)) * 100)
    missing = [key for key, is_ready in checks.items() if not is_ready]
    warnings = _readiness_warnings(study, quality, stats)
    recommendations = _readiness_recommendations(missing, warnings)
    dashboard = {
        "study_title": study.study_title,
        "principal_investigator": study.principal_investigator,
        "study_status": study.study_status,
        "study_status_label": STUDY_STATUS_LABELS.get(study.study_status, study.study_status),
        "study_design": study.study_design,
        "study_design_label": STUDY_DESIGN_LABELS.get(study.study_design or "", study.study_design),
        "target_sample_size": study.target_sample_size,
        "current_patients": db.query(Patient).count(),
        "dataset_rows": len(rows),
        "analytics_status": "ready" if checks["analytics_available"] else "not_ready",
        "export_readiness": kpis.get("export_readiness", "not_ready"),
        "readiness_score": readiness_score,
        "dataset_quality_score": quality.get("quality_score", 0),
    }
    db.add(AuditLog(action="study_readiness_viewed", entity_type="research_study", entity_id=str(study.id), new_value=str(readiness_score)))
    db.commit()
    return {
        "study_id": study.id,
        "readiness_score": readiness_score,
        "missing_requirements": missing,
        "warnings": warnings,
        "recommendations": recommendations,
        "checks": checks,
        "check_labels": READINESS_CHECK_LABELS,
        "dashboard": dashboard,
        "protocol": {
            "study_objective": study.study_description,
            "study_design": study.study_design,
            "baseline_period": _period(study.baseline_period_start, study.baseline_period_end),
            "intervention_period": _period(study.intervention_period_start, study.intervention_period_end),
            "inclusion_notes": study.inclusion_notes,
            "exclusion_notes": study.exclusion_notes,
            "research_notes": study.notes,
        },
        "timeline": {
            "study_start": study.study_start_date,
            "baseline_period_start": study.baseline_period_start,
            "baseline_period_end": study.baseline_period_end,
            "intervention_period_start": study.intervention_period_start,
            "intervention_period_end": study.intervention_period_end,
            "current_date": date.today(),
            "study_end": study.study_end_date,
        },
    }


def _sync_legacy_fields(study: ResearchStudy) -> None:
    study.title = study.study_title
    study.description = study.study_description
    study.start_date = study.study_start_date
    study.end_date = study.study_end_date
    study.status = study.study_status


def _hydrate_legacy_fields(study: ResearchStudy) -> None:
    study.study_title = study.study_title or study.title
    study.study_description = study.study_description or study.description
    study.study_start_date = study.study_start_date or study.start_date
    study.study_end_date = study.study_end_date or study.end_date
    study.study_status = study.study_status or study.status or "draft"


def _validate_study_dates(study: ResearchStudy) -> None:
    pairs = [
        ("baseline_period_start", "baseline_period_end"),
        ("intervention_period_start", "intervention_period_end"),
        ("study_start_date", "study_end_date"),
    ]
    for start_key, end_key in pairs:
        start = getattr(study, start_key)
        end = getattr(study, end_key)
        if start and end and end < start:
            raise HTTPException(status_code=422, detail=f"{end_key} must be on or after {start_key}")


def _readiness_warnings(study: ResearchStudy, quality: dict[str, object], stats: dict[str, object]) -> list[str]:
    warnings: list[str] = []
    if study.target_sample_size and int(stats.get("dataset_rows", 0)) < study.target_sample_size:
        warnings.append("target_sample_size_not_reached")
    if int(quality.get("issues_count", 0)):
        warnings.extend(str(warning) for warning in quality.get("warnings", []))
    if study.study_status == "active" and not study.study_start_date:
        warnings.append("active_study_without_start_date")
    return warnings


def _readiness_recommendations(missing: list[str], warnings: list[str]) -> list[str]:
    recommendations = []
    if "study_defined" in missing:
        recommendations.append("complete_protocol_configuration")
    if "dataset_available" in missing:
        recommendations.append("record_news2_measurements_before_export")
    if "outcomes_available" in missing:
        recommendations.append("document_clinical_outcomes_for_deterioration_events")
    if "response_tracking_available" in missing:
        recommendations.append("complete_response_tracking_for_alerts")
    if warnings:
        recommendations.append("review_dataset_quality_before_analysis")
    return recommendations


def _period(start: date | None, end: date | None) -> dict[str, date | None]:
    return {"start": start, "end": end}
