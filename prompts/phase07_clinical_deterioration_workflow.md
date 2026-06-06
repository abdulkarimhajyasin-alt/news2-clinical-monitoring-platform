# PHASE 07 — CLINICAL DETERIORATION EVENT WORKFLOW

## Objective

Implement the Clinical Deterioration Event Workflow for the NEWS2 Hemodialysis Monitoring Platform.

This phase must transform clinically significant alerts into structured clinical deterioration events while preserving the full traceability chain:

```text
Patient
↓
Dialysis Session
↓
Intradialytic Measurement
↓
NEWS2 Assessment
↓
Alert
↓
Clinical Deterioration Event
```

The system must allow clinical staff to create, view, and manage deterioration events linked to alerts, without yet implementing medical/nursing response documentation or outcome tracking.

---

# CURRENT PROJECT STATE

The project currently supports:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready config
- Real NEWS2 calculation engine
- Persisted intradialytic measurements
- Persisted NEWS2 assessments
- Governed alert creation engine
- Duplicate alert prevention
- Alert lifecycle APIs
- Real active alerts UI
- Audit logs for alert lifecycle

Current workflow:

```text
Vital Signs Entry
↓
Measurement Saved
↓
NEWS2 Calculated
↓
NEWS2 Assessment Saved
↓
Alert Created / Reused / Upgraded
```

Phase 07 extends this workflow to:

```text
Alert
↓
Clinical Deterioration Event
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.

Do not break the monitoring write workflow.

Do not break NEWS2 calculation.

Do not break alert creation.

Do not change database tables destructively.

Do not implement medical/nursing response workflow yet.

Do not implement response time tracking yet.

Do not implement outcomes yet.

Do not implement full authentication or role enforcement yet.

---

# PHASE BOUNDARY

This phase must do:

```text
Alert exists
↓
Create or view clinical deterioration event
↓
Link event to patient/session/NEWS2/alert
↓
Prevent duplicate deterioration event per active alert chain
↓
Expose API and frontend UI
```

This phase must NOT do:

```text
Medical response log
Nursing response log
Response time calculation
Clinical outcome tracking
SPSS export
Full auth/permissions
```

Those belong to later phases.

---

# DETERIORATION EVENT MODEL

Use the existing model/table if already created:

```text
clinical_deterioration_events
```

Required fields:

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

If the fields already exist, do not recreate them destructively.

---

# DETERIORATION TYPES

Support these values:

```text
acute_hypotension
suspected_sepsis_or_fever
arrhythmia
seizures
reduced_consciousness
other
```

Arabic labels:

```text
acute_hypotension              => هبوط ضغط حاد
suspected_sepsis_or_fever      => اشتباه إنتان / حرارة
arrhythmia                     => اضطراب نظم القلب
seizures                       => تشنجات
reduced_consciousness          => انخفاض الوعي
other                          => أخرى
```

---

# CREATION RULES

A clinical deterioration event can be created when:

```text
alert exists
```

and the alert is linked to:

```text
patient_id
dialysis_session_id
news2_assessment_id
```

Required behavior:

1. Validate alert exists.
2. Validate alert is not closed or cancelled.
3. Validate linked patient exists.
4. Validate linked dialysis session exists.
5. Validate linked NEWS2 assessment exists.
6. Prevent duplicate deterioration events for the same active alert.
7. Create event.
8. Optionally set alert status to `in_progress` if it is still `new`, `viewed`, or `acknowledged`.
9. Write audit log entry.

---

# DUPLICATE PREVENTION

For a given active alert:

```text
one alert
↓
one active clinical deterioration event
```

If an event already exists for the same alert:

- Do not create another duplicate.
- Return the existing event with a clear message.
- Keep traceability stable.

---

# TIME FROM SESSION START

Calculate:

```text
time_from_session_start_minutes
```

If:

```text
dialysis_session.actual_start_time
```

and:

```text
deterioration_time
```

are available.

If it cannot be calculated safely:

- Store null.
- Do not fail the event creation.
- Document the limitation.

---

# SERVICE LAYER

Create or update:

```text
app/services/deterioration_service.py
```

Recommended functions:

```python
create_deterioration_event_from_alert(db, payload)
get_deterioration_events(db, filters)
get_deterioration_event(db, event_id)
```

The service must:

- Validate alert relationship.
- Prevent duplicates.
- Calculate time from session start.
- Update alert status if appropriate.
- Create audit log if infrastructure exists.
- Use transaction-safe logic.
- Return structured results.

Do not put all business logic directly inside the router.

---

# Pydantic SCHEMAS

Update:

```text
app/schemas.py
```

Required schemas:

```text
ClinicalDeteriorationEventCreate
ClinicalDeteriorationEventRead
ClinicalDeteriorationEventResult
```

Create request fields:

```text
alert_id
deterioration_time
deterioration_type
description
created_by_user_id
```

Notes:

- `created_by_user_id` can temporarily use seeded doctor/nurse user until auth is implemented.
- `triggering_news2_score` should be derived from linked NEWS2 assessment, not manually trusted from frontend.
- patient/session/assessment IDs should be derived from alert, not manually trusted from frontend.

---

# API ENDPOINTS

Create or update router:

```text
app/routers/deterioration.py
```

Required endpoints:

## Create Event From Alert

```text
POST /api/deterioration/events
```

Creates event from alert.

---

## List Events

```text
GET /api/deterioration/events
```

Support filters:

```text
patient_id
dialysis_session_id
alert_id
deterioration_type
limit
```

Order:

```text
newest first
```

---

## Get Single Event

```text
GET /api/deterioration/events/{id}
```

Returns full event details including:

```text
patient_code
session_date
news2_total_score
alert_status
deterioration_type
description
time_from_session_start_minutes
created_at
```

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement or improve the following screens:

```text
Clinical Deterioration Events
Event Details
Event Timeline
```

Use real API data.

---

# FRONTEND EVENT CREATION

From Active Alerts screen or Alert Details screen, add action:

```text
فتح سجل تدهور سريري
```

Behavior:

1. User clicks action on alert.
2. Show Arabic form/modal/page.
3. User selects deterioration type.
4. User enters description.
5. User confirms creation.
6. POST to `/api/deterioration/events`.
7. Show success or duplicate-existing message.
8. Refresh deterioration events list and alert status.

Do not create response log yet.

---

# ARABIC UI LABELS

Use professional Arabic labels.

Screen titles:

```text
سجل التدهور السريري
تفاصيل حدث التدهور
الخط الزمني للتدهور السريري
```

Form labels:

```text
التنبيه المرتبط
وقت التدهور
نوع التدهور
وصف الحالة
```

Buttons:

```text
فتح سجل تدهور سريري
حفظ حدث التدهور
عرض التفاصيل
```

Messages:

```text
تم إنشاء حدث التدهور السريري بنجاح
يوجد حدث تدهور مسجل مسبقاً لهذا التنبيه
تعذر إنشاء حدث التدهور
```

---

# EVENT DETAILS UI

Event detail page/card should show:

```text
Patient Code
Dialysis Session
Alert ID
NEWS2 Score
Risk Level
Deterioration Type
Deterioration Time
Time From Session Start
Description
Alert Status
```

Arabic labels only in UI.

Use medical card style.

Use risk colors.

---

# EVENT TIMELINE UI

Create a clean timeline showing:

```text
Vital signs recorded
NEWS2 calculated
Alert created
Alert acknowledged / started if available
Deterioration event created
```

If some timestamps are missing, show them as pending/not recorded.

Arabic text examples:

```text
تم تسجيل العلامات الحيوية
تم حساب NEWS2
تم إنشاء التنبيه
تم فتح سجل التدهور
```

---

# DASHBOARD / RESEARCH SUMMARY UPDATE

Update research summary if appropriate to include:

```text
deterioration_events_count
acute_hypotension_count
suspected_sepsis_or_fever_count
arrhythmia_count
seizures_count
reduced_consciousness_count
```

Do this only if safe and simple.

Dashboard should display deterioration event count if already showing clinical KPIs.

---

# AUDIT LOG

Add audit logs for:

```text
clinical_deterioration_event_created
clinical_deterioration_event_reused
```

If audit helper exists, use it.

If not, implement minimal safe insertion using existing audit_logs table.

Do not overbuild.

---

# SEED DATA

Update seed data only if helpful.

Requirements:

- Seed remains idempotent.
- It may create one fake deterioration event linked to the seeded alert.
- Do not duplicate event rows on repeated seed runs.
- Use medically plausible but fake data.

---

# TESTS

Create:

```text
tests/test_deterioration_workflow.py
```

Required tests:

1. Create deterioration event from valid active alert.
2. Duplicate creation returns/reuses existing event, not duplicate row.
3. Closed alert cannot create new deterioration event.
4. Invalid alert returns 404.
5. Event derives patient/session/assessment from alert.
6. Event derives triggering NEWS2 score from assessment.
7. Alert status moves to `in_progress` if appropriate.
8. List endpoint returns created events.
9. Detail endpoint returns enriched event info.
10. Audit log entry is created if audit infrastructure exists.

Update existing tests if required.

---

# DOCUMENTATION

Create:

```text
docs/deterioration_workflow.md
```

Must document:

- Purpose of clinical deterioration events
- Relationship to alerts and NEWS2
- Duplicate prevention rule
- Deterioration types
- API endpoints
- UI behavior
- Clinical safety note
- What remains for later phases

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/alert_engine.md
```

Mention Phase 07 support.

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Manual validation:

```bash
uvicorn app.main:app --reload
```

Then test:

1. Submit high NEWS2 measurement to create alert.
2. Open Active Alerts.
3. Click/create deterioration event.
4. Confirm event appears in Clinical Deterioration Events.
5. Confirm duplicate click does not create duplicate event.
6. Confirm Event Timeline shows the correct traceability chain.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Deterioration workflow architecture
4. API endpoints created
5. Frontend updates
6. Duplicate prevention behavior
7. Audit log behavior
8. Seed data changes
9. Tests added or updated
10. Validation results
11. Medical safety notes
12. Risks / next phase recommendation
13. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase, the recommended next phase is:

```text
Phase 08 — Medical and Nursing Response Workflow
```

That phase will document clinical actions taken after deterioration:

```text
Stop ultrafiltration
Give fluids
Give oxygen
Position adjustment
Medication given
Doctor called
Transfer prepared
Vascular access actions
```
