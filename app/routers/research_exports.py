from datetime import date

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.services.export_service import (
    build_research_dataset,
    build_spss_codebook,
    build_spss_variable_labels,
    dataset_statistics,
    export_dataset_csv,
    export_dataset_xlsx,
    validate_research_dataset,
)

router = APIRouter(prefix="/api/research", tags=["research exports"])


@router.get("/dataset")
def read_research_dataset(
    start_date: date | None = None,
    end_date: date | None = None,
    patient_id: int | None = Query(default=None, gt=0),
    patient_code: str | None = None,
    study_phase: str | None = None,
    study_group: str | None = None,
    risk_level: str | None = None,
    outcome_type: str | None = None,
    deterioration_type: str | None = None,
    limit: int = Query(default=25, gt=0, le=1000),
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    return build_research_dataset(db, _filters(locals()), limit=limit)


@router.get("/dataset/quality")
def read_research_dataset_quality(
    start_date: date | None = None,
    end_date: date | None = None,
    patient_id: int | None = Query(default=None, gt=0),
    patient_code: str | None = None,
    study_phase: str | None = None,
    study_group: str | None = None,
    risk_level: str | None = None,
    outcome_type: str | None = None,
    deterioration_type: str | None = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:view")),
):
    rows = build_research_dataset(db, _filters(locals()))
    quality = validate_research_dataset(rows)
    return {**quality, "statistics": dataset_statistics(rows, quality)}


@router.get("/export/csv")
def export_research_dataset_csv(
    start_date: date | None = None,
    end_date: date | None = None,
    patient_id: int | None = Query(default=None, gt=0),
    patient_code: str | None = None,
    study_phase: str | None = None,
    study_group: str | None = None,
    risk_level: str | None = None,
    outcome_type: str | None = None,
    deterioration_type: str | None = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:export")),
):
    rows = build_research_dataset(db, _filters(locals()))
    return Response(
        content=export_dataset_csv(rows),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="research_dataset.csv"'},
    )


@router.get("/export/xlsx")
def export_research_dataset_xlsx(
    start_date: date | None = None,
    end_date: date | None = None,
    patient_id: int | None = Query(default=None, gt=0),
    patient_code: str | None = None,
    study_phase: str | None = None,
    study_group: str | None = None,
    risk_level: str | None = None,
    outcome_type: str | None = None,
    deterioration_type: str | None = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("research:export")),
):
    rows = build_research_dataset(db, _filters(locals()))
    return Response(
        content=export_dataset_xlsx(rows),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="research_dataset.xlsx"'},
    )


@router.get("/export/spss-codebook")
def export_spss_codebook(_current_user=Depends(require_permission("research:export"))):
    return Response(
        content=build_spss_codebook(),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="spss_codebook.md"'},
    )


@router.get("/export/spss-variable-labels")
def export_spss_variable_labels(_current_user=Depends(require_permission("research:export"))):
    return Response(
        content=build_spss_variable_labels(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="spss_variable_labels.csv"'},
    )


def _filters(values: dict[str, object]) -> dict[str, object]:
    excluded = {"db", "limit"}
    return {key: value for key, value in values.items() if key not in excluded and value is not None}
