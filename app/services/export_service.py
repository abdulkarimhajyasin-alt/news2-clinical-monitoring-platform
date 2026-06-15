from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from io import BytesIO, StringIO
import csv
import html
import zipfile

from sqlalchemy.orm import Session

from app.models import (
    Alert,
    ClinicalDeteriorationEvent,
    ClinicalOutcome,
    ClinicalResponse,
    DialysisSession,
    IntradialyticMeasurement,
    News2Assessment,
    Patient,
    PatientVascularAccess,
    ResponseTracking,
)


DATASET_FIELDS = [
    "patient_code",
    "age",
    "gender",
    "target_dry_weight",
    "dialysis_start_date",
    "dialysis_vintage_months",
    "weekly_sessions_count",
    "comorbidities",
    "charlson_comorbidity_index",
    "baseline_functional_status",
    "study_phase",
    "study_group",
    "vascular_access_type",
    "vascular_access_location",
    "vascular_access_inserted_at",
    "dialysis_session_id",
    "session_date",
    "weekday",
    "actual_start_time",
    "actual_end_time",
    "target_ultrafiltration",
    "blood_flow_rate",
    "dialysate_flow_rate",
    "dialysate_temperature",
    "ultrafiltration_rate",
    "ultrafiltration_volume",
    "session_duration_minutes",
    "session_status",
    "measurement_id",
    "measurement_time",
    "measurement_interval_minutes",
    "respiratory_rate",
    "spo2",
    "oxygen_therapy",
    "systolic_bp",
    "diastolic_bp",
    "pulse_rate",
    "temperature",
    "consciousness_level",
    "confusion_status",
    "news2_assessment_id",
    "respiratory_score",
    "spo2_score",
    "oxygen_score",
    "systolic_bp_score",
    "pulse_score",
    "temperature_score",
    "consciousness_score",
    "news2_total_score",
    "risk_level",
    "alert_required",
    "trigger_reason",
    "alert_id",
    "alert_created",
    "alert_status",
    "alert_priority",
    "alert_severity_level",
    "alert_trigger_reason",
    "alert_created_at",
    "alert_viewed_at",
    "alert_acknowledged_at",
    "alert_action_taken_at",
    "alert_closed_at",
    "clinical_deterioration_event_id",
    "deterioration_time",
    "time_from_session_start_minutes",
    "deterioration_type",
    "triggering_news2_score",
    "deterioration_description",
    "clinical_response_id",
    "digital_alert_time",
    "actual_response_start_time",
    "response_delay_minutes",
    "patient_actions",
    "vascular_access_actions",
    "response_notes",
    "response_tracking_id",
    "time_to_alert_minutes",
    "time_to_view_minutes",
    "time_to_response_minutes",
    "time_to_action_minutes",
    "total_response_time_minutes",
    "clinical_outcome_id",
    "outcome_type",
    "outcome_recorded_at",
    "outcome_window_hours",
    "outcome_description",
]


VARIABLE_LABELS = {
    "patient_code": "Anonymized patient code",
    "age": "Patient age in years",
    "gender": "Patient gender",
    "study_phase": "Research study phase",
    "study_group": "Research study group",
    "measurement_id": "Intradialytic measurement identifier",
    "measurement_time": "Vital-sign measurement timestamp",
    "news2_total_score": "NEWS2 total score",
    "risk_level": "NEWS2 risk level",
    "alert_created": "Whether a NEWS2 alert was created",
    "deterioration_type": "Clinical deterioration type",
    "response_delay_minutes": "Minutes from digital alert to response start",
    "outcome_type": "Clinical outcome category",
}


VALUE_LABELS = {
    "study_phase": {"pre_implementation": "Pre implementation", "post_implementation": "Post implementation"},
    "study_group": {"control": "Control", "intervention": "Intervention"},
    "risk_level": {"low": "Low", "medium": "Medium", "high": "High", "critical": "Critical"},
    "alert_created": {False: "No alert", True: "Alert created"},
}


def build_research_dataset(db: Session, filters: dict[str, object] | None = None, limit: int | None = None) -> list[dict[str, object]]:
    filters = filters or {}
    assessments = (
        db.query(News2Assessment)
        .join(IntradialyticMeasurement, News2Assessment.intradialytic_measurement_id == IntradialyticMeasurement.id)
        .order_by(IntradialyticMeasurement.measurement_time.desc(), News2Assessment.id.desc())
        .all()
    )
    rows: list[dict[str, object]] = []
    for assessment in assessments:
        measurement = db.get(IntradialyticMeasurement, assessment.intradialytic_measurement_id)
        patient = db.get(Patient, assessment.patient_id)
        session = db.get(DialysisSession, assessment.dialysis_session_id)
        if measurement is None or patient is None:
            continue
        if patient.status == "deleted":
            continue
        alert = db.query(Alert).filter(Alert.news2_assessment_id == assessment.id).first()
        event = db.query(ClinicalDeteriorationEvent).filter(ClinicalDeteriorationEvent.news2_assessment_id == assessment.id).first()
        response = (
            db.query(ClinicalResponse)
            .filter(ClinicalResponse.clinical_deterioration_event_id == event.id)
            .first()
            if event
            else None
        )
        tracking = db.query(ResponseTracking).filter(ResponseTracking.alert_id == alert.id).first() if alert else None
        outcome = (
            db.query(ClinicalOutcome)
            .filter(ClinicalOutcome.clinical_deterioration_event_id == event.id)
            .order_by(ClinicalOutcome.outcome_window_hours.asc(), ClinicalOutcome.created_at.asc())
            .first()
            if event
            else None
        )
        access = (
            db.query(PatientVascularAccess)
            .filter(PatientVascularAccess.patient_id == patient.id)
            .order_by(PatientVascularAccess.inserted_at.desc().nullslast(), PatientVascularAccess.id.desc())
            .first()
        )
        row = _dataset_row(patient, session, access, measurement, assessment, alert, event, response, tracking, outcome)
        if _matches_filters(row, filters):
            rows.append(_public_row(row))
            if limit is not None and len(rows) >= limit:
                break
    return rows


def validate_research_dataset(rows: list[dict[str, object]]) -> dict[str, object]:
    issues: list[dict[str, object]] = []
    measurement_ids: Counter[object] = Counter(row.get("measurement_id") for row in rows)
    duplicate_ids = {measurement_id for measurement_id, count in measurement_ids.items() if measurement_id is not None and count > 1}

    for row in rows:
        row_ref = row.get("measurement_id") or row.get("news2_assessment_id") or "unknown"
        if not row.get("patient_code"):
            issues.append(_issue("missing_patient_code", row_ref))
        if not row.get("dialysis_session_id"):
            issues.append(_issue("missing_session", row_ref))
        if not row.get("measurement_time"):
            issues.append(_issue("missing_measurement_time", row_ref))
        if row.get("news2_total_score") is None:
            issues.append(_issue("missing_news2_total_score", row_ref))
        if _invalid_timestamp_sequence(row):
            issues.append(_issue("invalid_timestamp_sequence", row_ref))
        if row.get("clinical_deterioration_event_id") and not row.get("clinical_outcome_id"):
            issues.append(_issue("missing_outcome_for_deterioration", row_ref))
        if row.get("alert_id") and not row.get("clinical_response_id"):
            issues.append(_issue("alert_without_response", row_ref))
        if row.get("clinical_response_id") and not row.get("response_tracking_id"):
            issues.append(_issue("response_without_tracking", row_ref))
        if row.get("measurement_id") in duplicate_ids:
            issues.append(_issue("duplicate_dataset_rows", row_ref))

    issues_by_type = dict(Counter(issue["type"] for issue in issues))
    penalties = {
        "missing_patient_code": 20,
        "missing_session": 15,
        "missing_measurement_time": 15,
        "missing_news2_total_score": 15,
        "invalid_timestamp_sequence": 15,
        "missing_outcome_for_deterioration": 8,
        "alert_without_response": 8,
        "response_without_tracking": 6,
        "duplicate_dataset_rows": 10,
    }
    penalty = sum(penalties.get(issue["type"], 5) for issue in issues)
    quality_score = max(0, 100 - penalty)
    warnings = [
        f"{issue_type}: {count} issue(s)"
        for issue_type, count in sorted(issues_by_type.items())
    ]
    return {
        "quality_score": quality_score,
        "total_rows": len(rows),
        "issues_count": len(issues),
        "issues_by_type": issues_by_type,
        "warnings": warnings,
    }


def export_dataset_csv(rows: list[dict[str, object]]) -> bytes:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=DATASET_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: _serialize(row.get(field)) for field in DATASET_FIELDS})
    return output.getvalue().encode("utf-8-sig")


def export_dataset_xlsx(rows: list[dict[str, object]]) -> bytes:
    shared_strings: list[str] = []
    shared_index: dict[str, int] = {}

    def string_id(value: object) -> int:
        text = _serialize(value)
        if text not in shared_index:
            shared_index[text] = len(shared_strings)
            shared_strings.append(text)
        return shared_index[text]

    sheet_rows = []
    for row_index, values in enumerate([DATASET_FIELDS, *[[row.get(field) for field in DATASET_FIELDS] for row in rows]], start=1):
        cells = []
        for col_index, value in enumerate(values, start=1):
            ref = f"{_excel_column(col_index)}{row_index}"
            cells.append(f'<c r="{ref}" t="s"><v>{string_id(value)}</v></c>')
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    sheet_xml = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    shared_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared_strings)}" uniqueCount="{len(shared_strings)}">'
        + "".join(f"<si><t>{html.escape(value)}</t></si>" for value in shared_strings)
        + "</sst>"
    )
    workbook_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="research_dataset" sheetId="1" r:id="rId1"/></sheets></workbook>'
    rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    workbook_rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>'
    content_types_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>'

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml)
        archive.writestr("_rels/.rels", rels_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        archive.writestr("xl/sharedStrings.xml", shared_xml)
    return buffer.getvalue()


def build_spss_codebook() -> str:
    value_label_lines = []
    for variable, values in VALUE_LABELS.items():
        value_label_lines.append(f"- `{variable}`: " + "; ".join(f"{key} = {label}" for key, label in values.items()))
    field_lines = [f"- `{field}`: {VARIABLE_LABELS.get(field, field.replace('_', ' ').title())}" for field in DATASET_FIELDS]
    return "\n".join(
        [
            "# SPSS-Ready Research Dataset Codebook",
            "",
            "Dataset row definition: one intradialytic measurement with its linked NEWS2 assessment, enriched with downstream clinical workflow data when available.",
            "",
            "Privacy: exports include anonymized patient codes and exclude patient names, user emails, phones, password hashes, IP addresses, and user agents.",
            "",
            "## Variables",
            *field_lines,
            "",
            "## Value Labels",
            *value_label_lines,
            "",
            "## Missing Values",
            "Blank cells represent unavailable or not-yet-documented linked workflow data.",
            "",
            "## Notes",
            "This package is SPSS-ready CSV plus labels and codebook. It is not a native .sav file.",
        ]
    )


def build_spss_variable_labels() -> bytes:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["variable", "label"])
    writer.writeheader()
    for field in DATASET_FIELDS:
        writer.writerow({"variable": field, "label": VARIABLE_LABELS.get(field, field.replace("_", " ").title())})
    return output.getvalue().encode("utf-8-sig")


def dataset_statistics(rows: list[dict[str, object]], quality: dict[str, object]) -> dict[str, object]:
    return {
        "dataset_rows": len(rows),
        "measurements_count": len({row.get("measurement_id") for row in rows if row.get("measurement_id") is not None}),
        "news2_alerts_count": sum(1 for row in rows if row.get("alert_created")),
        "deterioration_events_count": len({row.get("clinical_deterioration_event_id") for row in rows if row.get("clinical_deterioration_event_id") is not None}),
        "responses_count": len({row.get("clinical_response_id") for row in rows if row.get("clinical_response_id") is not None}),
        "outcomes_count": len({row.get("clinical_outcome_id") for row in rows if row.get("clinical_outcome_id") is not None}),
        "completion_rate": quality.get("quality_score", 0),
    }


def _dataset_row(
    patient: Patient,
    session: DialysisSession | None,
    access: PatientVascularAccess | None,
    measurement: IntradialyticMeasurement,
    assessment: News2Assessment,
    alert: Alert | None,
    event: ClinicalDeteriorationEvent | None,
    response: ClinicalResponse | None,
    tracking: ResponseTracking | None,
    outcome: ClinicalOutcome | None,
) -> dict[str, object]:
    return {
        "_patient_id": patient.id,
        "patient_code": patient.patient_code,
        "age": patient.age,
        "gender": patient.gender,
        "target_dry_weight": patient.target_dry_weight,
        "dialysis_start_date": patient.dialysis_start_date,
        "dialysis_vintage_months": patient.dialysis_vintage_months,
        "weekly_sessions_count": patient.weekly_sessions_count,
        "comorbidities": patient.comorbidities,
        "charlson_comorbidity_index": patient.charlson_comorbidity_index,
        "baseline_functional_status": patient.baseline_functional_status,
        "study_phase": patient.study_phase,
        "study_group": patient.study_group,
        "vascular_access_type": access.access_type if access else None,
        "vascular_access_location": access.access_location if access else None,
        "vascular_access_inserted_at": access.inserted_at if access else None,
        "dialysis_session_id": session.id if session else None,
        "session_date": session.session_date if session else None,
        "weekday": session.weekday if session else None,
        "actual_start_time": session.actual_start_time if session else None,
        "actual_end_time": session.actual_end_time if session else None,
        "target_ultrafiltration": session.target_ultrafiltration if session else None,
        "blood_flow_rate": session.blood_flow_rate if session else None,
        "dialysate_flow_rate": session.dialysate_flow_rate if session else None,
        "dialysate_temperature": session.dialysate_temperature if session else None,
        "ultrafiltration_rate": session.ultrafiltration_rate if session else None,
        "ultrafiltration_volume": session.ultrafiltration_volume if session else None,
        "session_duration_minutes": session.session_duration_minutes if session else None,
        "session_status": session.session_status if session else None,
        "measurement_id": measurement.id,
        "measurement_time": measurement.measurement_time,
        "measurement_interval_minutes": measurement.measurement_interval_minutes,
        "respiratory_rate": measurement.respiratory_rate,
        "spo2": measurement.spo2,
        "oxygen_therapy": measurement.oxygen_therapy,
        "systolic_bp": measurement.systolic_bp,
        "diastolic_bp": measurement.diastolic_bp,
        "pulse_rate": measurement.pulse_rate,
        "temperature": measurement.temperature,
        "consciousness_level": measurement.consciousness_level,
        "confusion_status": measurement.confusion_status,
        "news2_assessment_id": assessment.id,
        "respiratory_score": assessment.respiratory_score,
        "spo2_score": assessment.spo2_score,
        "oxygen_score": assessment.oxygen_score,
        "systolic_bp_score": assessment.systolic_bp_score,
        "pulse_score": assessment.pulse_score,
        "temperature_score": assessment.temperature_score,
        "consciousness_score": assessment.consciousness_score,
        "news2_total_score": assessment.total_score,
        "risk_level": assessment.risk_level,
        "alert_required": assessment.alert_required,
        "trigger_reason": assessment.trigger_reason,
        "alert_id": alert.id if alert else None,
        "alert_created": alert is not None,
        "alert_status": alert.status if alert else None,
        "alert_priority": alert.priority if alert else None,
        "alert_severity_level": alert.severity_level if alert else None,
        "alert_trigger_reason": alert.trigger_reason if alert else None,
        "alert_created_at": alert.created_at if alert else None,
        "alert_viewed_at": alert.viewed_at if alert else None,
        "alert_acknowledged_at": alert.acknowledged_at if alert else None,
        "alert_action_taken_at": alert.action_taken_at if alert else None,
        "alert_closed_at": alert.closed_at if alert else None,
        "clinical_deterioration_event_id": event.id if event else None,
        "deterioration_time": event.deterioration_time if event else None,
        "time_from_session_start_minutes": event.time_from_session_start_minutes if event else None,
        "deterioration_type": event.deterioration_type if event else None,
        "triggering_news2_score": event.triggering_news2_score if event else None,
        "deterioration_description": event.description if event else None,
        "clinical_response_id": response.id if response else None,
        "digital_alert_time": response.digital_alert_time if response else None,
        "actual_response_start_time": response.actual_response_start_time if response else None,
        "response_delay_minutes": response.response_delay_minutes if response else None,
        "patient_actions": response.patient_actions if response else None,
        "vascular_access_actions": response.vascular_access_actions if response else None,
        "response_notes": response.notes if response else None,
        "response_tracking_id": tracking.id if tracking else None,
        "time_to_alert_minutes": tracking.time_to_alert_minutes if tracking else None,
        "time_to_view_minutes": tracking.time_to_view_minutes if tracking else None,
        "time_to_response_minutes": tracking.time_to_response_minutes if tracking else None,
        "time_to_action_minutes": tracking.time_to_action_minutes if tracking else None,
        "total_response_time_minutes": tracking.total_response_time_minutes if tracking else None,
        "clinical_outcome_id": outcome.id if outcome else None,
        "outcome_type": outcome.outcome_type if outcome else None,
        "outcome_recorded_at": outcome.outcome_recorded_at if outcome else None,
        "outcome_window_hours": outcome.outcome_window_hours if outcome else None,
        "outcome_description": outcome.description if outcome else None,
    }


def _matches_filters(row: dict[str, object], filters: dict[str, object]) -> bool:
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    session_date = row.get("session_date")
    if start_date and isinstance(session_date, date) and session_date < start_date:
        return False
    if end_date and isinstance(session_date, date) and session_date > end_date:
        return False
    for key in ["patient_code", "study_phase", "study_group", "risk_level", "outcome_type", "deterioration_type"]:
        if filters.get(key) and row.get(key) != filters[key]:
            return False
    patient_id = filters.get("patient_id")
    if patient_id and row.get("_patient_id") == patient_id:
        return True
    if patient_id:
        return False
    return True


def _invalid_timestamp_sequence(row: dict[str, object]) -> bool:
    measurement_time = row.get("measurement_time")
    alert_created_at = row.get("alert_created_at")
    response_start = row.get("actual_response_start_time")
    outcome_recorded_at = row.get("outcome_recorded_at")
    deterioration_time = row.get("deterioration_time")
    if measurement_time and alert_created_at and _as_naive(alert_created_at) < _as_naive(measurement_time):
        return True
    if alert_created_at and response_start and _as_naive(response_start) < _as_naive(alert_created_at):
        return True
    if deterioration_time and outcome_recorded_at and _as_naive(outcome_recorded_at) < _as_naive(deterioration_time):
        return True
    return False


def _public_row(row: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in row.items() if not key.startswith("_")}


def _as_naive(value: datetime) -> datetime:
    return value.replace(tzinfo=None) if value.tzinfo else value


def _issue(issue_type: str, row_ref: object) -> dict[str, object]:
    return {"type": issue_type, "row_ref": row_ref}


def _serialize(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, bool):
        return "1" if value else "0"
    return str(value)


def _excel_column(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result
