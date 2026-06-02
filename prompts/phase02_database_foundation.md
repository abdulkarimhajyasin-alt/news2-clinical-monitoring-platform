# PHASE 02 — DATABASE FOUNDATION + PROJECT ARCHITECTURE

## Objective

Implement the database foundation and project architecture for the NEWS2 Hemodialysis Monitoring Platform.

This phase must transform the current static UI prototype into a structured project ready for real backend/database integration.

The system is an Arabic-first clinical research platform for monitoring hemodialysis patients using NEWS2, tracking clinical deterioration, documenting medical/nursing response, measuring response time, and recording outcomes within 24–72 hours.

---

# CURRENT PROJECT STATE

The project currently contains a static frontend implementation:

- `index.html`
- `styles.css`
- `app.js`

Phase 01 created a connected static Arabic RTL UI shell with 40 screens and mock data.

Do not destroy this work.

---

# CRITICAL RULES

## Preserve Existing UI

Do not remove the existing UI system.

Do not break hash routing.

Do not change the medical visual identity unless needed for integration readiness.

Do not replace the frontend with a different framework in this phase.

---

## No Premature Backend Features

This phase is about:

- Project structure
- Database schema design
- Local database foundation
- Data models
- Migration readiness
- Seed data readiness
- Documentation

Do not implement full authentication workflows yet.

Do not implement real NEWS2 calculations yet.

Do not implement full API endpoints yet unless minimal structural stubs are needed.

---

# RECOMMENDED STACK

Use a practical production-ready Python web foundation:

- FastAPI
- SQLAlchemy
- SQLite for local development
- PostgreSQL-ready configuration
- Alembic-ready structure
- Pydantic schemas
- Clean service/repository separation

If dependencies are not already present, create a clear `requirements.txt`.

---

# REQUIRED PROJECT STRUCTURE

Create or organize the project into this structure:

```text
news2-hemodialysis-monitoring/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── patients.py
│   │   ├── dialysis_sessions.py
│   │   ├── monitoring.py
│   │   ├── news2.py
│   │   ├── alerts.py
│   │   ├── deterioration.py
│   │   ├── responses.py
│   │   ├── outcomes.py
│   │   ├── research.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── patient_service.py
│   │   ├── dialysis_service.py
│   │   ├── monitoring_service.py
│   │   ├── news2_service.py
│   │   ├── alert_service.py
│   │   ├── response_service.py
│   │   ├── outcome_service.py
│   │   └── research_service.py
│   │
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── app.js
│
├── docs/
│   ├── system_architecture.md
│   ├── database_design.md
│   ├── research_workflow.md
│   ├── ui_identity.md
│   └── project_scope.md
│
├── prompts/
│   ├── phase01_complete_ui_system.md
│   └── phase02_database_foundation.md
│
├── tests/
│   ├── test_database_models.py
│   └── test_app_health.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

If some files already exist, preserve them and modify safely.

---

# STATIC FRONTEND RELOCATION

Move the current static frontend files into:

```text
app/static/
```

Files:

```text
index.html
styles.css
app.js
```

Then configure FastAPI to serve the static frontend.

The root route `/` should serve:

```text
app/static/index.html
```

Static assets should remain accessible.

Do not break browser preview.

---

# DATABASE MODELS

Implement SQLAlchemy models for the following entities.

Use English table and field names.

Arabic text must remain in frontend/i18n later, not database identifiers.

---

## users

Fields:

```text
id
full_name
email
password_hash
role
department
phone
status
preferred_language
last_login_at
created_at
updated_at
```

Roles should support at minimum:

```text
admin
doctor
on_call_doctor
nurse
researcher
```

---

## patients

Fields:

```text
id
patient_code
full_name
age
gender
target_dry_weight
dialysis_start_date
dialysis_vintage_months
weekly_sessions_count
comorbidities
charlson_comorbidity_index
baseline_functional_status
study_phase
study_group
is_anonymized
is_locked
locked_at
locked_by_user_id
created_at
updated_at
```

Study phase values:

```text
pre_implementation
post_implementation
```

Study group values:

```text
control
intervention
```

---

## patient_vascular_access

Fields:

```text
id
patient_id
access_type
access_location
inserted_at
notes
is_locked
locked_at
locked_by_user_id
created_at
updated_at
```

Access type values:

```text
av_fistula
av_graft
central_venous_catheter
```

---

## dialysis_sessions

Fields:

```text
id
patient_id
session_date
weekday
actual_start_time
actual_end_time
target_ultrafiltration
blood_flow_rate
dialysate_flow_rate
dialysate_temperature
ultrafiltration_rate
ultrafiltration_volume
session_duration_minutes
session_status
session_notes
created_by_user_id
is_locked
locked_at
locked_by_user_id
created_at
updated_at
```

---

## intradialytic_measurements

Fields:

```text
id
patient_id
dialysis_session_id
measurement_time
measurement_interval_minutes
respiratory_rate
spo2
oxygen_therapy
systolic_bp
diastolic_bp
pulse_rate
temperature
consciousness_level
confusion_status
recorded_by_user_id
created_at
```

---

## news2_assessments

Fields:

```text
id
patient_id
dialysis_session_id
intradialytic_measurement_id
respiratory_score
spo2_score
oxygen_score
systolic_bp_score
pulse_score
temperature_score
consciousness_score
total_score
risk_level
alert_required
trigger_reason
created_by_user_id
created_at
```

Risk level values:

```text
low
medium
high
critical
```

---

## alerts

Fields:

```text
id
patient_id
dialysis_session_id
news2_assessment_id
risk_level
severity_level
status
priority
trigger_reason
assigned_to_user_id
created_at
viewed_at
acknowledged_at
action_taken_at
closed_at
closed_by_user_id
```

Alert status values:

```text
new
viewed
acknowledged
in_progress
closed
cancelled
```

Severity values:

```text
low
medium
high
critical
```

---

## clinical_deterioration_events

Fields:

```text
id
patient_id
dialysis_session_id
news2_assessment_id
alert_id
deterioration_time
time_from_session_start_minutes
deterioration_type
triggering_news2_score
description
is_locked
locked_at
locked_by_user_id
created_at
updated_at
```

Deterioration types:

```text
acute_hypotension
suspected_sepsis_or_fever
arrhythmia
seizures
reduced_consciousness
other
```

---

## clinical_responses

Fields:

```text
id
clinical_deterioration_event_id
alert_id
digital_alert_time
actual_response_start_time
response_delay_minutes
patient_actions
vascular_access_actions
responded_by_user_id
notes
is_locked
locked_at
locked_by_user_id
created_at
updated_at
```

Use JSON/text-safe storage for action arrays.

---

## response_tracking

Fields:

```text
id
alert_id
dialysis_session_id
news2_assessment_id
clinical_deterioration_event_id
vital_signs_recorded_at
alert_created_at
alert_viewed_at
actual_response_start_time
clinical_action_at
alert_closed_at
time_to_alert_minutes
time_to_view_minutes
time_to_response_minutes
time_to_action_minutes
total_response_time_minutes
created_at
updated_at
```

---

## clinical_outcomes

Fields:

```text
id
patient_id
dialysis_session_id
clinical_deterioration_event_id
outcome_type
outcome_recorded_at
outcome_window_hours
description
recorded_by_user_id
is_locked
locked_at
locked_by_user_id
created_at
```

Outcome type values:

```text
stable_completed_session
session_stopped_early
hospital_admission
emergency_department_transfer
icu_admission
death
```

---

## clinical_notes

Fields:

```text
id
patient_id
dialysis_session_id
news2_assessment_id
alert_id
user_id
note_type
content
created_at
updated_at
```

---

## research_studies

Fields:

```text
id
title
description
principal_investigator
study_design
start_date
end_date
status
created_at
updated_at
```

---

## audit_logs

Fields:

```text
id
user_id
action
entity_type
entity_id
old_value
new_value
ip_address
user_agent
created_at
```

---

## system_settings

Fields:

```text
id
setting_key
setting_value
created_at
updated_at
```

---

# RELATIONSHIPS

Implement meaningful SQLAlchemy relationships:

- Patient → vascular access
- Patient → dialysis sessions
- Dialysis session → measurements
- Measurement → NEWS2 assessment
- NEWS2 assessment → alert
- Alert → clinical deterioration event
- Clinical deterioration event → clinical response
- Clinical deterioration event → clinical outcome
- User → created sessions
- User → recorded measurements
- User → audit logs

Use foreign keys where appropriate.

---

# DATABASE INITIALIZATION

Create a safe local database initialization flow.

Required:

```bash
python -m app.seed
```

This should:

- Create tables
- Insert sample users
- Insert sample patients
- Insert sample dialysis sessions
- Insert sample intradialytic measurements
- Insert sample NEWS2 assessments
- Insert sample alerts
- Insert sample deterioration events
- Insert sample responses
- Insert sample outcomes
- Insert system settings

Seed data should be medically plausible but clearly fake.

Do not include real patient names.

Use anonymized Arabic sample names or coded patients.

---

# HEALTH CHECK

Create a FastAPI health route:

```text
GET /health
```

Response example:

```json
{
  "status": "ok",
  "service": "news2-hemodialysis-monitoring",
  "database": "connected"
}
```

---

# MINIMAL READ-ONLY API STUBS

Create minimal read-only API endpoints only for structural validation.

Do not overbuild.

Required endpoints:

```text
GET /api/patients
GET /api/dialysis-sessions
GET /api/alerts
GET /api/research/summary
```

Each endpoint should query real database seed data.

---

# DOCUMENTATION FILES

Create the following docs.

---

## docs/project_scope.md

Must explain:

- This is a PhD Research MVP
- It is clinical decision support, not a replacement for medical judgment
- Arabic-first UI
- English codebase/database
- Future healthcare SaaS path
- Excluded for MVP:
  - APK
  - WhatsApp
  - SMS
  - Device integration
  - AI/ML
  - Hospital system integration
  - Multi-center SaaS

---

## docs/system_architecture.md

Must summarize:

- Patient baseline
- Dialysis session
- Intradialytic monitoring
- NEWS2 assessment
- Alerts
- Clinical deterioration
- Clinical response
- Response time tracking
- Outcomes 24–72h
- Research analytics
- Export layer
- Audit log

---

## docs/database_design.md

Must document:

- Tables
- Key fields
- Relationships
- Locking fields
- Research data governance
- Export privacy rules

---

## docs/research_workflow.md

Must document:

```text
Patient Baseline
↓
Dialysis Session
↓
Repeated Monitoring
↓
NEWS2 Calculation
↓
Alert if NEWS2 >= 5 or sudden deterioration
↓
Deterioration Log
↓
Medical/Nursing Response
↓
Response Time Tracking
↓
Outcome within 24–72h
↓
Research Dataset
```

---

## docs/ui_identity.md

Must document:

- Arabic RTL
- Medical blue palette
- White clinical cards
- Soft shadows
- Sidebar navigation
- KPI cards
- NEWS2 colors
- Alert severity colors
- Medical animations
- Accessibility direction

---

# FRONTEND INTEGRATION PREPARATION

Do not fully connect frontend to API yet.

But prepare the project so Phase 03 can do that cleanly.

Add comments or clear service boundaries in `app.js` if needed.

Do not rewrite the UI.

---

# TESTS

Add basic tests.

Required:

```text
tests/test_app_health.py
tests/test_database_models.py
```

Tests should verify:

- FastAPI app can start
- `/health` works
- database models can create tables
- seed flow does not crash
- required models exist

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
```

If pytest is unavailable, add it to requirements.

Also keep frontend validation:

```bash
node --check app/static/app.js
```

---

# README UPDATE

Update README with:

- Project name
- Purpose
- Stack
- How to install
- How to seed database
- How to run locally
- How to open UI
- Validation commands

Example run command:

```bash
uvicorn app.main:app --reload
```

---

# FINAL RESPONSE REQUIRED FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Architecture impact
4. Database models created
5. API endpoints created
6. Seed data summary
7. Docs created
8. Validation results
9. Risks / next phase recommendation
10. Git commands

Do not skip validation.
