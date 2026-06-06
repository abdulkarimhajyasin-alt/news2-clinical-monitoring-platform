from datetime import date, datetime, timedelta, timezone
import json

from sqlalchemy.orm import Session

from app.database import SessionLocal, create_database
from app.models import (
    AccessType,
    Alert,
    AlertStatus,
    AuditLog,
    ClinicalDeteriorationEvent,
    ClinicalNote,
    ClinicalOutcome,
    ClinicalResponse,
    DialysisSession,
    DeteriorationType,
    IntradialyticMeasurement,
    News2Assessment,
    OutcomeType,
    Patient,
    PatientVascularAccess,
    ResearchStudy,
    ResponseTracking,
    StudyGroup,
    StudyPhase,
    SystemSetting,
    User,
    UserRole,
)
from app.schemas import NEWS2CalculationRequest
from app.services.news2_service import calculate_news2


def _json(value: list[str]) -> str:
    return json.dumps(value, ensure_ascii=False)


def seed_database(db: Session) -> dict[str, int | str]:
    create_database()
    existing = db.query(SystemSetting).filter(SystemSetting.setting_key == "seed_version").first()
    if existing:
        return {"status": "already_seeded", "seed_version": existing.setting_value}

    now = datetime.now(timezone.utc).replace(microsecond=0)

    users = [
        User(full_name="د. باحث سريري 01", email="admin@example.local", password_hash="not-for-auth-phase", role=UserRole.admin, department="Research", phone="+0000000001"),
        User(full_name="د. طبيب كلى 01", email="doctor@example.local", password_hash="not-for-auth-phase", role=UserRole.doctor, department="Nephrology", phone="+0000000002"),
        User(full_name="تمريض غسيل 01", email="nurse@example.local", password_hash="not-for-auth-phase", role=UserRole.nurse, department="Dialysis Unit", phone="+0000000003"),
        User(full_name="باحث بيانات 01", email="researcher@example.local", password_hash="not-for-auth-phase", role=UserRole.researcher, department="Clinical Research", phone="+0000000004"),
    ]
    db.add_all(users)
    db.flush()

    patients = [
        Patient(
            patient_code="ANON-P-1001",
            full_name="مريض مرمز 1001",
            age=58,
            gender="female",
            target_dry_weight=67.5,
            dialysis_start_date=date(2021, 3, 12),
            dialysis_vintage_months=62,
            weekly_sessions_count=3,
            comorbidities="Diabetes mellitus; hypertension",
            charlson_comorbidity_index=5,
            baseline_functional_status="Independent with mild exertional limitation",
            study_phase=StudyPhase.pre_implementation,
            study_group=StudyGroup.control,
        ),
        Patient(
            patient_code="ANON-P-1002",
            full_name="مريض مرمز 1002",
            age=66,
            gender="male",
            target_dry_weight=74.0,
            dialysis_start_date=date(2019, 8, 2),
            dialysis_vintage_months=82,
            weekly_sessions_count=3,
            comorbidities="Ischemic heart disease; hypertension",
            charlson_comorbidity_index=6,
            baseline_functional_status="Requires assistance after dialysis",
            study_phase=StudyPhase.post_implementation,
            study_group=StudyGroup.intervention,
        ),
        Patient(
            patient_code="ANON-P-1003",
            full_name="مريض مرمز 1003",
            age=49,
            gender="female",
            target_dry_weight=61.2,
            dialysis_start_date=date(2023, 1, 20),
            dialysis_vintage_months=40,
            weekly_sessions_count=3,
            comorbidities="Hypertension",
            charlson_comorbidity_index=3,
            baseline_functional_status="Independent",
            study_phase=StudyPhase.post_implementation,
            study_group=StudyGroup.intervention,
        ),
    ]
    db.add_all(patients)
    db.flush()

    db.add_all(
        [
            PatientVascularAccess(patient_id=patients[0].id, access_type=AccessType.av_fistula, access_location="left forearm", inserted_at=date(2020, 11, 5), notes="Mature access with stable thrill"),
            PatientVascularAccess(patient_id=patients[1].id, access_type=AccessType.central_venous_catheter, access_location="right internal jugular", inserted_at=date(2025, 12, 15), notes="Temporary catheter under infection surveillance"),
            PatientVascularAccess(patient_id=patients[2].id, access_type=AccessType.av_graft, access_location="right upper arm", inserted_at=date(2022, 9, 9), notes="Patent graft"),
        ]
    )

    session_start = now.replace(hour=8, minute=0, second=0)
    sessions = [
        DialysisSession(
            patient_id=patients[0].id,
            session_date=session_start.date(),
            weekday="Tuesday",
            actual_start_time=session_start,
            actual_end_time=session_start + timedelta(hours=4),
            target_ultrafiltration=2.1,
            blood_flow_rate=320,
            dialysate_flow_rate=500,
            dialysate_temperature=36.5,
            ultrafiltration_rate=8.0,
            ultrafiltration_volume=2.0,
            session_duration_minutes=240,
            session_status="completed",
            session_notes="Stable session",
            created_by_user_id=users[2].id,
        ),
        DialysisSession(
            patient_id=patients[1].id,
            session_date=session_start.date(),
            weekday="Tuesday",
            actual_start_time=session_start + timedelta(minutes=30),
            target_ultrafiltration=2.8,
            blood_flow_rate=280,
            dialysate_flow_rate=500,
            dialysate_temperature=36.0,
            ultrafiltration_rate=10.5,
            ultrafiltration_volume=1.4,
            session_duration_minutes=150,
            session_status="active",
            session_notes="NEWS2 escalation during treatment",
            created_by_user_id=users[2].id,
        ),
    ]
    db.add_all(sessions)
    db.flush()

    measurements = [
        IntradialyticMeasurement(
            patient_id=patients[0].id,
            dialysis_session_id=sessions[0].id,
            measurement_time=session_start + timedelta(minutes=60),
            measurement_interval_minutes=60,
            respiratory_rate=18,
            spo2=96,
            oxygen_therapy=False,
            systolic_bp=136,
            diastolic_bp=78,
            pulse_rate=82,
            temperature=36.8,
            consciousness_level="alert",
            confusion_status="none",
            recorded_by_user_id=users[2].id,
        ),
        IntradialyticMeasurement(
            patient_id=patients[1].id,
            dialysis_session_id=sessions[1].id,
            measurement_time=session_start + timedelta(minutes=105),
            measurement_interval_minutes=30,
            respiratory_rate=24,
            spo2=91,
            oxygen_therapy=True,
            systolic_bp=92,
            diastolic_bp=58,
            pulse_rate=112,
            temperature=37.9,
            consciousness_level="alert",
            confusion_status="new_confusion",
            recorded_by_user_id=users[2].id,
        ),
    ]
    db.add_all(measurements)
    db.flush()

    stable_news2 = calculate_news2(
        NEWS2CalculationRequest(
            respiratory_rate=measurements[0].respiratory_rate,
            spo2=measurements[0].spo2,
            oxygen_therapy=measurements[0].oxygen_therapy,
            systolic_bp=measurements[0].systolic_bp,
            pulse_rate=measurements[0].pulse_rate,
            temperature=measurements[0].temperature,
            consciousness_level=measurements[0].consciousness_level,
        )
    )
    deteriorating_consciousness = (
        "new_confusion"
        if measurements[1].confusion_status == "new_confusion"
        else measurements[1].consciousness_level
    )
    deteriorating_news2 = calculate_news2(
        NEWS2CalculationRequest(
            respiratory_rate=measurements[1].respiratory_rate,
            spo2=measurements[1].spo2,
            oxygen_therapy=measurements[1].oxygen_therapy,
            systolic_bp=measurements[1].systolic_bp,
            pulse_rate=measurements[1].pulse_rate,
            temperature=measurements[1].temperature,
            consciousness_level=deteriorating_consciousness,
        )
    )

    assessments = [
        News2Assessment(
            patient_id=patients[0].id,
            dialysis_session_id=sessions[0].id,
            intradialytic_measurement_id=measurements[0].id,
            respiratory_score=stable_news2.respiratory_score,
            spo2_score=stable_news2.spo2_score,
            oxygen_score=stable_news2.oxygen_score,
            systolic_bp_score=stable_news2.systolic_bp_score,
            pulse_score=stable_news2.pulse_score,
            temperature_score=stable_news2.temperature_score,
            consciousness_score=stable_news2.consciousness_score,
            total_score=stable_news2.total_score,
            risk_level=stable_news2.risk_level,
            alert_required=stable_news2.alert_required,
            trigger_reason=stable_news2.trigger_reason,
            created_by_user_id=users[2].id,
        ),
        News2Assessment(
            patient_id=patients[1].id,
            dialysis_session_id=sessions[1].id,
            intradialytic_measurement_id=measurements[1].id,
            respiratory_score=deteriorating_news2.respiratory_score,
            spo2_score=deteriorating_news2.spo2_score,
            oxygen_score=deteriorating_news2.oxygen_score,
            systolic_bp_score=deteriorating_news2.systolic_bp_score,
            pulse_score=deteriorating_news2.pulse_score,
            temperature_score=deteriorating_news2.temperature_score,
            consciousness_score=deteriorating_news2.consciousness_score,
            total_score=deteriorating_news2.total_score,
            risk_level=deteriorating_news2.risk_level,
            alert_required=deteriorating_news2.alert_required,
            trigger_reason=deteriorating_news2.trigger_reason,
            created_by_user_id=users[2].id,
        ),
    ]
    db.add_all(assessments)
    db.flush()

    alert = Alert(
        patient_id=patients[1].id,
        dialysis_session_id=sessions[1].id,
        news2_assessment_id=assessments[1].id,
        risk_level=assessments[1].risk_level,
        severity_level=assessments[1].risk_level,
        status=AlertStatus.acknowledged,
        priority="immediate",
        trigger_reason=assessments[1].trigger_reason,
        assigned_to_user_id=users[1].id,
        created_at=measurements[1].measurement_time,
        viewed_at=measurements[1].measurement_time + timedelta(minutes=2),
        acknowledged_at=measurements[1].measurement_time + timedelta(minutes=5),
        action_taken_at=measurements[1].measurement_time + timedelta(minutes=9),
    )
    db.add(alert)
    db.flush()

    event = ClinicalDeteriorationEvent(
        patient_id=patients[1].id,
        dialysis_session_id=sessions[1].id,
        news2_assessment_id=assessments[1].id,
        alert_id=alert.id,
        deterioration_time=measurements[1].measurement_time,
        time_from_session_start_minutes=75,
        deterioration_type=DeteriorationType.acute_hypotension,
        triggering_news2_score=assessments[1].total_score,
        description="Acute intradialytic hypotension with oxygen desaturation and new confusion.",
    )
    db.add(event)
    db.flush()

    response = ClinicalResponse(
        clinical_deterioration_event_id=event.id,
        alert_id=alert.id,
        digital_alert_time=alert.created_at,
        actual_response_start_time=measurements[1].measurement_time + timedelta(minutes=9),
        response_delay_minutes=9,
        patient_actions=_json(["reposition_patient", "administer_oxygen", "reduce_ultrafiltration"]),
        vascular_access_actions=_json(["check_catheter_site", "confirm_line_patency"]),
        responded_by_user_id=users[1].id,
        notes="Fake seed record for MVP validation.",
    )
    outcome = ClinicalOutcome(
        patient_id=patients[1].id,
        dialysis_session_id=sessions[1].id,
        clinical_deterioration_event_id=event.id,
        outcome_type=OutcomeType.session_stopped_early,
        outcome_recorded_at=measurements[1].measurement_time + timedelta(hours=24),
        outcome_window_hours=24,
        description="Session stopped early; patient stabilized without hospital transfer.",
        recorded_by_user_id=users[1].id,
    )
    tracking = ResponseTracking(
        alert_id=alert.id,
        dialysis_session_id=sessions[1].id,
        news2_assessment_id=assessments[1].id,
        clinical_deterioration_event_id=event.id,
        vital_signs_recorded_at=measurements[1].measurement_time,
        alert_created_at=measurements[1].measurement_time,
        alert_viewed_at=measurements[1].measurement_time + timedelta(minutes=2),
        actual_response_start_time=measurements[1].measurement_time + timedelta(minutes=9),
        clinical_action_at=measurements[1].measurement_time + timedelta(minutes=9),
        time_to_alert_minutes=0,
        time_to_view_minutes=2,
        time_to_response_minutes=9,
        time_to_action_minutes=9,
        total_response_time_minutes=9,
    )
    db.add_all([response, outcome, tracking])

    db.add_all(
        [
            ClinicalNote(patient_id=patients[1].id, dialysis_session_id=sessions[1].id, news2_assessment_id=assessments[1].id, alert_id=alert.id, user_id=users[2].id, note_type="nursing", content="Repeat vital signs confirmed deterioration; physician notified."),
            ResearchStudy(
                study_code="NEWS2-HD-001",
                study_title="NEWS2 in Hemodialysis Clinical Deterioration Monitoring",
                study_description="PhD MVP study dataset for pre/post implementation monitoring.",
                principal_investigator="Principal Investigator",
                study_design="before_after",
                study_phase="implementation",
                study_status="active",
                study_group_a_name="Control",
                study_group_b_name="Intervention",
                baseline_period_start=date(2026, 1, 1),
                baseline_period_end=date(2026, 3, 31),
                intervention_period_start=date(2026, 4, 1),
                intervention_period_end=date(2026, 12, 31),
                study_start_date=date(2026, 1, 1),
                study_end_date=date(2026, 12, 31),
                target_sample_size=120,
                inclusion_notes="Adult hemodialysis sessions with intradialytic vital signs.",
                exclusion_notes="Incomplete anonymized identifiers or non-hemodialysis encounters.",
                notes="Governance seed record for Phase 13 readiness monitoring.",
                title="NEWS2 in Hemodialysis Clinical Deterioration Monitoring",
                description="PhD MVP study dataset for pre/post implementation monitoring.",
                start_date=date(2026, 1, 1),
                end_date=date(2026, 12, 31),
                status="active",
            ),
            AuditLog(user_id=users[0].id, action="seed_database", entity_type="system", entity_id="seed_v1", new_value="Initial fake clinical research seed data", ip_address="127.0.0.1", user_agent="python -m app.seed"),
            SystemSetting(setting_key="seed_version", setting_value="phase02_v1"),
            SystemSetting(setting_key="default_language", setting_value="ar"),
            SystemSetting(setting_key="news2_high_risk_threshold", setting_value="5"),
            SystemSetting(setting_key="outcome_window_hours", setting_value="24-72"),
        ]
    )

    db.commit()
    return {
        "status": "seeded",
        "users": len(users),
        "patients": len(patients),
        "dialysis_sessions": len(sessions),
        "measurements": len(measurements),
        "news2_assessments": len(assessments),
        "alerts": 1,
        "deterioration_events": 1,
        "responses": 1,
        "outcomes": 1,
    }


def main() -> None:
    create_database()
    db = SessionLocal()
    try:
        result = seed_database(db)
        print(result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
