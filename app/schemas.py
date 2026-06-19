from datetime import date, datetime, time
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.rbac import ROLE_PERMISSIONS


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str
    department: str | None = None
    status: str
    preferred_language: str


class StaffUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    username: str | None = None
    email: str
    phone: str | None = None
    department: str | None = None
    job_title: str | None = None
    role: str
    is_active: bool
    status: str
    created_at: datetime
    updated_at: datetime


class StaffUserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    username: str = Field(min_length=2, max_length=80)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    department: str | None = Field(default=None, max_length=120)
    job_title: str | None = Field(default=None, max_length=120)
    role: str
    temporary_password: str = Field(min_length=8, max_length=256)
    is_active: bool = True

    @field_validator("full_name", "username", "phone", "department", "job_title", "role", "temporary_password")
    @classmethod
    def strip_staff_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    @field_validator("email")
    @classmethod
    def validate_staff_email(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("invalid email")
        return value

    @field_validator("role")
    @classmethod
    def validate_staff_role(cls, value: str) -> str:
        if value not in ROLE_PERMISSIONS:
            raise ValueError("invalid role")
        return value


class StaffUserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=160)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    department: str | None = Field(default=None, max_length=120)
    job_title: str | None = Field(default=None, max_length=120)
    role: str | None = None
    is_active: bool | None = None

    @field_validator("full_name", "phone", "department", "job_title", "role")
    @classmethod
    def strip_update_staff_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    @field_validator("email")
    @classmethod
    def validate_update_staff_email(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("invalid email")
        return value

    @field_validator("role")
    @classmethod
    def validate_update_staff_role(cls, value: str | None) -> str | None:
        if value is not None and value not in ROLE_PERMISSIONS:
            raise ValueError("invalid role")
        return value


class StaffUserStatusUpdate(BaseModel):
    is_active: bool


class StaffUserCreateResult(BaseModel):
    user: StaffUserRead
    user_created: bool
    message: str


class AuthLoginRequest(BaseModel):
    username_or_email: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=256)

    @field_validator("username_or_email")
    @classmethod
    def normalize_identifier(cls, value: str) -> str:
        return value.strip().lower()


class AuthenticatedUserRead(BaseModel):
    id: int | None = None
    full_name: str | None = None
    username: str | None = None
    email: str | None = None
    role: str
    role_label: str
    permissions: list[str]
    is_dev_context: bool = False
    allow_dev_role: bool = False


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_code: str
    medical_code: str | None = None
    full_name: str
    age: int
    gender: str
    education_level: str | None = None
    target_dry_weight: float | None = None
    dry_weight_kg: float | None = None
    dialysis_start_date: date | None = None
    weekly_sessions_count: int | None = None
    weekly_dialysis_sessions: int | None = None
    comorbidities: str | None = None
    comorbid_heart_failure: bool | None = None
    comorbid_diabetes: bool | None = None
    comorbid_hypertension: bool | None = None
    comorbidities_notes: str | None = None
    vascular_access_type: str | None = None
    vascular_access_location: str | None = None
    vascular_access_placement_date: date | None = None
    study_phase: str
    study_group: str
    dialysis_vintage_months: int | None = None
    baseline_functional_status: str | None = None
    is_anonymized: bool
    status: str = "active"
    discharged_at: datetime | None = None
    discharge_reason: str | None = None
    discharge_notes: str | None = None
    archived_at: datetime | None = None
    archived_by_user_id: int | None = None
    deleted_at: datetime | None = None
    deleted_by_user_id: int | None = None
    delete_reason: str | None = None


class PatientCreate(BaseModel):
    patient_code: str = Field(min_length=2, max_length=80)
    full_name: str = Field(min_length=2, max_length=160)
    age: int = Field(ge=0, le=130)
    gender: Literal["male", "female"]
    education_level: str | None = Field(default=None, max_length=80)
    target_dry_weight: float | None = Field(default=None, gt=0, le=500)
    dry_weight_kg: float | None = Field(default=None, gt=0, le=500)
    dialysis_start_date: date | None = None
    dialysis_vintage_months: int | None = Field(default=None, ge=0, le=1200)
    weekly_sessions_count: int | None = Field(default=3, ge=1, le=7)
    weekly_dialysis_sessions: int | None = Field(default=None, ge=1, le=7)
    comorbidities: str | None = Field(default=None, max_length=4000)
    comorbid_heart_failure: bool | None = None
    comorbid_diabetes: bool | None = None
    comorbid_hypertension: bool | None = None
    comorbidities_notes: str | None = Field(default=None, max_length=4000)
    charlson_comorbidity_index: int | None = Field(default=None, ge=0, le=40)
    baseline_functional_status: str | None = Field(default=None, max_length=4000)
    vascular_access_type: Literal["av_fistula", "av_graft", "cvc", "central_venous_catheter"] | None = None
    vascular_access_location: str | None = Field(default=None, max_length=120)
    vascular_access_placement_date: date | None = None
    study_phase: Literal["pre_implementation", "post_implementation"] = "post_implementation"
    study_group: Literal["control", "intervention"] = "intervention"
    is_anonymized: bool = True

    @field_validator("patient_code")
    @classmethod
    def normalize_patient_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("full_name", "education_level", "comorbidities", "comorbidities_notes", "baseline_functional_status", "vascular_access_location")
    @classmethod
    def strip_patient_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if self.dry_weight_kg is not None and self.target_dry_weight is None:
            self.target_dry_weight = self.dry_weight_kg
        if self.weekly_dialysis_sessions is not None:
            self.weekly_sessions_count = self.weekly_dialysis_sessions
        if self.vascular_access_type == "cvc":
            self.vascular_access_type = "central_venous_catheter"


class PatientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=160)
    age: int | None = Field(default=None, ge=0, le=130)
    gender: Literal["male", "female"] | None = None
    education_level: str | None = Field(default=None, max_length=80)
    target_dry_weight: float | None = Field(default=None, gt=0, le=500)
    dry_weight_kg: float | None = Field(default=None, gt=0, le=500)
    dialysis_start_date: date | None = None
    dialysis_vintage_months: int | None = Field(default=None, ge=0, le=1200)
    weekly_sessions_count: int | None = Field(default=None, ge=1, le=7)
    weekly_dialysis_sessions: int | None = Field(default=None, ge=1, le=7)
    comorbidities: str | None = Field(default=None, max_length=4000)
    comorbid_heart_failure: bool | None = None
    comorbid_diabetes: bool | None = None
    comorbid_hypertension: bool | None = None
    comorbidities_notes: str | None = Field(default=None, max_length=4000)
    charlson_comorbidity_index: int | None = Field(default=None, ge=0, le=40)
    baseline_functional_status: str | None = Field(default=None, max_length=4000)
    vascular_access_type: Literal["av_fistula", "av_graft", "cvc", "central_venous_catheter"] | None = None
    vascular_access_location: str | None = Field(default=None, max_length=120)
    vascular_access_placement_date: date | None = None

    @field_validator("full_name", "education_level", "comorbidities", "comorbidities_notes", "baseline_functional_status", "vascular_access_location")
    @classmethod
    def strip_update_patient_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if self.dry_weight_kg is not None and self.target_dry_weight is None:
            self.target_dry_weight = self.dry_weight_kg
        if self.weekly_dialysis_sessions is not None:
            self.weekly_sessions_count = self.weekly_dialysis_sessions
        if self.vascular_access_type == "cvc":
            self.vascular_access_type = "central_venous_catheter"


class PatientCreateResult(BaseModel):
    patient: PatientRead
    patient_created: bool
    message: str


class PatientDischargeRequest(BaseModel):
    discharge_reason: str = Field(min_length=2, max_length=255)
    discharge_notes: str | None = Field(default=None, max_length=4000)

    @field_validator("discharge_reason", "discharge_notes")
    @classmethod
    def strip_discharge_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value


class PatientArchiveRequest(BaseModel):
    archive_reason: str | None = Field(default=None, max_length=255)

    @field_validator("archive_reason")
    @classmethod
    def strip_archive_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value


class PatientDeleteRequest(BaseModel):
    delete_reason: str = Field(min_length=2, max_length=4000)
    confirmation_text: str

    @field_validator("delete_reason", "confirmation_text")
    @classmethod
    def strip_delete_text(cls, value: str) -> str:
        return value.strip()


class PatientLifecycleResult(BaseModel):
    patient: PatientRead
    message: str


class DialysisSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    patient_code: str | None = None
    session_date: date
    weekday: str | None = None
    session_day_of_week: str | None = None
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    session_status: str
    target_ultrafiltration: float | None = None
    target_fluid_removal_ml: float | None = None
    session_duration_minutes: int | None = None


class DialysisSessionCreate(BaseModel):
    patient_id: int = Field(gt=0)
    session_date: date
    weekday: str | None = Field(default=None, max_length=20)
    session_day_of_week: str | None = Field(default=None, max_length=20)
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    session_status: str = Field(default="scheduled", max_length=40)
    target_ultrafiltration: float | None = Field(default=None, ge=0, le=100)
    target_fluid_removal_ml: float | None = Field(default=None, ge=0, le=10000)
    session_duration_minutes: int | None = Field(default=None, ge=1, le=1440)

    @field_validator("weekday", "session_day_of_week", "session_status")
    @classmethod
    def strip_session_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if self.session_day_of_week and not self.weekday:
            self.weekday = self.session_day_of_week


class DialysisSessionUpdate(BaseModel):
    session_date: date | None = None
    weekday: str | None = Field(default=None, max_length=20)
    session_day_of_week: str | None = Field(default=None, max_length=20)
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    session_status: str | None = Field(default=None, max_length=40)
    target_ultrafiltration: float | None = Field(default=None, ge=0, le=100)
    target_fluid_removal_ml: float | None = Field(default=None, ge=0, le=10000)
    session_duration_minutes: int | None = Field(default=None, ge=1, le=1440)

    @field_validator("weekday", "session_day_of_week", "session_status")
    @classmethod
    def strip_update_session_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if self.session_day_of_week and not self.weekday:
            self.weekday = self.session_day_of_week


class AlertRead(BaseModel):
    id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    news2_assessment_id: int | None = None
    risk_level: str
    severity_level: str
    status: str
    priority: str | None = None
    trigger_reason: str | None = None
    created_at: datetime
    viewed_at: datetime | None = None
    acknowledged_at: datetime | None = None
    action_taken_at: datetime | None = None
    closed_at: datetime | None = None


class ResearchSummary(BaseModel):
    patients_count: int
    sessions_count: int
    measurements_count: int
    news2_assessments_count: int
    alerts_count: int
    active_alerts_count: int
    deterioration_events_count: int
    acute_hypotension_count: int = 0
    suspected_sepsis_or_fever_count: int = 0
    arrhythmia_count: int = 0
    seizures_count: int = 0
    reduced_consciousness_count: int = 0
    responses_count: int
    clinical_responses_count: int = 0
    average_response_delay_minutes: float | None = None
    fastest_response_delay_minutes: int | None = None
    slowest_response_delay_minutes: int | None = None
    average_time_to_alert_minutes: float | None = None
    average_time_to_response_minutes: float | None = None
    fastest_response_minutes: int | None = None
    slowest_response_minutes: int | None = None
    alerts_without_response_count: int = 0
    outcomes_count: int
    total_outcomes: int = 0
    stable_completed_session_count: int = 0
    session_stopped_early_count: int = 0
    hospital_admission_count: int = 0
    emergency_department_transfer_count: int = 0
    icu_admission_count: int = 0
    death_count: int = 0
    research_dataset_rows: int = 0
    dataset_quality_score: int = 0
    missing_outcomes_count: int = 0
    export_readiness: str = "not_ready"
    average_news2: float | None = None


class NEWS2CalculationRequest(BaseModel):
    respiratory_rate: int = Field(gt=0, le=80)
    spo2: int = Field(ge=0, le=100)
    oxygen_therapy: bool = False
    systolic_bp: int = Field(gt=0, le=300)
    pulse_rate: int = Field(gt=0, le=300)
    temperature: float = Field(ge=25.0, le=45.0)
    consciousness_level: Literal["alert", "voice", "pain", "unresponsive", "new_confusion"]
    spo2_scale: Literal["scale_1", "scale_2"] = "scale_1"

    @field_validator("temperature")
    @classmethod
    def validate_temperature_precision(cls, value: float) -> float:
        return round(value, 1)


class NEWS2ComponentScores(BaseModel):
    respiratory_score: int
    spo2_score: int
    oxygen_score: int
    systolic_bp_score: int
    pulse_score: int
    temperature_score: int
    consciousness_score: int


class NEWS2CalculationResult(NEWS2ComponentScores):
    total_score: int
    risk_level: Literal["low", "medium", "high"]
    alert_required: bool
    single_parameter_trigger: bool
    trigger_reason: str


class HD2MNEWSCalculationRequest(BaseModel):
    respiratory_rate: int = Field(gt=0, le=80)
    oxygen_saturation: int = Field(ge=0, le=100)
    temperature: float = Field(ge=25.0, le=45.0)
    systolic_bp: int = Field(gt=0, le=300)
    heart_rate: int = Field(gt=0, le=300)
    consciousness_level: Literal["alert", "voice", "pain", "unresponsive", "new_confusion"]
    vascular_access_status: Literal["normal", "weak", "disturbed", "critical"]
    pre_dialysis_weight: float = Field(gt=0, le=500)
    dry_weight: float = Field(gt=0, le=500)
    session_duration_hours: float = Field(gt=0, le=24)
    fluid_to_remove: float = Field(ge=0, le=10000)
    potassium: float = Field(gt=0, le=12)
    sbp_symptomatic_hypotension: bool = False

    @field_validator("temperature", "pre_dialysis_weight", "dry_weight", "session_duration_hours", "fluid_to_remove", "potassium")
    @classmethod
    def validate_hd2_numeric_precision(cls, value: float) -> float:
        return round(value, 2)


class HD2MNEWSComponentScores(BaseModel):
    respiratory_rate_score: int
    oxygen_saturation_score: int
    temperature_score: int
    systolic_bp_score: int
    heart_rate_score: int
    consciousness_score: int
    vascular_access_score: int
    idwg_score: int
    ufr_score: int
    potassium_score: int


class HD2MNEWSCalculationResult(HD2MNEWSComponentScores):
    idwg_percent: float
    ufr: float
    hd2_mnews_total_score: int
    hd2_mnews_risk_color: Literal["green", "yellow", "red"]
    hd2_mnews_risk_label_ar: str
    hd2_mnews_critical_trigger: bool
    hd2_mnews_critical_reasons: list[str] = Field(default_factory=list)
    nursing_protocol: dict[str, object] | None = None
    reassessment_interval_label_ar: str | None = None
    required_response_time_label_ar: str | None = None
    protocol_actions_ar: list[str] = Field(default_factory=list)


class MonitoringMeasurementCreate(BaseModel):
    patient_id: int = Field(gt=0)
    dialysis_session_id: int = Field(gt=0)
    measurement_time: datetime
    measurement_interval_minutes: int = Field(gt=0, le=1440)
    respiratory_rate: int = Field(gt=0, le=80)
    spo2: int = Field(ge=0, le=100)
    oxygen_therapy: bool = False
    systolic_bp: int = Field(gt=0, le=300)
    diastolic_bp: int = Field(gt=0, le=200)
    pulse_rate: int = Field(gt=0, le=300)
    temperature: float = Field(ge=25.0, le=45.0)
    consciousness_level: Literal["alert", "voice", "pain", "unresponsive", "new_confusion"]
    confusion_status: bool | str | None = None
    spo2_scale: Literal["scale_1", "scale_2"] = "scale_1"
    vascular_access_status: Literal["normal", "weak", "disturbed", "critical"] | None = None
    pre_dialysis_weight: float | None = Field(default=None, gt=0, le=500)
    dry_weight: float | None = Field(default=None, gt=0, le=500)
    session_duration_hours: float | None = Field(default=None, gt=0, le=24)
    fluid_to_remove: float | None = Field(default=None, ge=0, le=10000)
    potassium: float | None = Field(default=None, gt=0, le=12)
    sbp_symptomatic_hypotension: bool = False
    recorded_by_user_id: int | None = Field(default=None, gt=0)

    @field_validator("temperature", "pre_dialysis_weight", "dry_weight", "session_duration_hours", "fluid_to_remove", "potassium")
    @classmethod
    def validate_monitoring_numeric_precision(cls, value: float | None) -> float | None:
        return round(value, 2) if value is not None else value


class MonitoringMeasurementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    dialysis_session_id: int
    measurement_time: datetime
    measurement_interval_minutes: int | None = None
    respiratory_rate: int | None = None
    spo2: int | None = None
    oxygen_therapy: bool
    systolic_bp: int | None = None
    diastolic_bp: int | None = None
    pulse_rate: int | None = None
    temperature: float | None = None
    consciousness_level: str | None = None
    confusion_status: str | None = None
    vascular_access_status: str | None = None
    pre_dialysis_weight: float | None = None
    dry_weight: float | None = None
    session_duration_hours: float | None = None
    fluid_to_remove: float | None = None
    potassium: float | None = None
    idwg_percent: float | None = None
    ufr: float | None = None
    sbp_symptomatic_hypotension: bool = False
    hd2_mnews_total_score: int | None = None
    hd2_mnews_risk_color: str | None = None
    hd2_mnews_risk_label_ar: str | None = None
    hd2_reassessment_interval_min: int | None = None
    hd2_reassessment_interval_max: int | None = None
    hd2_required_response_time_minutes: int | None = None
    recorded_by_user_id: int | None = None
    created_at: datetime


class NEWS2AssessmentRead(NEWS2ComponentScores):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    dialysis_session_id: int
    intradialytic_measurement_id: int
    total_score: int
    risk_level: str
    alert_required: bool
    single_parameter_trigger: bool = False
    trigger_reason: str | None = None
    hd2_mnews_total_score: int | None = None
    hd2_mnews_risk_color: str | None = None
    hd2_mnews_risk_label_ar: str | None = None
    hd2_mnews_critical_trigger: bool | None = None
    hd2_mnews_critical_reasons: list[str] = Field(default_factory=list)
    hd2_mnews_breakdown: dict[str, object] | None = None
    hd2_protocol: dict[str, object] | None = None
    hd2_reassessment_interval_min: int | None = None
    hd2_reassessment_interval_max: int | None = None
    hd2_required_response_time_minutes: int | None = None
    hd2_requires_physician_call: bool | None = None
    hd2_requires_emergency_preparation: bool | None = None
    hd2_requires_close_monitoring: bool | None = None
    hd2_protocol_summary_ar: str | None = None
    created_by_user_id: int | None = None
    created_at: datetime


class MonitoringMeasurementResult(BaseModel):
    measurement: MonitoringMeasurementRead
    news2_assessment: NEWS2AssessmentRead
    alert: "AlertCreationResult | None" = None
    message: str


class AlertCreationResult(BaseModel):
    alert_created: bool
    alert_id: int | None = None
    reused_existing: bool = False
    status: str | None = None
    risk_level: str | None = None
    severity_level: str | None = None
    priority: str | None = None
    trigger_reason: str | None = None


class ClinicalDeteriorationEventCreate(BaseModel):
    alert_id: int = Field(gt=0)
    deterioration_time: datetime
    deterioration_type: Literal[
        "acute_hypotension",
        "suspected_sepsis_or_fever",
        "arrhythmia",
        "seizures",
        "reduced_consciousness",
        "other",
    ]
    description: str | None = Field(default=None, max_length=4000)
    created_by_user_id: int | None = Field(default=None, gt=0)


class ClinicalDeteriorationEventRead(BaseModel):
    id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    session_date: date | None = None
    news2_assessment_id: int
    news2_total_score: int
    alert_id: int
    alert_status: str
    risk_level: str | None = None
    deterioration_time: datetime
    time_from_session_start_minutes: int | None = None
    deterioration_type: str
    triggering_news2_score: int
    description: str | None = None
    is_locked: bool
    locked_at: datetime | None = None
    locked_by_user_id: int | None = None
    created_at: datetime
    updated_at: datetime


class ClinicalDeteriorationEventResult(BaseModel):
    event: ClinicalDeteriorationEventRead
    event_created: bool
    message: str


PatientAction = Literal[
    "stop_ultrafiltration",
    "give_fluids",
    "give_oxygen",
    "position_adjustment",
    "medication_given",
    "doctor_called",
    "transfer_prepared",
    "other",
]

VascularAccessAction = Literal[
    "check_flow",
    "inspect_access_site",
    "blood_culture_from_catheter",
    "catheter_evaluation",
    "other",
]


class ClinicalResponseCreate(BaseModel):
    clinical_deterioration_event_id: int = Field(gt=0)
    actual_response_start_time: datetime
    patient_actions: list[PatientAction] = Field(default_factory=list)
    vascular_access_actions: list[VascularAccessAction] = Field(default_factory=list)
    responded_by_user_id: int | None = Field(default=None, gt=0)
    notes: str | None = Field(default=None, max_length=4000)


class ClinicalResponseRead(BaseModel):
    id: int
    clinical_deterioration_event_id: int
    alert_id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    session_date: date | None = None
    news2_total_score: int | None = None
    deterioration_type: str | None = None
    digital_alert_time: datetime | None = None
    actual_response_start_time: datetime | None = None
    response_delay_minutes: int | None = None
    patient_actions: list[str]
    vascular_access_actions: list[str]
    responded_by_user_id: int | None = None
    notes: str | None = None
    is_locked: bool
    locked_at: datetime | None = None
    locked_by_user_id: int | None = None
    created_at: datetime
    updated_at: datetime


class ClinicalResponseResult(BaseModel):
    response: ClinicalResponseRead
    response_created: bool
    message: str


class ResponseTrackingRead(BaseModel):
    id: int
    alert_id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    session_date: date | None = None
    news2_assessment_id: int
    news2_total_score: int | None = None
    risk_level: str | None = None
    clinical_deterioration_event_id: int
    deterioration_type: str | None = None
    deterioration_event_created_at: datetime | None = None
    vital_signs_recorded_at: datetime | None = None
    alert_created_at: datetime | None = None
    alert_viewed_at: datetime | None = None
    actual_response_start_time: datetime | None = None
    clinical_action_at: datetime | None = None
    alert_closed_at: datetime | None = None
    time_to_alert_minutes: int | None = None
    time_to_view_minutes: int | None = None
    time_to_response_minutes: int | None = None
    time_to_action_minutes: int | None = None
    total_response_time_minutes: int | None = None
    warnings: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ResponseTrackingResult(BaseModel):
    tracking: ResponseTrackingRead
    tracking_created: bool
    warnings: list[str] = Field(default_factory=list)
    message: str


class ResponseTrackingSummary(BaseModel):
    records_count: int
    average_time_to_alert_minutes: float | None = None
    average_time_to_view_minutes: float | None = None
    average_time_to_response_minutes: float | None = None
    average_time_to_action_minutes: float | None = None
    average_total_response_time_minutes: float | None = None
    fastest_response_minutes: int | None = None
    slowest_response_minutes: int | None = None
    alerts_without_response_count: int


class ClinicalOutcomeCreate(BaseModel):
    clinical_deterioration_event_id: int = Field(gt=0)
    outcome_type: Literal[
        "stable_completed_session",
        "session_stopped_early",
        "hospital_admission",
        "emergency_department_transfer",
        "icu_admission",
        "death",
    ]
    outcome_window_hours: Literal[24, 48, 72]
    description: str | None = Field(default=None, max_length=4000)
    recorded_by_user_id: int | None = Field(default=None, gt=0)


class ClinicalOutcomeRead(BaseModel):
    id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    session_date: date | None = None
    clinical_deterioration_event_id: int
    alert_id: int | None = None
    news2_assessment_id: int | None = None
    news2_total_score: int | None = None
    deterioration_type: str | None = None
    outcome_type: str
    outcome_recorded_at: datetime
    outcome_window_hours: int
    description: str | None = None
    recorded_by_user_id: int | None = None
    is_locked: bool
    locked_at: datetime | None = None
    locked_by_user_id: int | None = None
    created_at: datetime


class ClinicalOutcomeResult(BaseModel):
    outcome: ClinicalOutcomeRead
    outcome_created: bool
    message: str


OutcomeValidationDeteriorationType = Literal[
    "severe_hypotension",
    "cardiac_arrhythmia",
    "electrolyte_disorder",
    "vascular_access_complication",
    "neurological_deterioration",
    "emergency_admission",
    "icu_transfer",
    "death",
]
OutcomeValidationTiming = Literal["during_session", "within_6h_after_session", "within_24_72h"]
OutcomeValidationPredictionStatus = Literal["predicted_before", "predicted_concurrent", "not_predicted", "false_negative"]
OutcomeValidationIntervention = Literal[
    "doctor_called",
    "fluids_given",
    "machine_settings_adjusted",
    "dialysis_stopped",
    "emergency_medications_given",
    "ed_transfer",
]
OutcomeValidationFinalResult = Literal["full_improvement", "partial_improvement", "no_improvement", "further_deterioration"]
OutcomeValidationVerificationSource = Literal[
    "medical_record_reviewed",
    "nurse_interviewed",
    "phone_followup_done",
    "independent_doctor_verified",
]


class OutcomeValidationTypeDetails(BaseModel):
    lowest_sbp: int | None = Field(default=None, gt=0, le=300)
    required_treatment: bool | None = None
    arrhythmia_type: Literal["tachycardia", "bradycardia", "irregular_rhythm", "unknown", "other"] | None = None
    arrhythmia_other_notes: str | None = Field(default=None, max_length=1000)
    potassium_value: float | None = Field(default=None, gt=0, le=12)
    vascular_complication_type: str | None = Field(default=None, max_length=120)
    neurological_type: str | None = Field(default=None, max_length=120)
    emergency_admission_datetime: datetime | None = None
    emergency_admission_reason: str | None = Field(default=None, max_length=4000)
    icu_transfer_datetime: datetime | None = None
    death_datetime: datetime | None = None
    death_reason: str | None = Field(default=None, max_length=4000)


class OutcomeValidation72hBase(BaseModel):
    patient_id: int = Field(gt=0)
    dialysis_session_id: int = Field(gt=0)
    deterioration_occurred: bool
    deterioration_types: list[OutcomeValidationDeteriorationType] = Field(default_factory=list)
    type_specific_details: OutcomeValidationTypeDetails = Field(default_factory=OutcomeValidationTypeDetails)
    deterioration_timing_category: OutcomeValidationTiming | None = None
    deterioration_time: time | None = None
    deterioration_datetime: datetime | None = None
    platform_prediction_status: OutcomeValidationPredictionStatus | None = None
    interventions: list[OutcomeValidationIntervention] = Field(default_factory=list)
    doctor_response_time_minutes: int | None = Field(default=None, ge=0, le=1440)
    final_result: OutcomeValidationFinalResult | None = None
    verification_sources: list[OutcomeValidationVerificationSource] = Field(default_factory=list)
    notes: str | None = Field(default=None, max_length=4000)
    completed_by_user_id: int | None = Field(default=None, gt=0)

    @field_validator("notes")
    @classmethod
    def strip_validation_notes(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if not self.verification_sources:
            raise ValueError("verification_sources is required")
        if not self.deterioration_occurred:
            if not self.notes:
                raise ValueError("notes are required when deterioration did not occur")
            self.deterioration_types = []
            self.interventions = []
            return
        if not self.deterioration_types:
            raise ValueError("deterioration_types is required when deterioration occurred")
        if self.deterioration_timing_category is None:
            raise ValueError("deterioration_timing_category is required when deterioration occurred")
        if self.platform_prediction_status is None:
            raise ValueError("platform_prediction_status is required when deterioration occurred")
        if not self.interventions:
            raise ValueError("interventions is required when deterioration occurred")
        if self.final_result is None:
            raise ValueError("final_result is required when deterioration occurred")
        if "doctor_called" in self.interventions and self.doctor_response_time_minutes is None:
            raise ValueError("doctor_response_time_minutes is required when doctor_called is selected")


class OutcomeValidation72hCreate(OutcomeValidation72hBase):
    pass


class OutcomeValidation72hUpdate(OutcomeValidation72hBase):
    pass


class OutcomeValidation72hRead(OutcomeValidation72hBase):
    id: int
    patient_code: str | None = None
    session_date: date | None = None
    eligible_for_completion: bool = False
    eligibility_time: datetime | None = None
    remaining_minutes: int | None = None
    completed_at: datetime
    created_at: datetime
    updated_at: datetime


class OutcomeValidation72hEligibility(BaseModel):
    dialysis_session_id: int
    eligible_for_completion: bool
    eligibility_time: datetime | None = None
    remaining_minutes: int | None = None
    message: str


class OutcomeValidation72hResult(BaseModel):
    validation: OutcomeValidation72hRead
    validation_created: bool
    message: str


class ClinicalOutcomeSummary(BaseModel):
    total_outcomes: int
    stable_completed_session_count: int = 0
    session_stopped_early_count: int = 0
    hospital_admission_count: int = 0
    emergency_department_transfer_count: int = 0
    icu_admission_count: int = 0
    death_count: int = 0


StudyStatus = Literal["draft", "active", "paused", "completed", "archived"]
StudyDesign = Literal["observational", "prospective", "retrospective", "before_after", "cohort", "pilot"]


class ResearchStudyBase(BaseModel):
    study_code: str = Field(min_length=2, max_length=80)
    study_title: str = Field(min_length=2, max_length=255)
    study_description: str | None = Field(default=None, max_length=4000)
    principal_investigator: str | None = Field(default=None, max_length=160)
    study_design: StudyDesign
    study_phase: str | None = Field(default=None, max_length=80)
    study_status: StudyStatus = "draft"
    study_group_a_name: str | None = Field(default=None, max_length=160)
    study_group_b_name: str | None = Field(default=None, max_length=160)
    baseline_period_start: date | None = None
    baseline_period_end: date | None = None
    intervention_period_start: date | None = None
    intervention_period_end: date | None = None
    study_start_date: date | None = None
    study_end_date: date | None = None
    target_sample_size: int | None = Field(default=None, ge=1)
    inclusion_notes: str | None = Field(default=None, max_length=4000)
    exclusion_notes: str | None = Field(default=None, max_length=4000)
    notes: str | None = Field(default=None, max_length=4000)

    @field_validator("study_code")
    @classmethod
    def normalize_study_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("study_title", "principal_investigator", "study_phase", "study_group_a_name", "study_group_b_name")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    @field_validator("baseline_period_end")
    @classmethod
    def validate_baseline_dates(cls, value: date | None, info):
        start = info.data.get("baseline_period_start")
        if value and start and value < start:
            raise ValueError("baseline_period_end must be on or after baseline_period_start")
        return value

    @field_validator("intervention_period_end")
    @classmethod
    def validate_intervention_dates(cls, value: date | None, info):
        start = info.data.get("intervention_period_start")
        if value and start and value < start:
            raise ValueError("intervention_period_end must be on or after intervention_period_start")
        return value

    @field_validator("study_end_date")
    @classmethod
    def validate_study_dates(cls, value: date | None, info):
        start = info.data.get("study_start_date")
        if value and start and value < start:
            raise ValueError("study_end_date must be on or after study_start_date")
        return value


class ResearchStudyCreate(ResearchStudyBase):
    pass


class ResearchStudyUpdate(BaseModel):
    study_code: str | None = Field(default=None, min_length=2, max_length=80)
    study_title: str | None = Field(default=None, min_length=2, max_length=255)
    study_description: str | None = Field(default=None, max_length=4000)
    principal_investigator: str | None = Field(default=None, max_length=160)
    study_design: StudyDesign | None = None
    study_phase: str | None = Field(default=None, max_length=80)
    study_status: StudyStatus | None = None
    study_group_a_name: str | None = Field(default=None, max_length=160)
    study_group_b_name: str | None = Field(default=None, max_length=160)
    baseline_period_start: date | None = None
    baseline_period_end: date | None = None
    intervention_period_start: date | None = None
    intervention_period_end: date | None = None
    study_start_date: date | None = None
    study_end_date: date | None = None
    target_sample_size: int | None = Field(default=None, ge=1)
    inclusion_notes: str | None = Field(default=None, max_length=4000)
    exclusion_notes: str | None = Field(default=None, max_length=4000)
    notes: str | None = Field(default=None, max_length=4000)

    @field_validator("study_code")
    @classmethod
    def normalize_update_study_code(cls, value: str | None) -> str | None:
        return value.strip().upper() if isinstance(value, str) else value


class ResearchStudyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    study_code: str | None = None
    study_title: str | None = None
    study_description: str | None = None
    principal_investigator: str | None = None
    study_design: str | None = None
    study_phase: str | None = None
    study_status: str
    study_group_a_name: str | None = None
    study_group_b_name: str | None = None
    baseline_period_start: date | None = None
    baseline_period_end: date | None = None
    intervention_period_start: date | None = None
    intervention_period_end: date | None = None
    study_start_date: date | None = None
    study_end_date: date | None = None
    target_sample_size: int | None = None
    inclusion_notes: str | None = None
    exclusion_notes: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class StudyReadinessReport(BaseModel):
    study_id: int
    readiness_score: int
    missing_requirements: list[str]
    warnings: list[str]
    recommendations: list[str]
    checks: dict[str, bool]
    check_labels: dict[str, str] = Field(default_factory=dict)
    dashboard: dict[str, object]
    protocol: dict[str, object] = Field(default_factory=dict)
    timeline: dict[str, object] = Field(default_factory=dict)


StaffTrainingRole = Literal["nurse", "doctor", "on_call_doctor", "researcher", "other"]
AcceptanceLevel = Literal["low", "medium", "high"]


class StaffTrainingEvaluationBase(BaseModel):
    staff_user_id: int | None = Field(default=None, gt=0)
    staff_name: str | None = Field(default=None, min_length=2, max_length=160)
    staff_role: StaffTrainingRole
    study_id: int | None = Field(default=None, gt=0)
    training_date: date
    pre_test_score: int = Field(ge=0)
    pre_test_total: int = Field(gt=0)
    post_test_score: int = Field(ge=0)
    post_test_total: int = Field(gt=0)
    competency_items: dict[str, bool] = Field(default_factory=dict)
    competency_notes: str | None = Field(default=None, max_length=4000)
    acceptance_survey: dict[str, int] = Field(default_factory=dict)
    general_notes: str | None = Field(default=None, max_length=4000)
    created_by_user_id: int | None = Field(default=None, gt=0)
    updated_by_user_id: int | None = Field(default=None, gt=0)

    @field_validator("staff_name", "competency_notes", "general_notes")
    @classmethod
    def strip_training_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    def model_post_init(self, __context) -> None:
        if self.staff_user_id is None and not self.staff_name:
            raise ValueError("staff_name is required when staff_user_id is not provided")


class StaffTrainingEvaluationCreate(StaffTrainingEvaluationBase):
    pass


class StaffTrainingEvaluationUpdate(StaffTrainingEvaluationBase):
    pass


class StaffTrainingEvaluationRead(StaffTrainingEvaluationBase):
    id: int
    pre_test_percent: float
    post_test_percent: float
    knowledge_improvement_score: int
    knowledge_improvement_percent: float
    competency_passed: bool
    competency_score: float
    acceptance_total_score: int
    acceptance_mean_score: float
    acceptance_level: AcceptanceLevel
    acceptance_level_label_ar: str
    created_at: datetime
    updated_at: datetime


class StaffTrainingEvaluationResult(BaseModel):
    evaluation: StaffTrainingEvaluationRead
    evaluation_created: bool
    message: str


class StaffTrainingSummary(BaseModel):
    total_evaluated_staff: int
    average_pre_test_percent: float | None = None
    average_post_test_percent: float | None = None
    average_knowledge_improvement_percent: float | None = None
    competency_pass_rate_percent: float | None = None
    average_competency_score: float | None = None
    average_acceptance_score: float | None = None
    acceptance_level_counts: dict[str, int] = Field(default_factory=dict)


AlignmentAuditStatus = Literal["implemented", "partial", "missing", "out_of_scope"]


class AlignmentAuditRow(BaseModel):
    requirement_key: str
    arabic_label: str
    technical_label: str
    source_document_category: str
    status: AlignmentAuditStatus
    related_api_route: str | None = None
    related_frontend_route: str | None = None
    related_export_fields: list[str] = Field(default_factory=list)
    notes: str | None = None


class AlignmentAuditSummary(BaseModel):
    total_requirements: int
    completion_percentage: float
    implemented_count: int
    partial_count: int
    missing_count: int
    out_of_scope_count: int


class AlignmentAuditResponse(BaseModel):
    summary: AlignmentAuditSummary
    rows: list[AlignmentAuditRow]
