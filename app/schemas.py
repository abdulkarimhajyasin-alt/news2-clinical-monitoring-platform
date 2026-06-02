from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str
    department: str | None = None
    status: str
    preferred_language: str


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_code: str
    full_name: str
    age: int
    gender: str
    study_phase: str
    study_group: str
    dialysis_vintage_months: int | None = None
    weekly_sessions_count: int | None = None
    is_anonymized: bool


class DialysisSessionRead(BaseModel):
    id: int
    patient_id: int
    patient_code: str | None = None
    session_date: date
    weekday: str | None = None
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    session_status: str
    target_ultrafiltration: float | None = None
    session_duration_minutes: int | None = None


class AlertRead(BaseModel):
    id: int
    patient_id: int
    patient_code: str | None = None
    dialysis_session_id: int
    risk_level: str
    severity_level: str
    status: str
    priority: str | None = None
    trigger_reason: str | None = None
    created_at: datetime


class ResearchSummary(BaseModel):
    patients_count: int
    sessions_count: int
    measurements_count: int
    news2_assessments_count: int
    alerts_count: int
    active_alerts_count: int
    deterioration_events_count: int
    responses_count: int
    outcomes_count: int
    average_news2: float | None = None
