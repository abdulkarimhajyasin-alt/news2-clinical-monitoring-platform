# PHASE 08 — MEDICAL AND NURSING RESPONSE WORKFLOW

## Objective

Implement the Medical and Nursing Response Workflow for the NEWS2 Hemodialysis Monitoring Platform.

This phase must allow clinical staff to document the medical/nursing response taken after a clinical deterioration event, while preserving the full traceability chain:

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
Medical / Nursing Response
```

This phase must record response actions, vascular access actions, response start time, response delay minutes, notes, and the responsible user.

This phase must NOT implement the full response time tracking engine yet. It should prepare the data needed for Phase 09.

---

# CURRENT PROJECT STATE

The project currently supports:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready configuration
- Real NEWS2 calculation engine
- Persisted intradialytic measurements
- Persisted NEWS2 assessments
- Governed alert creation engine
- Clinical deterioration event workflow
- Alert lifecycle APIs
- Audit logs
- Real clinical deterioration UI

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
↓
Clinical Deterioration Event Created
```

Phase 08 extends this workflow to:

```text
Clinical Deterioration Event
↓
Medical / Nursing Response
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.

Do not break monitoring workflow.

Do not break NEWS2 engine.

Do not break alert engine.

Do not break deterioration event workflow.

Do not change database tables destructively.

Do not implement outcome tracking yet.

Do not implement SPSS export yet.

Do not implement full authentication or role enforcement yet.

---

# PHASE BOUNDARY

This phase must do:

```text
Deterioration Event exists
↓
Create clinical response
↓
Record patient actions
↓
Record vascular access actions
↓
Record response start time
↓
Calculate response_delay_minutes
↓
Link response to event and alert
↓
Show response in UI
```

This phase must NOT do:

```text
Full response time tracking dashboard
Outcome within 24–72 hours
Research export
Advanced permissions
Automated escalation chains
```

Those belong to later phases.

---

# DATABASE MODEL

Use existing table/model if already present:

```text
clinical_responses
```

Required fields:

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

If fields already exist, do not recreate them destructively.

---

# RESPONSE ACTIONS

## Patient Actions

Support these values:

```text
stop_ultrafiltration
give_fluids
give_oxygen
position_adjustment
medication_given
doctor_called
transfer_prepared
other
```

Arabic labels:

```text
stop_ultrafiltration   => إيقاف سحب السوائل
give_fluids            => إعطاء محاليل
give_oxygen            => إعطاء أوكسجين
position_adjustment    => تعديل وضعية المريض
medication_given       => إعطاء دواء
doctor_called          => استدعاء الطبيب
transfer_prepared      => تجهيز النقل
other                  => أخرى
```

---

## Vascular Access Actions

Support these values:

```text
check_flow
inspect_access_site
blood_culture_from_catheter
catheter_evaluation
other
```

Arabic labels:

```text
check_flow                   => فحص التدفق
inspect_access_site           => فحص موضع الوصلة
blood_culture_from_catheter   => سحب مزرعة دم من القسطرة
catheter_evaluation           => تقييم القسطرة
other                         => أخرى
```

---

# CREATION RULES

A clinical response can be created when:

```text
clinical_deterioration_event exists
```

and it is linked to an alert.

Required behavior:

1. Validate deterioration event exists.
2. Validate linked alert exists.
3. Validate event is not locked.
4. Validate actual response start time.
5. Calculate response_delay_minutes:

```text
actual_response_start_time - digital_alert_time
```

Where:

```text
digital_alert_time = alert.created_at
```

If calculation cannot be done safely:

- Store null.
- Do not fail the response creation unless required timestamps are invalid.

6. Save response.
7. Update alert status to `in_progress` if not already closed/cancelled.
8. Write audit log.
9. Return structured response.

---

# DUPLICATE / MULTIPLE RESPONSE RULE

For MVP:

```text
one clinical deterioration event
↓
one primary clinical response record
```

If a response already exists for the event:

- Do not create duplicate primary response.
- Return the existing response with clear message.
- Allow later phases to add response timeline or multiple notes if needed.

---

# SERVICE LAYER

Create or update:

```text
app/services/response_service.py
```

Recommended functions:

```python
create_clinical_response(db, payload)
get_clinical_responses(db, filters)
get_clinical_response(db, response_id)
```

The service must:

- Validate event relationship.
- Prevent duplicate primary response.
- Calculate response delay.
- Update alert status if appropriate.
- Use transaction-safe behavior.
- Insert audit logs if available.
- Return structured result.

Do not place all logic directly inside the router.

---

# PYDANTIC SCHEMAS

Update:

```text
app/schemas.py
```

Required schemas:

```text
ClinicalResponseCreate
ClinicalResponseRead
ClinicalResponseResult
```

Create request fields:

```text
clinical_deterioration_event_id
actual_response_start_time
patient_actions
vascular_access_actions
responded_by_user_id
notes
```

Notes:

- `patient_actions` should support list of strings.
- `vascular_access_actions` should support list of strings.
- Store arrays safely according to current database style.
- `responded_by_user_id` can temporarily use seeded doctor/nurse user until auth is implemented.

---

# API ENDPOINTS

Create or update router:

```text
app/routers/responses.py
```

Required endpoints:

## Create Response

```text
POST /api/responses
```

Creates response from clinical deterioration event.

---

## List Responses

```text
GET /api/responses
```

Support filters:

```text
clinical_deterioration_event_id
alert_id
patient_id
dialysis_session_id
responded_by_user_id
limit
```

Order:

```text
newest first
```

---

## Get Single Response

```text
GET /api/responses/{id}
```

Returns enriched details:

```text
patient_code
session_date
alert_id
news2_total_score
deterioration_type
digital_alert_time
actual_response_start_time
response_delay_minutes
patient_actions
vascular_access_actions
responded_by_user_id
notes
created_at
```

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement or improve screens:

```text
Medical Response Log
Nursing Response Log
Response Workflow
```

Use real API data.

---

# FRONTEND RESPONSE CREATION

From Clinical Deterioration Events / Event Details screen, add action:

```text
تسجيل الاستجابة الطبية والتمريضية
```

Behavior:

1. User clicks action on deterioration event.
2. Show Arabic form/modal/page.
3. User selects patient actions.
4. User selects vascular access actions.
5. User enters actual response start time.
6. User enters notes.
7. User submits.
8. POST to `/api/responses`.
9. Show success or duplicate-existing message.
10. Refresh response logs and event details.

---

# ARABIC UI LABELS

Screen titles:

```text
سجل الاستجابة الطبية والتمريضية
الاستجابة الطبية
الاستجابة التمريضية
مسار الاستجابة
```

Form labels:

```text
حدث التدهور المرتبط
وقت بدء الاستجابة الفعلي
إجراءات المريض
إجراءات الوصلة الوعائية
المستخدم المستجيب
ملاحظات الاستجابة
```

Buttons:

```text
تسجيل الاستجابة الطبية والتمريضية
حفظ الاستجابة
عرض الاستجابة
```

Messages:

```text
تم تسجيل الاستجابة بنجاح
يوجد سجل استجابة مسجل مسبقاً لهذا الحدث
تعذر تسجيل الاستجابة
```

---

# RESPONSE DETAILS UI

Response details should show:

```text
Patient Code
Dialysis Session
Alert ID
Deterioration Type
NEWS2 Score
Digital Alert Time
Actual Response Start Time
Response Delay Minutes
Patient Actions
Vascular Access Actions
Responded By
Notes
```

Arabic labels only in UI.

Use existing medical card style.

Use response delay badge:

- Green if quick
- Orange if delayed
- Red if very delayed

Use safe thresholds for display only:

```text
<= 5 minutes       green
6–15 minutes       orange
> 15 minutes       red
```

Do not use these thresholds as clinical rules yet.

---

# RESPONSE WORKFLOW UI

Create a timeline showing:

```text
Alert created
Deterioration event created
Response started
Clinical actions documented
```

Arabic examples:

```text
تم إنشاء التنبيه
تم فتح سجل التدهور
بدأت الاستجابة الفعلية
تم توثيق الإجراءات الطبية والتمريضية
```

---

# DASHBOARD / RESEARCH SUMMARY UPDATE

Update research summary if safe to include:

```text
clinical_responses_count
average_response_delay_minutes
fastest_response_delay_minutes
slowest_response_delay_minutes
```

Do this only if straightforward.

Dashboard may display:

```text
متوسط زمن بدء الاستجابة
عدد الاستجابات المسجلة
```

---

# AUDIT LOG

Add audit logs for:

```text
clinical_response_created
clinical_response_reused
```

If audit helper exists, use it.

If not, insert safely into existing audit_logs table.

---

# SEED DATA

Update seed data if needed.

Requirements:

- Seed remains idempotent.
- It may create one fake clinical response linked to the seeded deterioration event.
- Do not duplicate response rows on repeated seed runs.
- Use plausible but fake data.

---

# TESTS

Create:

```text
tests/test_response_workflow.py
```

Required tests:

1. Create response from valid deterioration event.
2. Duplicate response returns/reuses existing record.
3. Invalid event returns 404.
4. Locked event cannot create response.
5. Response derives alert_id from event.
6. Response delay is calculated correctly.
7. Alert status moves to `in_progress` if appropriate.
8. List endpoint returns responses.
9. Detail endpoint returns enriched response.
10. Audit log entry is created if audit infrastructure exists.

Update existing tests if required.

---

# DOCUMENTATION

Create:

```text
docs/response_workflow.md
```

Must document:

- Purpose of medical/nursing response log
- Relationship to deterioration event and alert
- Patient actions
- Vascular access actions
- Response delay calculation
- Duplicate prevention rule
- API endpoints
- UI behavior
- Clinical safety note
- What remains for Phase 09

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/deterioration_workflow.md
```

Mention Phase 08 support.

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

1. Create high NEWS2 measurement.
2. Confirm alert exists.
3. Create deterioration event.
4. Create response.
5. Confirm response appears in Medical/Nursing Response Log.
6. Confirm duplicate response is reused, not duplicated.
7. Confirm response delay is calculated.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Response workflow architecture
4. API endpoints created
5. Frontend updates
6. Duplicate prevention behavior
7. Response delay behavior
8. Audit log behavior
9. Seed data changes
10. Tests added or updated
11. Validation results
12. Medical safety notes
13. Risks / next phase recommendation
14. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase, the recommended next phase is:

```text
Phase 09 — Response Time Tracking Engine
```

That phase will compute and persist full response timing metrics:

```text
time_to_alert_minutes
time_to_view_minutes
time_to_response_minutes
time_to_action_minutes
total_response_time_minutes
```
