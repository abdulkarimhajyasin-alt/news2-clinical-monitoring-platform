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
    is_anonymized: bool


class DialysisSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    session_date: date
    weekday: str | None = None
    session_status: str
    target_ultrafiltration: float | None = None
    session_duration_minutes: int | None = None


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    dialysis_session_id: int
    risk_level: str
    severity_level: str
    status: str
    priority: str | None = None
    trigger_reason: str | None = None
    created_at: datetime


class ResearchSummary(BaseModel):
    patients: int
    dialysis_sessions: int
    measurements: int
    news2_assessments: int
    active_alerts: int
    deterioration_events: int
    outcomes: int
