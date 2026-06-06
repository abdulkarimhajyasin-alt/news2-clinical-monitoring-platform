# PHASE 10 — CLINICAL OUTCOMES 24–72H WORKFLOW

## Objective

Implement the Clinical Outcomes 24–72 Hours Workflow for the NEWS2 Hemodialysis Monitoring Platform.

This phase must allow the system to document, persist, analyze, and visualize patient outcomes occurring after a clinical deterioration event.

This phase is a major research milestone because it provides the outcome layer needed to evaluate whether early detection and timely response improve clinical outcomes.

The workflow must preserve the complete traceability chain:

```text
Patient
↓
Dialysis Session
↓
Measurement
↓
NEWS2 Assessment
↓
Alert
↓
Clinical Deterioration Event
↓
Clinical Response
↓
Response Time Tracking
↓
Clinical Outcome (24–72h)
```

---

# CURRENT PROJECT STATE

The project currently supports:

- Patient management
- Dialysis sessions
- Intradialytic measurements
- NEWS2 engine
- Alert engine
- Deterioration workflow
- Clinical response workflow
- Response time tracking engine
- Research dashboard
- Audit logs
- API-driven frontend

Current workflow:

```text
Measurement
↓
NEWS2
↓
Alert
↓
Deterioration Event
↓
Clinical Response
↓
Response Time Metrics
```

Phase 10 extends this workflow to:

```text
Clinical Outcome Recording
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.

Do not break any existing workflow.

Do not modify database tables destructively.

Do not implement SPSS export yet.

Do not implement multi-center support.

Do not implement advanced permissions.

Do not implement predictive analytics.

---

# PHASE BOUNDARY

This phase must do:

```text
Clinical Deterioration Event
↓
Outcome Recorded
↓
Outcome Analytics
↓
Research Summary
```

This phase must NOT do:

```text
SPSS Export
Pre/Post Statistical Comparison
Research Dataset Export
AI Prediction
```

Those belong to later phases.

---

# OUTCOME MODEL

Use existing model/table if present:

```text
clinical_outcomes
```

Required fields:

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

If fields already exist, do not recreate destructively.

---

# OUTCOME TYPES

Support:

```text
stable_completed_session
session_stopped_early
hospital_admission
emergency_department_transfer
icu_admission
death
```

Arabic labels:

```text
stable_completed_session      => استقرار واستكمال الجلسة
session_stopped_early         => إيقاف الجلسة مبكراً
hospital_admission            => إدخال إلى المستشفى
emergency_department_transfer => تحويل إلى الطوارئ
icu_admission                 => دخول العناية المركزة
death                         => وفاة
```

---

# OUTCOME WINDOW

Support:

```text
24
48
72
```

Stored as:

```text
outcome_window_hours
```

Purpose:

```text
24h Outcome
48h Outcome
72h Outcome
```

---

# CREATION RULES

Outcome can be recorded when:

```text
clinical_deterioration_event exists
```

Requirements:

1. Validate event exists.
2. Derive patient/session from event.
3. Prevent duplicate primary outcome for the same event/window.
4. Save outcome.
5. Write audit log.
6. Return structured result.

---

# DUPLICATE PREVENTION

For MVP:

```text
one event
+
one outcome window
=
one outcome record
```

Examples:

Allowed:

```text
Event A → 24h Outcome
Event A → 48h Outcome
Event A → 72h Outcome
```

Not allowed:

```text
Event A → 24h Outcome
Event A → another 24h Outcome
```

Return existing record if duplicate attempted.

---

# SERVICE LAYER

Create or update:

```text
app/services/outcome_service.py
```

Recommended functions:

```python
create_outcome(db, payload)
get_outcomes(db, filters)
get_outcome(db, outcome_id)
get_outcome_summary(db)
```

Responsibilities:

- Validate relationships.
- Prevent duplicates.
- Persist outcome.
- Update analytics.
- Write audit logs.
- Return structured results.

---

# PYDANTIC SCHEMAS

Update:

```text
app/schemas.py
```

Required schemas:

```text
ClinicalOutcomeCreate
ClinicalOutcomeRead
ClinicalOutcomeResult
```

Request fields:

```text
clinical_deterioration_event_id
outcome_type
outcome_window_hours
description
recorded_by_user_id
```

Patient/session IDs must be derived from event.

---

# API ENDPOINTS

Create or update:

```text
app/routers/outcomes.py
```

Required:

## Create Outcome

```text
POST /api/outcomes
```

---

## List Outcomes

```text
GET /api/outcomes
```

Filters:

```text
patient_id
dialysis_session_id
clinical_deterioration_event_id
outcome_type
outcome_window_hours
limit
```

Newest first.

---

## Get Outcome

```text
GET /api/outcomes/{id}
```

Return enriched details.

---

## Outcome Summary

```text
GET /api/outcomes/summary
```

Return:

```text
total_outcomes
stable_completed_session_count
session_stopped_early_count
hospital_admission_count
emergency_department_transfer_count
icu_admission_count
death_count
```

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement or improve:

```text
Clinical Outcomes
Outcome Tracking
Outcome Analytics
```

Use real API data.

---

# OUTCOME CREATION UI

From Deterioration Event Details or Response Details:

Add:

```text
تسجيل المآل السريري
```

User workflow:

1. Open event.
2. Select outcome type.
3. Select window:
   - 24 ساعة
   - 48 ساعة
   - 72 ساعة
4. Enter notes.
5. Save outcome.
6. Refresh analytics.

---

# ARABIC UI LABELS

Screen titles:

```text
المآلات السريرية
متابعة المآلات
تحليلات المآلات
```

Form labels:

```text
حدث التدهور المرتبط
نوع المآل
الفترة الزمنية
وصف المآل
المستخدم المسجل
```

Buttons:

```text
تسجيل المآل السريري
حفظ المآل
عرض المآل
```

Messages:

```text
تم تسجيل المآل بنجاح
يوجد مآل مسجل مسبقاً لهذه الفترة
تعذر تسجيل المآل
```

---

# OUTCOME DETAILS UI

Display:

```text
Patient Code
Session Date
Alert ID
NEWS2 Score
Deterioration Type
Outcome Type
Outcome Window
Recorded By
Description
Created At
```

Arabic labels only.

Use existing medical design language.

---

# OUTCOME ANALYTICS

Add KPI cards:

```text
إجمالي المآلات
استقرار واستكمال الجلسة
إدخال إلى المستشفى
تحويل إلى الطوارئ
العناية المركزة
الوفيات
```

Add simple charts.

---

# RESEARCH DASHBOARD UPDATE

Update research summary service.

Add:

```text
total_outcomes
hospital_admission_count
emergency_department_transfer_count
icu_admission_count
death_count
stable_completed_session_count
```

These metrics are essential for the PhD study.

---

# AUDIT LOG

Create logs:

```text
clinical_outcome_created
clinical_outcome_reused
```

Use existing audit infrastructure.

---

# SEED DATA

Update seed data if helpful.

Requirements:

- Seed remains idempotent.
- May create one fake 24h outcome.
- Do not duplicate rows.
- Must be medically plausible.

---

# TESTS

Create:

```text
tests/test_outcome_workflow.py
```

Required tests:

1. Create outcome successfully.
2. Duplicate window prevented.
3. Different windows allowed.
4. Invalid event returns 404.
5. Outcome derives patient/session from event.
6. Outcome summary returns expected counts.
7. Audit logs created.
8. List endpoint returns outcomes.
9. Detail endpoint returns enriched outcome.
10. Outcome analytics updates correctly.

---

# DOCUMENTATION

Create:

```text
docs/outcome_workflow.md
```

Must document:

- Purpose of outcome tracking.
- Outcome windows.
- Outcome types.
- Duplicate prevention.
- API endpoints.
- Analytics.
- Research relevance.

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/response_time_tracking.md
```

Mention Phase 10 support.

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

1. High NEWS2.
2. Alert.
3. Deterioration event.
4. Response.
5. Response tracking.
6. Outcome 24h.
7. Outcome analytics update.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Outcome workflow architecture
4. API endpoints created
5. Frontend updates
6. Duplicate prevention behavior
7. Research dashboard updates
8. Audit log behavior
9. Seed data changes
10. Tests added or updated
11. Validation results
12. Research/medical safety notes
13. Risks / next phase recommendation
14. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase:

```text
Phase 11 — Research Dataset & Export Center
```

This phase will prepare:

```text
Excel Export
CSV Export
SPSS Export
Research Dataset Builder
Study Dataset Validation
```
