# PHASE 09 — RESPONSE TIME TRACKING ENGINE

## Objective

Implement the Response Time Tracking Engine for the NEWS2 Hemodialysis Monitoring Platform.

This phase must compute, persist, expose, and visualize response-time metrics across the clinical deterioration workflow.

This is a core research phase because the PhD study depends on measuring whether digital NEWS2-based monitoring improves early detection and clinical response time.

The engine must preserve the full traceability chain:

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
↓
Response Time Tracking
```

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
- Medical/nursing response workflow
- Alert lifecycle APIs
- Audit logs
- Real frontend integration for monitoring, alerts, deterioration, and responses

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
↓
Medical / Nursing Response Created
```

Phase 09 extends this workflow to:

```text
Response Time Metrics Calculated and Persisted
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.

Do not break monitoring workflow.

Do not break NEWS2 engine.

Do not break alert engine.

Do not break deterioration workflow.

Do not break response workflow.

Do not change database tables destructively.

Do not implement clinical outcomes yet.

Do not implement SPSS export yet.

Do not implement full authentication or role enforcement yet.

---

# PHASE BOUNDARY

This phase must do:

```text
Collect timestamps
↓
Calculate response-time metrics
↓
Persist metrics in response_tracking
↓
Expose APIs
↓
Show metrics in UI
↓
Update research summary
```

This phase must NOT do:

```text
24–72h outcomes
SPSS export
Full research comparison engine
Advanced permissions
Automated external notifications
```

Those belong to later phases.

---

# RESPONSE TRACKING MODEL

Use the existing model/table if already present:

```text
response_tracking
```

Required fields:

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

If fields already exist, do not recreate them destructively.

---

# TIMESTAMP DEFINITIONS

Use these sources:

## vital_signs_recorded_at

From:

```text
intradialytic_measurements.measurement_time
```

or created_at if measurement_time unavailable.

---

## alert_created_at

From:

```text
alerts.created_at
```

---

## alert_viewed_at

From:

```text
alerts.viewed_at
```

May be null.

---

## actual_response_start_time

From:

```text
clinical_responses.actual_response_start_time
```

May be null until response exists.

---

## clinical_action_at

For this phase, use:

```text
clinical_responses.actual_response_start_time
```

unless a stronger action timestamp already exists.

Document this clearly as Phase 09 MVP behavior.

---

## alert_closed_at

From:

```text
alerts.closed_at
```

May be null.

---

# CALCULATED METRICS

Calculate in minutes.

## time_to_alert_minutes

```text
alert_created_at - vital_signs_recorded_at
```

---

## time_to_view_minutes

```text
alert_viewed_at - alert_created_at
```

Null if alert not viewed.

---

## time_to_response_minutes

```text
actual_response_start_time - alert_created_at
```

Null if response does not exist.

---

## time_to_action_minutes

```text
clinical_action_at - alert_created_at
```

Null if unavailable.

---

## total_response_time_minutes

For MVP:

```text
actual_response_start_time - vital_signs_recorded_at
```

If alert is closed and closed_at exists, optionally use:

```text
alert_closed_at - vital_signs_recorded_at
```

But prefer consistent documented behavior:

```text
actual_response_start_time - vital_signs_recorded_at
```

---

# VALIDATION RULES

- Negative durations must not be silently accepted.
- If a timestamp sequence is invalid, set metric to null and include a warning field in service result if appropriate.
- Do not crash the entire workflow because optional timestamps are missing.
- Required timestamps:
  - measurement time
  - alert created time
- Optional timestamps:
  - alert viewed time
  - response start time
  - action time
  - alert closed time

---

# SERVICE LAYER

Create or update:

```text
app/services/response_tracking_service.py
```

Recommended functions:

```python
calculate_response_tracking_for_alert(db, alert_id)
upsert_response_tracking_for_alert(db, alert_id)
get_response_tracking_records(db, filters)
get_response_tracking_summary(db, filters)
```

Responsibilities:

- Load alert.
- Load NEWS2 assessment.
- Load measurement.
- Load deterioration event if exists.
- Load clinical response if exists.
- Calculate metrics.
- Upsert response_tracking record.
- Return structured result.
- Avoid duplicate tracking rows for same alert.
- Write audit log if appropriate.

---

# WHEN TO CREATE / UPDATE TRACKING

Call the tracking service after these events if safe:

1. Alert created/reused/upgraded.
2. Alert viewed.
3. Alert acknowledged.
4. Alert started.
5. Alert closed.
6. Deterioration event created.
7. Clinical response created.

Minimum required for this phase:

- When clinical response is created, tracking must be created/updated.
- When alert lifecycle changes, tracking should be updated.

Do this without creating circular imports.

---

# API ENDPOINTS

Create or update router:

```text
app/routers/response_tracking.py
```

Required endpoints:

## List Tracking Records

```text
GET /api/response-tracking
```

Filters:

```text
patient_id
dialysis_session_id
alert_id
clinical_deterioration_event_id
limit
```

Order:

```text
newest first
```

---

## Get Single Tracking Record

```text
GET /api/response-tracking/{id}
```

Return enriched fields:

```text
patient_code
session_date
alert_id
news2_total_score
risk_level
deterioration_type
time_to_alert_minutes
time_to_view_minutes
time_to_response_minutes
time_to_action_minutes
total_response_time_minutes
created_at
updated_at
```

---

## Recalculate Tracking For Alert

```text
POST /api/response-tracking/recalculate/{alert_id}
```

Use for manual repair/testing.

---

## Summary Endpoint

```text
GET /api/response-tracking/summary
```

Return:

```text
records_count
average_time_to_alert_minutes
average_time_to_view_minutes
average_time_to_response_minutes
average_time_to_action_minutes
average_total_response_time_minutes
fastest_response_minutes
slowest_response_minutes
alerts_without_response_count
```

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement or improve these screens:

```text
Response Time Dashboard
Response Analytics
Response Workflow
```

Use real API data.

---

# RESPONSE TIME DASHBOARD UI

Display KPI cards:

```text
متوسط زمن إنشاء التنبيه
متوسط زمن مشاهدة التنبيه
متوسط زمن بدء الاستجابة
أسرع استجابة
أبطأ استجابة
تنبيهات بدون استجابة
```

Use minutes.

Use Arabic labels.

Use clinical card style.

---

# RESPONSE TRACKING TABLE

Display records with:

```text
Patient Code
Session Date
NEWS2 Score
Risk Level
Deterioration Type
Time to Alert
Time to View
Time to Response
Total Response Time
```

Arabic UI labels only.

---

# RESPONSE ANALYTICS UI

Add simple charts using existing chart style:

- Average response metrics
- Risk-level response timing if available
- Alerts with/without response

Do not introduce large external chart libraries unless already used.

---

# RESPONSE WORKFLOW TIMELINE

Update existing response workflow timeline to include:

```text
Vital signs recorded
Alert created
Alert viewed
Deterioration event created
Response started
Alert closed
```

Show missing steps as pending.

Arabic examples:

```text
تم تسجيل العلامات الحيوية
تم إنشاء التنبيه
تمت مشاهدة التنبيه
تم فتح سجل التدهور
بدأت الاستجابة
تم إغلاق التنبيه
```

---

# DASHBOARD / RESEARCH SUMMARY UPDATE

Update research summary service if safe:

Add:

```text
average_time_to_alert_minutes
average_time_to_response_minutes
fastest_response_minutes
slowest_response_minutes
alerts_without_response_count
```

Dashboard should reflect these metrics if already displaying response KPIs.

---

# AUDIT LOG

Add audit logs for:

```text
response_tracking_created
response_tracking_updated
response_tracking_recalculated
```

If audit helper exists, use it.

If not, insert safely into existing audit_logs table.

---

# SEED DATA

Update seed data if helpful.

Requirements:

- Seed remains idempotent.
- It may create or update one fake response_tracking record based on existing seeded alert/response.
- Do not duplicate tracking rows on repeated seed runs.
- Seeded metrics should be plausible.

---

# TESTS

Create:

```text
tests/test_response_tracking_engine.py
```

Required tests:

1. Tracking is created/updated after clinical response creation.
2. Tracking calculates time_to_alert correctly.
3. Tracking calculates time_to_response correctly.
4. Optional null timestamps do not crash calculation.
5. Negative durations are not silently accepted.
6. Duplicate tracking rows are prevented.
7. Recalculate endpoint works.
8. Summary endpoint returns expected keys.
9. Alert lifecycle update refreshes tracking where applicable.
10. Frontend-facing list endpoint returns enriched fields.

Update existing tests if needed.

---

# DOCUMENTATION

Create:

```text
docs/response_time_tracking.md
```

Must document:

- Purpose of response time tracking
- Research importance
- Timestamp sources
- Metric formulas
- Null/invalid timestamp handling
- API endpoints
- UI behavior
- Clinical/research safety note
- What remains for later phases

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/response_workflow.md
```

Mention Phase 09 support.

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
3. View/acknowledge/start alert.
4. Create deterioration event.
5. Create clinical response.
6. Confirm response_tracking record exists.
7. Confirm metrics display in Response Time Dashboard.
8. Confirm summary endpoint returns averages.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Response tracking engine architecture
4. Metrics implemented
5. API endpoints created
6. Frontend updates
7. Dashboard/research summary updates
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

After this phase, the recommended next phase is:

```text
Phase 10 — Clinical Outcomes 24–72h Workflow
```

That phase will record patient outcomes after deterioration events:

```text
Stable completed session
Session stopped early
Hospital admission
Emergency department transfer
ICU admission
Death
```
