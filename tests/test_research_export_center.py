from datetime import date, datetime, timezone
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import (
    Alert,
    AlertStatus,
    ClinicalDeteriorationEvent,
    ClinicalOutcome,
    ClinicalResponse,
    DialysisSession,
    IntradialyticMeasurement,
    News2Assessment,
    OutcomeValidation72h,
    Patient,
    PatientVascularAccess,
    ResponseTracking,
    StudyGroup,
    StudyPhase,
    User,
    UserRole,
)
from app.services.hd2_protocol_service import build_hd2_nursing_protocol


@pytest.fixture()
def export_client(tmp_path):
    db_path = tmp_path / "research_export.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(
        full_name="Export Doctor",
        email="export-doctor@example.local",
        password_hash="secret-hash",
        role=UserRole.doctor,
        department="Nephrology",
        phone="+000000000",
    )
    patient = Patient(
        patient_code="EXP-P-1",
        full_name="Sensitive Patient Name",
        age=70,
        gender="female",
        target_dry_weight=68.5,
        dialysis_start_date=date(2020, 1, 15),
        dialysis_vintage_months=77,
        weekly_sessions_count=3,
        comorbidities="Diabetes mellitus; hypertension",
        charlson_comorbidity_index=6,
        baseline_functional_status="Independent",
        study_phase=StudyPhase.post_implementation,
        study_group=StudyGroup.intervention,
    )
    db.add_all([user, patient])
    db.flush()
    db.add(PatientVascularAccess(patient_id=patient.id, access_type="av_fistula", access_location="left forearm", inserted_at=date(2021, 2, 1)))
    session = DialysisSession(
        patient_id=patient.id,
        session_date=date(2026, 6, 5),
        weekday="Friday",
        actual_start_time=datetime(2026, 6, 5, 8, 0, tzinfo=timezone.utc),
        actual_end_time=datetime(2026, 6, 5, 12, 0, tzinfo=timezone.utc),
        target_ultrafiltration=2.4,
        blood_flow_rate=300,
        dialysate_flow_rate=500,
        dialysate_temperature=36.5,
        ultrafiltration_rate=9.5,
        ultrafiltration_volume=2.0,
        session_duration_minutes=240,
        session_status="completed",
        created_by_user_id=user.id,
    )
    db.add(session)
    db.flush()

    stable_measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 5, 8, 30, tzinfo=timezone.utc),
        measurement_interval_minutes=30,
        respiratory_rate=18,
        spo2=97,
        oxygen_therapy=False,
        systolic_bp=138,
        diastolic_bp=76,
        pulse_rate=82,
        temperature=36.7,
        consciousness_level="alert",
        confusion_status="none",
        recorded_by_user_id=user.id,
    )
    high_measurement = IntradialyticMeasurement(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        measurement_time=datetime(2026, 6, 5, 9, 15, tzinfo=timezone.utc),
        measurement_interval_minutes=30,
        respiratory_rate=25,
        spo2=90,
        oxygen_therapy=True,
        systolic_bp=88,
        diastolic_bp=54,
        pulse_rate=118,
        temperature=38.1,
        consciousness_level="alert",
        confusion_status="new_confusion",
        recorded_by_user_id=user.id,
    )
    db.add_all([stable_measurement, high_measurement])
    db.flush()
    hd2_protocol = build_hd2_nursing_protocol(8, "red", ["SpO2 <=91%"])

    stable_assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=stable_measurement.id,
        respiratory_score=0,
        spo2_score=0,
        oxygen_score=0,
        systolic_bp_score=0,
        pulse_score=0,
        temperature_score=0,
        consciousness_score=0,
        total_score=0,
        risk_level="low",
        alert_required=False,
        trigger_reason="NEWS2 total score below alert threshold",
        created_by_user_id=user.id,
    )
    high_assessment = News2Assessment(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        intradialytic_measurement_id=high_measurement.id,
        respiratory_score=3,
        spo2_score=3,
        oxygen_score=2,
        systolic_bp_score=3,
        pulse_score=2,
        temperature_score=1,
        consciousness_score=3,
        total_score=16,
        risk_level="high",
        alert_required=True,
        trigger_reason="NEWS2 >= 7",
        hd2_mnews_total_score=8,
        hd2_mnews_risk_color="red",
        hd2_mnews_risk_label_ar=hd2_protocol["risk_label_ar"],
        hd2_mnews_critical_trigger=True,
        hd2_mnews_critical_reasons=json.dumps(["SpO2 <=91%"], ensure_ascii=False),
        hd2_protocol_json=json.dumps(hd2_protocol, ensure_ascii=False),
        hd2_reassessment_interval_min=hd2_protocol["reassessment_interval_minutes_min"],
        hd2_reassessment_interval_max=hd2_protocol["reassessment_interval_minutes_max"],
        hd2_required_response_time_minutes=hd2_protocol["required_response_time_minutes"],
        hd2_requires_physician_call=hd2_protocol["requires_physician_call"],
        hd2_requires_emergency_preparation=hd2_protocol["requires_emergency_preparation"],
        hd2_requires_close_monitoring=hd2_protocol["requires_close_monitoring"],
        created_by_user_id=user.id,
    )
    db.add_all([stable_assessment, high_assessment])
    db.flush()
    alert = Alert(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=high_assessment.id,
        risk_level="high",
        severity_level="high",
        status=AlertStatus.in_progress,
        priority="immediate",
        trigger_reason="NEWS2 >= 7",
        created_at=datetime(2026, 6, 5, 9, 16, tzinfo=timezone.utc),
        viewed_at=datetime(2026, 6, 5, 9, 17, tzinfo=timezone.utc),
        acknowledged_at=datetime(2026, 6, 5, 9, 18, tzinfo=timezone.utc),
        action_taken_at=datetime(2026, 6, 5, 9, 22, tzinfo=timezone.utc),
    )
    db.add(alert)
    db.flush()
    event = ClinicalDeteriorationEvent(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        news2_assessment_id=high_assessment.id,
        alert_id=alert.id,
        deterioration_time=datetime(2026, 6, 5, 9, 20, tzinfo=timezone.utc),
        time_from_session_start_minutes=80,
        deterioration_type="acute_hypotension",
        triggering_news2_score=16,
        description="Acute hypotension with confusion.",
    )
    db.add(event)
    db.flush()
    response = ClinicalResponse(
        clinical_deterioration_event_id=event.id,
        alert_id=alert.id,
        digital_alert_time=alert.created_at,
        actual_response_start_time=datetime(2026, 6, 5, 9, 25, tzinfo=timezone.utc),
        response_delay_minutes=9,
        patient_actions='["stop_ultrafiltration", "give_oxygen"]',
        vascular_access_actions='["check_flow"]',
        responded_by_user_id=user.id,
        notes="Response documented.",
    )
    outcome = ClinicalOutcome(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        clinical_deterioration_event_id=event.id,
        outcome_type="hospital_admission",
        outcome_recorded_at=datetime(2026, 6, 6, 9, 20, tzinfo=timezone.utc),
        outcome_window_hours=24,
        description="Admitted for observation.",
        recorded_by_user_id=user.id,
    )
    tracking = ResponseTracking(
        alert_id=alert.id,
        dialysis_session_id=session.id,
        news2_assessment_id=high_assessment.id,
        clinical_deterioration_event_id=event.id,
        vital_signs_recorded_at=high_measurement.measurement_time,
        alert_created_at=alert.created_at,
        alert_viewed_at=alert.viewed_at,
        actual_response_start_time=response.actual_response_start_time,
        clinical_action_at=response.actual_response_start_time,
        time_to_alert_minutes=1,
        time_to_view_minutes=1,
        time_to_response_minutes=9,
        time_to_action_minutes=9,
        total_response_time_minutes=10,
    )
    validation = OutcomeValidation72h(
        patient_id=patient.id,
        dialysis_session_id=session.id,
        deterioration_occurred=True,
        deterioration_types=json.dumps(["severe_hypotension"], ensure_ascii=False),
        type_specific_details=json.dumps({"lowest_sbp": 82, "required_treatment": True}, ensure_ascii=False),
        deterioration_timing_category="within_24_72h",
        deterioration_datetime=datetime(2026, 6, 6, 8, 0, tzinfo=timezone.utc),
        platform_prediction_status="predicted_before",
        interventions=json.dumps(["doctor_called", "fluids_given"], ensure_ascii=False),
        doctor_response_time_minutes=5,
        final_result="partial_improvement",
        verification_sources=json.dumps(["medical_record_reviewed"], ensure_ascii=False),
        notes="72h validation complete.",
        completed_by_user_id=user.id,
        completed_at=datetime(2026, 6, 8, 12, 0, tzinfo=timezone.utc),
    )
    db.add_all([response, outcome, tracking, validation])
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
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_dataset_builder_returns_rows(export_client):
    response = export_client.get("/api/research/dataset")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_dataset_rows_exclude_patient_full_name(export_client):
    response = export_client.get("/api/research/dataset")

    assert response.status_code == 200
    assert "full_name" not in response.json()[0]
    assert "patient_id" not in response.json()[0]
    assert "Sensitive Patient Name" not in response.text


def test_dataset_includes_required_core_fields(export_client):
    response = export_client.get("/api/research/dataset")

    row = response.json()[0]
    assert {"patient_code", "session_date", "measurement_id", "news2_assessment_id", "news2_total_score", "risk_level"}.issubset(row.keys())


def test_dataset_includes_hd2_protocol_fields(export_client):
    response = export_client.get("/api/research/dataset", params={"risk_level": "high"})

    assert response.status_code == 200
    row = response.json()[0]
    assert row["hd2_risk_color"] == "red"
    assert row["hd2_risk_label_ar"] == "ط£ط­ظ…ط± - ط·ظˆط§ط±ط¦"
    assert row["hd2_reassessment_interval_min"] == 5
    assert row["hd2_required_response_time_minutes"] == 5
    assert row["hd2_requires_physician_call"] is True
    assert row["hd2_requires_emergency_preparation"] is True
    assert row["hd2_requires_close_monitoring"] is True
    assert row["hd2_protocol_action_summary"]


def test_dataset_includes_72h_outcome_validation_fields(export_client):
    response = export_client.get("/api/research/dataset", params={"risk_level": "high"})

    assert response.status_code == 200
    row = response.json()[0]
    assert row["outcome_validation_completed"] is True
    assert row["deterioration_occurred"] is True
    assert row["deterioration_types_72h"] == "severe_hypotension"
    assert row["platform_prediction_status"] == "predicted_before"
    assert row["interventions_72h"] == "doctor_called | fluids_given"
    assert row["doctor_response_time_minutes_72h"] == 5
    assert row["final_result_72h"] == "partial_improvement"
    assert row["verification_sources"] == "medical_record_reviewed"
    assert row["severe_hypotension_lowest_sbp"] == 82
    assert row["severe_hypotension_required_treatment"] is True


def test_filters_work(export_client):
    response = export_client.get("/api/research/dataset", params={"risk_level": "high"})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["risk_level"] == "high"


def test_quality_report_returns_expected_structure(export_client):
    response = export_client.get("/api/research/dataset/quality")

    assert response.status_code == 200
    payload = response.json()
    assert {"quality_score", "total_rows", "issues_count", "issues_by_type", "warnings", "statistics"}.issubset(payload.keys())


def test_csv_export_returns_correct_content_type(export_client):
    response = export_client.get("/api/research/export/csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "patient_code" in response.text


def test_xlsx_export_returns_downloadable_content(export_client):
    response = export_client.get("/api/research/export/xlsx")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert response.content[:2] == b"PK"


def test_spss_codebook_endpoint_works(export_client):
    response = export_client.get("/api/research/export/spss-codebook")

    assert response.status_code == 200
    assert "SPSS-Ready Research Dataset Codebook" in response.text


def test_spss_variable_labels_endpoint_works(export_client):
    response = export_client.get("/api/research/export/spss-variable-labels")

    assert response.status_code == 200
    assert "variable" in response.text
    assert "news2_total_score" in response.text


def test_export_does_not_include_private_identifiers(export_client):
    response = export_client.get("/api/research/export/csv")

    assert response.status_code == 200
    assert "password_hash" not in response.text
    assert "export-doctor@example.local" not in response.text
    assert "+000000000" not in response.text
    assert "Sensitive Patient Name" not in response.text


def test_dataset_row_count_is_stable_with_seeded_data(export_client):
    first = export_client.get("/api/research/dataset").json()
    second = export_client.get("/api/research/dataset").json()

    assert len(first) == 2
    assert len(second) == 2


def test_dataset_preserves_discharged_patients(export_client):
    discharge_response = export_client.post(
        "/api/patients/1/discharge",
        headers={"X-Dev-Role": "doctor"},
        json={"discharge_reason": "Completed dialysis monitoring"},
    )

    response = export_client.get("/api/research/dataset")

    assert discharge_response.status_code == 200
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {row["patient_code"] for row in response.json()} == {"EXP-P-1"}


def test_dataset_preserves_archived_patients(export_client):
    archive_response = export_client.post("/api/patients/1/archive", headers={"X-Dev-Role": "technical_admin"}, json={})

    response = export_client.get("/api/research/dataset")

    assert archive_response.status_code == 200
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {row["patient_code"] for row in response.json()} == {"EXP-P-1"}


def test_dataset_excludes_deleted_patients(export_client):
    delete_response = export_client.post(
        "/api/patients/1/delete",
        headers={"X-Dev-Role": "admin"},
        json={"delete_reason": "Duplicate test record", "confirmation_text": "DELETE PATIENT"},
    )

    response = export_client.get("/api/research/dataset")

    assert delete_response.status_code == 200
    assert response.status_code == 200
    assert response.json() == []
