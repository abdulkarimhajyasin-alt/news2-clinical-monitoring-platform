from datetime import date, datetime
from enum import StrEnum
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(StrEnum):
    admin = "admin"
    technical_admin = "technical_admin"
    doctor = "doctor"
    on_call_doctor = "on_call_doctor"
    nurse = "nurse"
    researcher = "researcher"


class StudyPhase(StrEnum):
    pre_implementation = "pre_implementation"
    post_implementation = "post_implementation"


class StudyGroup(StrEnum):
    control = "control"
    intervention = "intervention"


class ResearchStudyStatus(StrEnum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"
    archived = "archived"


class ResearchStudyDesign(StrEnum):
    observational = "observational"
    prospective = "prospective"
    retrospective = "retrospective"
    before_after = "before_after"
    cohort = "cohort"
    pilot = "pilot"


class AccessType(StrEnum):
    av_fistula = "av_fistula"
    av_graft = "av_graft"
    central_venous_catheter = "central_venous_catheter"


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AlertStatus(StrEnum):
    new = "new"
    viewed = "viewed"
    acknowledged = "acknowledged"
    in_progress = "in_progress"
    closed = "closed"
    cancelled = "cancelled"


class DeteriorationType(StrEnum):
    acute_hypotension = "acute_hypotension"
    suspected_sepsis_or_fever = "suspected_sepsis_or_fever"
    arrhythmia = "arrhythmia"
    seizures = "seizures"
    reduced_consciousness = "reduced_consciousness"
    other = "other"


class OutcomeType(StrEnum):
    stable_completed_session = "stable_completed_session"
    session_stopped_early = "session_stopped_early"
    hospital_admission = "hospital_admission"
    emergency_department_transfer = "emergency_department_transfer"
    icu_admission = "icu_admission"
    death = "death"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class LockMixin:
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    locked_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    username: Mapped[str | None] = mapped_column(String(80), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(40), nullable=False)
    department: Mapped[str | None] = mapped_column(String(120))
    job_title: Mapped[str | None] = mapped_column(String(120))
    phone: Mapped[str | None] = mapped_column(String(40))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    preferred_language: Mapped[str] = mapped_column(String(10), default="ar", nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_sessions: Mapped[list["DialysisSession"]] = relationship(back_populates="created_by", foreign_keys="DialysisSession.created_by_user_id")
    recorded_measurements: Mapped[list["IntradialyticMeasurement"]] = relationship(back_populates="recorded_by", foreign_keys="IntradialyticMeasurement.recorded_by_user_id")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")
    auth_sessions: Mapped[list["AuthSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="auth_sessions")


class Patient(Base, TimestampMixin, LockMixin):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_code: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    education_level: Mapped[str | None] = mapped_column(String(80))
    target_dry_weight: Mapped[float | None] = mapped_column(Float)
    dialysis_start_date: Mapped[date | None] = mapped_column(Date)
    dialysis_vintage_months: Mapped[int | None] = mapped_column(Integer)
    weekly_sessions_count: Mapped[int | None] = mapped_column(Integer)
    comorbidities: Mapped[str | None] = mapped_column(Text)
    comorbid_heart_failure: Mapped[bool | None] = mapped_column(Boolean)
    comorbid_diabetes: Mapped[bool | None] = mapped_column(Boolean)
    comorbid_hypertension: Mapped[bool | None] = mapped_column(Boolean)
    comorbidities_notes: Mapped[str | None] = mapped_column(Text)
    charlson_comorbidity_index: Mapped[int | None] = mapped_column(Integer)
    baseline_functional_status: Mapped[str | None] = mapped_column(Text)
    vascular_access_type: Mapped[str | None] = mapped_column(String(60))
    vascular_access_location: Mapped[str | None] = mapped_column(String(120))
    vascular_access_placement_date: Mapped[date | None] = mapped_column(Date)
    study_phase: Mapped[str] = mapped_column(String(40), nullable=False)
    study_group: Mapped[str] = mapped_column(String(40), nullable=False)
    is_anonymized: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    discharged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    discharge_reason: Mapped[str | None] = mapped_column(String(255))
    discharge_notes: Mapped[str | None] = mapped_column(Text)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    archived_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    delete_reason: Mapped[str | None] = mapped_column(Text)

    vascular_access: Mapped[list["PatientVascularAccess"]] = relationship(back_populates="patient")
    dialysis_sessions: Mapped[list["DialysisSession"]] = relationship(back_populates="patient")
    measurements: Mapped[list["IntradialyticMeasurement"]] = relationship(back_populates="patient")
    news2_assessments: Mapped[list["News2Assessment"]] = relationship(back_populates="patient")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="patient")
    deterioration_events: Mapped[list["ClinicalDeteriorationEvent"]] = relationship(back_populates="patient")
    outcomes: Mapped[list["ClinicalOutcome"]] = relationship(back_populates="patient")

    @property
    def medical_code(self) -> str:
        return self.patient_code

    @property
    def dry_weight_kg(self) -> float | None:
        return self.target_dry_weight

    @property
    def weekly_dialysis_sessions(self) -> int | None:
        return self.weekly_sessions_count


class PatientVascularAccess(Base, TimestampMixin, LockMixin):
    __tablename__ = "patient_vascular_access"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    access_type: Mapped[str] = mapped_column(String(60), nullable=False)
    access_location: Mapped[str | None] = mapped_column(String(120))
    inserted_at: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)

    patient: Mapped[Patient] = relationship(back_populates="vascular_access")


class DialysisSession(Base, TimestampMixin, LockMixin):
    __tablename__ = "dialysis_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    weekday: Mapped[str | None] = mapped_column(String(20))
    actual_start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    target_ultrafiltration: Mapped[float | None] = mapped_column(Float)
    target_fluid_removal_ml: Mapped[float | None] = mapped_column(Float)
    blood_flow_rate: Mapped[int | None] = mapped_column(Integer)
    dialysate_flow_rate: Mapped[int | None] = mapped_column(Integer)
    dialysate_temperature: Mapped[float | None] = mapped_column(Float)
    ultrafiltration_rate: Mapped[float | None] = mapped_column(Float)
    ultrafiltration_volume: Mapped[float | None] = mapped_column(Float)
    session_duration_minutes: Mapped[int | None] = mapped_column(Integer)
    session_status: Mapped[str] = mapped_column(String(40), default="scheduled", nullable=False)
    session_notes: Mapped[str | None] = mapped_column(Text)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    patient: Mapped[Patient] = relationship(back_populates="dialysis_sessions")
    created_by: Mapped[User | None] = relationship(back_populates="created_sessions", foreign_keys=[created_by_user_id])
    measurements: Mapped[list["IntradialyticMeasurement"]] = relationship(back_populates="dialysis_session")
    news2_assessments: Mapped[list["News2Assessment"]] = relationship(back_populates="dialysis_session")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="dialysis_session")

    @property
    def session_day_of_week(self) -> str | None:
        return self.weekday


class IntradialyticMeasurement(Base):
    __tablename__ = "intradialytic_measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False, index=True)
    measurement_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    measurement_interval_minutes: Mapped[int | None] = mapped_column(Integer)
    respiratory_rate: Mapped[int | None] = mapped_column(Integer)
    spo2: Mapped[int | None] = mapped_column(Integer)
    oxygen_therapy: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    systolic_bp: Mapped[int | None] = mapped_column(Integer)
    diastolic_bp: Mapped[int | None] = mapped_column(Integer)
    pulse_rate: Mapped[int | None] = mapped_column(Integer)
    temperature: Mapped[float | None] = mapped_column(Float)
    consciousness_level: Mapped[str | None] = mapped_column(String(80))
    confusion_status: Mapped[str | None] = mapped_column(String(80))
    vascular_access_status: Mapped[str | None] = mapped_column(String(40))
    pre_dialysis_weight: Mapped[float | None] = mapped_column(Float)
    dry_weight: Mapped[float | None] = mapped_column(Float)
    session_duration_hours: Mapped[float | None] = mapped_column(Float)
    fluid_to_remove: Mapped[float | None] = mapped_column(Float)
    potassium: Mapped[float | None] = mapped_column(Float)
    idwg_percent: Mapped[float | None] = mapped_column(Float)
    ufr: Mapped[float | None] = mapped_column(Float)
    sbp_symptomatic_hypotension: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recorded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="measurements")
    dialysis_session: Mapped[DialysisSession] = relationship(back_populates="measurements")
    recorded_by: Mapped[User | None] = relationship(back_populates="recorded_measurements", foreign_keys=[recorded_by_user_id])
    news2_assessment: Mapped["News2Assessment | None"] = relationship(back_populates="measurement")

    @property
    def hd2_mnews_total_score(self) -> int | None:
        return self.news2_assessment.hd2_mnews_total_score if self.news2_assessment else None

    @property
    def hd2_mnews_risk_color(self) -> str | None:
        return self.news2_assessment.hd2_mnews_risk_color if self.news2_assessment else None

    @property
    def hd2_mnews_risk_label_ar(self) -> str | None:
        return self.news2_assessment.hd2_mnews_risk_label_ar if self.news2_assessment else None

    @property
    def hd2_reassessment_interval_min(self) -> int | None:
        return self.news2_assessment.hd2_reassessment_interval_min if self.news2_assessment else None

    @property
    def hd2_reassessment_interval_max(self) -> int | None:
        return self.news2_assessment.hd2_reassessment_interval_max if self.news2_assessment else None

    @property
    def hd2_required_response_time_minutes(self) -> int | None:
        return self.news2_assessment.hd2_required_response_time_minutes if self.news2_assessment else None


class News2Assessment(Base):
    __tablename__ = "news2_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False, index=True)
    intradialytic_measurement_id: Mapped[int] = mapped_column(ForeignKey("intradialytic_measurements.id"), nullable=False, unique=True)
    respiratory_score: Mapped[int] = mapped_column(Integer, nullable=False)
    spo2_score: Mapped[int] = mapped_column(Integer, nullable=False)
    oxygen_score: Mapped[int] = mapped_column(Integer, nullable=False)
    systolic_bp_score: Mapped[int] = mapped_column(Integer, nullable=False)
    pulse_score: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature_score: Mapped[int] = mapped_column(Integer, nullable=False)
    consciousness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    alert_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    trigger_reason: Mapped[str | None] = mapped_column(Text)
    hd2_mnews_total_score: Mapped[int | None] = mapped_column(Integer)
    hd2_mnews_risk_color: Mapped[str | None] = mapped_column(String(40))
    hd2_mnews_risk_label_ar: Mapped[str | None] = mapped_column(String(80))
    hd2_mnews_critical_trigger: Mapped[bool | None] = mapped_column(Boolean)
    hd2_mnews_critical_reasons: Mapped[str | None] = mapped_column(Text)
    hd2_mnews_breakdown_json: Mapped[str | None] = mapped_column(Text)
    hd2_protocol_json: Mapped[str | None] = mapped_column(Text)
    hd2_reassessment_interval_min: Mapped[int | None] = mapped_column(Integer)
    hd2_reassessment_interval_max: Mapped[int | None] = mapped_column(Integer)
    hd2_required_response_time_minutes: Mapped[int | None] = mapped_column(Integer)
    hd2_requires_physician_call: Mapped[bool | None] = mapped_column(Boolean)
    hd2_requires_emergency_preparation: Mapped[bool | None] = mapped_column(Boolean)
    hd2_requires_close_monitoring: Mapped[bool | None] = mapped_column(Boolean)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="news2_assessments")
    dialysis_session: Mapped[DialysisSession] = relationship(back_populates="news2_assessments")
    measurement: Mapped[IntradialyticMeasurement] = relationship(back_populates="news2_assessment")
    alert: Mapped["Alert | None"] = relationship(back_populates="news2_assessment")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False, index=True)
    news2_assessment_id: Mapped[int] = mapped_column(ForeignKey("news2_assessments.id"), nullable=False, unique=True)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    severity_level: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="new", nullable=False)
    priority: Mapped[str | None] = mapped_column(String(40))
    trigger_reason: Mapped[str | None] = mapped_column(Text)
    assigned_to_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    action_taken_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    patient: Mapped[Patient] = relationship(back_populates="alerts")
    dialysis_session: Mapped[DialysisSession] = relationship(back_populates="alerts")
    news2_assessment: Mapped[News2Assessment] = relationship(back_populates="alert")
    deterioration_event: Mapped["ClinicalDeteriorationEvent | None"] = relationship(back_populates="alert")
    response_tracking: Mapped["ResponseTracking | None"] = relationship(back_populates="alert")


class ClinicalDeteriorationEvent(Base, TimestampMixin, LockMixin):
    __tablename__ = "clinical_deterioration_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False, index=True)
    news2_assessment_id: Mapped[int] = mapped_column(ForeignKey("news2_assessments.id"), nullable=False)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), nullable=False, unique=True)
    deterioration_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    time_from_session_start_minutes: Mapped[int | None] = mapped_column(Integer)
    deterioration_type: Mapped[str] = mapped_column(String(80), nullable=False)
    triggering_news2_score: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    patient: Mapped[Patient] = relationship(back_populates="deterioration_events")
    alert: Mapped[Alert] = relationship(back_populates="deterioration_event")
    clinical_response: Mapped["ClinicalResponse | None"] = relationship(back_populates="clinical_deterioration_event")
    outcomes: Mapped[list["ClinicalOutcome"]] = relationship(back_populates="clinical_deterioration_event")


class ClinicalResponse(Base, TimestampMixin, LockMixin):
    __tablename__ = "clinical_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    clinical_deterioration_event_id: Mapped[int] = mapped_column(ForeignKey("clinical_deterioration_events.id"), nullable=False, unique=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), nullable=False)
    digital_alert_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_response_start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    response_delay_minutes: Mapped[int | None] = mapped_column(Integer)
    patient_actions: Mapped[str | None] = mapped_column(Text)
    vascular_access_actions: Mapped[str | None] = mapped_column(Text)
    responded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    notes: Mapped[str | None] = mapped_column(Text)

    clinical_deterioration_event: Mapped[ClinicalDeteriorationEvent] = relationship(back_populates="clinical_response")


class ResponseTracking(Base, TimestampMixin):
    __tablename__ = "response_tracking"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), nullable=False, unique=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False)
    news2_assessment_id: Mapped[int] = mapped_column(ForeignKey("news2_assessments.id"), nullable=False)
    clinical_deterioration_event_id: Mapped[int] = mapped_column(ForeignKey("clinical_deterioration_events.id"), nullable=False)
    vital_signs_recorded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    alert_created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    alert_viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_response_start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    clinical_action_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    alert_closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    time_to_alert_minutes: Mapped[int | None] = mapped_column(Integer)
    time_to_view_minutes: Mapped[int | None] = mapped_column(Integer)
    time_to_response_minutes: Mapped[int | None] = mapped_column(Integer)
    time_to_action_minutes: Mapped[int | None] = mapped_column(Integer)
    total_response_time_minutes: Mapped[int | None] = mapped_column(Integer)

    alert: Mapped[Alert] = relationship(back_populates="response_tracking")


class ClinicalOutcome(Base):
    __tablename__ = "clinical_outcomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False)
    clinical_deterioration_event_id: Mapped[int] = mapped_column(ForeignKey("clinical_deterioration_events.id"), nullable=False)
    outcome_type: Mapped[str] = mapped_column(String(80), nullable=False)
    outcome_recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    outcome_window_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    recorded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    locked_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="outcomes")
    clinical_deterioration_event: Mapped[ClinicalDeteriorationEvent] = relationship(back_populates="outcomes")


class OutcomeValidation72h(Base, TimestampMixin):
    __tablename__ = "outcome_validations_72h"
    __table_args__ = (UniqueConstraint("dialysis_session_id", name="uq_outcome_validations_72h_session"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    dialysis_session_id: Mapped[int] = mapped_column(ForeignKey("dialysis_sessions.id"), nullable=False, index=True)
    deterioration_occurred: Mapped[bool] = mapped_column(Boolean, nullable=False)
    deterioration_types: Mapped[str | None] = mapped_column(Text)
    type_specific_details: Mapped[str | None] = mapped_column(Text)
    deterioration_timing_category: Mapped[str | None] = mapped_column(String(80))
    deterioration_time: Mapped[str | None] = mapped_column(String(20))
    deterioration_datetime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    platform_prediction_status: Mapped[str | None] = mapped_column(String(80))
    interventions: Mapped[str | None] = mapped_column(Text)
    doctor_response_time_minutes: Mapped[int | None] = mapped_column(Integer)
    final_result: Mapped[str | None] = mapped_column(String(80))
    verification_sources: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    completed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ClinicalNote(Base, TimestampMixin):
    __tablename__ = "clinical_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int | None] = mapped_column(ForeignKey("patients.id"))
    dialysis_session_id: Mapped[int | None] = mapped_column(ForeignKey("dialysis_sessions.id"))
    news2_assessment_id: Mapped[int | None] = mapped_column(ForeignKey("news2_assessments.id"))
    alert_id: Mapped[int | None] = mapped_column(ForeignKey("alerts.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    note_type: Mapped[str] = mapped_column(String(60), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class ResearchStudy(Base, TimestampMixin):
    __tablename__ = "research_studies"

    id: Mapped[int] = mapped_column(primary_key=True)
    study_code: Mapped[str | None] = mapped_column(String(80), unique=True, index=True)
    study_title: Mapped[str | None] = mapped_column(String(255))
    study_description: Mapped[str | None] = mapped_column(Text)
    principal_investigator: Mapped[str | None] = mapped_column(String(160))
    study_design: Mapped[str | None] = mapped_column(String(80))
    study_phase: Mapped[str | None] = mapped_column(String(80))
    study_status: Mapped[str] = mapped_column(String(40), default=ResearchStudyStatus.draft, nullable=False)
    study_group_a_name: Mapped[str | None] = mapped_column(String(160))
    study_group_b_name: Mapped[str | None] = mapped_column(String(160))
    baseline_period_start: Mapped[date | None] = mapped_column(Date)
    baseline_period_end: Mapped[date | None] = mapped_column(Date)
    intervention_period_start: Mapped[date | None] = mapped_column(Date)
    intervention_period_end: Mapped[date | None] = mapped_column(Date)
    study_start_date: Mapped[date | None] = mapped_column(Date)
    study_end_date: Mapped[date | None] = mapped_column(Date)
    target_sample_size: Mapped[int | None] = mapped_column(Integer)
    inclusion_notes: Mapped[str | None] = mapped_column(Text)
    exclusion_notes: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(40), default=ResearchStudyStatus.draft)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(80))
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    ip_address: Mapped[str | None] = mapped_column(String(80))
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped[User | None] = relationship(back_populates="audit_logs")


class SystemSetting(Base, TimestampMixin):
    __tablename__ = "system_settings"
    __table_args__ = (UniqueConstraint("setting_key", name="uq_system_settings_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    setting_key: Mapped[str] = mapped_column(String(120), nullable=False)
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
