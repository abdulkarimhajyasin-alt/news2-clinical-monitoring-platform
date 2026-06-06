# PHASE 05 — MONITORING WRITE WORKFLOW

## Objective

Implement the real intradialytic monitoring write workflow for the NEWS2 Hemodialysis Monitoring Platform.

This phase must allow the system to accept new vital-sign measurements during a dialysis session, persist the intradialytic measurement, calculate NEWS2 using the Phase 04 engine, persist the generated NEWS2 assessment, and return the complete result to the frontend.

This phase is the bridge between readonly clinical data and real clinical workflow.

---

# CURRENT PROJECT STATE

The project currently has:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready configuration
- Seed data
- Read-only API integration
- Real NEWS2 calculation engine
- `POST /api/news2/calculate`
- Dashboard / Patients / Sessions / Alerts / Research Summary using real API data
- A small frontend NEWS2 calculator demo panel

Important files:

```text
app/main.py
app/database.py
app/models.py
app/schemas.py
app/seed.py

app/services/news2_service.py
app/services/monitoring_service.py
app/services/dialysis_service.py

app/routers/monitoring.py
app/routers/news2.py
app/routers/dialysis_sessions.py

app/static/index.html
app/static/styles.css
app/static/app.js

tests/
docs/
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.
Do not break the existing hash routing.
Do not remove the NEWS2 calculator endpoint.
Do not remove existing read-only endpoints.
Do not change database tables destructively.
Do not implement full authentication yet.
Do not implement role enforcement yet.
Do not implement automatic alert creation yet.
Do not implement clinical deterioration workflow yet.

---

# PHASE BOUNDARY

This phase must do:

```text
Create measurement
↓
Calculate NEWS2
↓
Save NEWS2 assessment
↓
Return result
↓
Refresh relevant frontend views
```

This phase must NOT do:

```text
Automatic alert creation
Clinical deterioration event creation
Response tracking
Outcome tracking
Authentication
Role permissions
```

Those belong to later phases.

---

# BACKEND WORKFLOW

Implement a write endpoint for recording a new intradialytic measurement.

Required endpoint:

```text
POST /api/monitoring/measurements
```

The endpoint must:

1. Validate input.
2. Confirm the referenced patient exists.
3. Confirm the referenced dialysis session exists.
4. Confirm the session belongs to the patient.
5. Save a new `intradialytic_measurements` record.
6. Calculate NEWS2 using the Phase 04 engine.
7. Save a new `news2_assessments` record linked to the measurement.
8. Return the created measurement and assessment together.
9. Do not create alerts automatically yet.

---

# REQUEST SCHEMA

Create or update Pydantic schema:

```text
MonitoringMeasurementCreate
```

Required fields:

```text
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
spo2_scale
recorded_by_user_id
```

Notes:

- `spo2_scale` defaults to `scale_1`.
- `diastolic_bp` is stored but not used in NEWS2 calculation.
- `recorded_by_user_id` can temporarily use a seeded nurse user until Auth is implemented.

Validation:

- patient_id must be positive.
- dialysis_session_id must be positive.
- respiratory_rate must be positive.
- spo2 must be 0–100.
- systolic_bp and diastolic_bp must be positive.
- pulse_rate must be positive.
- temperature must be clinically plausible.
- measurement_interval_minutes must be positive.
- consciousness_level must be one of:
  - alert
  - voice
  - pain
  - unresponsive
  - new_confusion

---

# RESPONSE SCHEMA

Create or update Pydantic schema:

```text
MonitoringMeasurementResult
```

Response should include:

```text
measurement
news2_assessment
message
```

Measurement response fields:

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

NEWS2 assessment response fields:

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

Add `single_parameter_trigger` to the response if supported by the engine even if not stored in the database yet.

---

# SERVICE LAYER

Implement the core workflow in:

```text
app/services/monitoring_service.py
```

Recommended function:

```python
create_measurement_with_news2(db, payload)
```

Responsibilities:

- Validate patient/session relationship.
- Create measurement.
- Call NEWS2 engine.
- Create NEWS2 assessment.
- Commit transaction safely.
- Roll back on failure.
- Return structured result.

Do not put all business logic directly in the router.

---

# ROUTER LAYER

Update:

```text
app/routers/monitoring.py
```

Add:

```text
POST /api/monitoring/measurements
```

Use dependency-injected DB session.

Return Pydantic response.

Use clear HTTP errors:

```text
404 if patient not found
404 if session not found
400 if session does not belong to patient
422 for invalid clinical input
500 only for unexpected failures
```

---

# READ ENDPOINTS FOR FRONTEND REFRESH

Add minimal read endpoints if missing:

```text
GET /api/monitoring/measurements
GET /api/news2/assessments
```

They should support optional query filters:

```text
patient_id
dialysis_session_id
limit
```

Purpose:

- Refresh monitoring table.
- Refresh NEWS2 history.
- Refresh trend data later.

Keep these endpoints simple and read-only.

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Connect the Intradialytic Monitoring / Vital Signs Entry screen to the new endpoint.

Required behavior:

1. Show a professional Arabic vital-sign entry form.
2. Allow selecting patient and dialysis session from real API data.
3. Submit vital signs to:

```text
POST /api/monitoring/measurements
```

4. Show loading state while submitting.
5. Show success state with:
   - NEWS2 total score
   - Arabic risk level
   - component scores
   - alert required indicator
6. Show scoped Arabic error messages if submission fails.
7. Keep the form usable after submission.
8. Refresh monitoring/NEWS2 data after successful submission if read endpoints exist.

Do not redesign the whole app.

---

# REQUIRED FORM FIELDS — ARABIC UI

Use Arabic labels:

```text
المريض
جلسة الغسيل
وقت القياس
الفاصل الزمني بالدقائق
معدل التنفس
تشبع الأوكسجين SpO2
هل يتلقى أوكسجين؟
ضغط الدم الانقباضي
ضغط الدم الانبساطي
معدل النبض
درجة الحرارة
مستوى الوعي
وجود ارتباك حديث
```

Submit button:

```text
حفظ القياس وحساب NEWS2
```

Success message:

```text
تم حفظ القياس وحساب NEWS2 بنجاح
```

Error message examples:

```text
تعذر حفظ القياس
تأكد من صحة البيانات المدخلة
الجلسة المحددة لا تتبع هذا المريض
```

---

# CLINICAL RESULT UI

After successful submission, display a result panel:

```text
نتيجة NEWS2
الدرجة الكلية
مستوى الخطورة
يتطلب تنبيهاً سريرياً
سبب التفعيل
```

Component scores:

```text
التنفس
تشبع الأوكسجين
الأوكسجين الإضافي
ضغط الدم الانقباضي
النبض
درجة الحرارة
الوعي
```

Use existing medical card style.

Use existing risk colors.

Use subtle pulse animation only if risk is high or alert_required is true.

---

# API CLIENT

Extend the frontend API client with:

```text
api.createMonitoringMeasurement(payload)
api.getMonitoringMeasurements(filters)
api.getNews2Assessments(filters)
```

Keep fetch logic centralized.

Handle non-2xx responses cleanly.

---

# DATABASE / MODEL NOTES

Do not add new tables unless absolutely necessary.

Use existing:

```text
intradialytic_measurements
news2_assessments
```

If a required field is missing from model/schema, add it safely without destructive migration logic.

Because this project is still local SQLite without Alembic migrations, if schema changes are unavoidable, document them clearly.

---

# SEED DATA

Update seed data only if needed.

Requirements:

- Seed must remain idempotent.
- Seed should still create at least one patient, one session, one measurement, one NEWS2 assessment.
- Seed NEWS2 assessment should continue to use the engine.
- Do not duplicate rows across repeated seed runs.

---

# TESTING REQUIREMENTS

Add tests:

```text
tests/test_monitoring_write_workflow.py
```

Required tests:

1. Valid measurement creates measurement and NEWS2 assessment.
2. Invalid patient returns 404.
3. Invalid session returns 404.
4. Session/patient mismatch returns 400.
5. Invalid vital signs returns 422.
6. Created NEWS2 score matches engine output.
7. No alert is automatically created in this phase.

Update existing tests if response schemas change.

---

# API TEST EXAMPLE

Test request:

```json
{
  "patient_id": 1,
  "dialysis_session_id": 1,
  "measurement_time": "2026-06-05T10:30:00",
  "measurement_interval_minutes": 30,
  "respiratory_rate": 22,
  "spo2": 94,
  "oxygen_therapy": false,
  "systolic_bp": 105,
  "diastolic_bp": 65,
  "pulse_rate": 112,
  "temperature": 38.2,
  "consciousness_level": "alert",
  "confusion_status": false,
  "spo2_scale": "scale_1",
  "recorded_by_user_id": 4
}
```

Expected:

- HTTP 200 or 201
- measurement created
- NEWS2 assessment created
- total_score calculated
- risk_level returned
- alert_required returned
- no alert row created automatically

---

# DOCUMENTATION

Create or update:

```text
docs/monitoring_workflow.md
```

Must document:

- Purpose of intradialytic monitoring
- Measurement submission workflow
- NEWS2 calculation integration
- Database records created
- Why alerts are not auto-created until Phase 06
- Clinical safety note

Update:

```text
docs/system_architecture.md
docs/research_workflow.md
docs/news2_engine.md
README.md
```

Mention that Phase 05 now supports persisted measurements and persisted NEWS2 assessments.

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Manual smoke test:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Verify:

- Vital Signs Entry form loads.
- Patients are loaded from API.
- Sessions are loaded from API.
- Submitting valid vitals creates a measurement.
- NEWS2 result appears on screen.
- Refreshing the page does not break the app.
- No automatic alert is created yet.

Also test API directly:

```text
POST http://127.0.0.1:8000/api/monitoring/measurements
```

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Backend workflow implemented
4. API endpoints created or updated
5. Frontend screens updated
6. NEWS2 persistence behavior
7. Tests added or updated
8. Validation results
9. Medical safety notes
10. Risks / next phase recommendation
11. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase, the recommended next phase is:

```text
Phase 06 — Alert Creation Engine
```

That phase will use persisted NEWS2 assessments to create alerts automatically when:

```text
NEWS2 >= 5
```

or when a single parameter scores 3 / sudden deterioration is manually triggered.
