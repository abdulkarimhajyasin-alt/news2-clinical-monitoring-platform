# PHASE 03 — FRONTEND API INTEGRATION FOUNDATION

## Objective

Implement the frontend API integration foundation for the NEWS2 Hemodialysis Monitoring Platform.

This phase must connect the existing Arabic-first static UI to the real FastAPI read-only endpoints created in Phase 02, while preserving the current visual identity, RTL layout, hash routing, and medical dashboard experience.

The goal is to start replacing mock-only behavior with real database-backed data safely.

---

# CURRENT PROJECT STATE

The project currently has:

- FastAPI backend
- SQLAlchemy models
- SQLite local database
- Seed data
- Read-only API endpoints
- Static frontend served from `app/static/`

Existing key files:

```text
app/main.py
app/database.py
app/models.py
app/schemas.py
app/seed.py

app/routers/health.py
app/routers/patients.py
app/routers/dialysis_sessions.py
app/routers/alerts.py
app/routers/research.py

app/static/index.html
app/static/styles.css
app/static/app.js
```

Phase 01 created the UI.
Phase 02 created the backend/database foundation.

This phase must connect both layers.

---

# CRITICAL RULES

## Preserve UI

Do not redesign the app.

Do not replace the UI framework.

Do not break hash routing.

Do not remove existing screens.

Do not remove the medical animations.

Do not change the Arabic-first RTL identity.

---

## Do Not Overbuild

This phase is NOT for:

- Authentication
- Login security
- Write APIs
- CRUD workflows
- NEWS2 calculation engine
- Alert creation engine
- Export engine
- Role permissions enforcement

Those will come later.

This phase is only for safe frontend-to-backend read integration.

---

# PRIMARY GOAL

Replace mock data with real API data where endpoints already exist.

Integrate these routes:

```text
GET /health
GET /api/patients
GET /api/dialysis-sessions
GET /api/alerts
GET /api/research/summary
```

---

# FRONTEND API CLIENT

Create a clean API client inside:

```text
app/static/app.js
```

or a new file if appropriate:

```text
app/static/api.js
```

If creating `api.js`, update `index.html` safely.

The API client must include:

```text
api.getHealth()
api.getPatients()
api.getDialysisSessions()
api.getAlerts()
api.getResearchSummary()
```

Requirements:

- Use `fetch`
- Use async/await
- Handle HTTP errors
- Handle network errors
- Return normalized data
- Avoid duplicated fetch logic
- Keep base URL relative, e.g. `/api/patients`

---

# DATA STATE MANAGEMENT

Add a small frontend state layer.

Required state:

```text
appState = {
  health: null,
  patients: [],
  dialysisSessions: [],
  alerts: [],
  researchSummary: null,
  loading: {},
  errors: {}
}
```

The UI should remain functional if an API fails.

Fallback behavior:

- Show error state in affected screen
- Do not crash the whole app
- Keep navigation working
- Show empty states when no data exists

---

# SCREENS TO CONNECT TO REAL API DATA

## Dashboard

Use:

```text
GET /api/research/summary
GET /api/alerts
GET /api/patients
GET /api/dialysis-sessions
```

Dashboard should display real seeded counts where available:

- Patient count
- Session count
- Alert count
- Research summary metrics
- Active alert count
- High risk / critical alert indicators if available

If a value is not yet available from API, keep a safe placeholder but label it clearly as demo/placeholder only in code comments, not visually unless needed.

---

## Patient List

Use:

```text
GET /api/patients
```

Replace static patient list with API-backed rows.

Required columns:

```text
patient_code
age
gender
study_phase
study_group
dialysis_vintage_months
weekly_sessions_count
```

Arabic labels must remain in UI.

---

## Dialysis Session List

Use:

```text
GET /api/dialysis-sessions
```

Display API-backed sessions.

Required columns if available:

```text
patient_code or patient_id
session_date
weekday
actual_start_time
actual_end_time
target_ultrafiltration
session_status
```

---

## Alerts

Use:

```text
GET /api/alerts
```

Display API-backed alert list.

Required columns if available:

```text
patient_code or patient_id
risk_level
severity_level
status
priority
trigger_reason
created_at
```

Add Arabic risk/severity/status labels.

---

## Research Dashboard

Use:

```text
GET /api/research/summary
```

Display real summary data.

This screen should feel more real than Phase 01.

Add dedicated cards for:

- Total patients
- Total sessions
- Total measurements
- Total alerts
- Total deterioration events
- Total outcomes
- Average NEWS2 if available
- Outcome distribution if available

If backend does not provide all values yet, handle missing keys safely.

---

# LOADING STATES

Add real loading states for API-backed screens.

Required loading components:

- Medical skeleton card
- Table skeleton rows
- Subtle ECG/heartbeat loader
- Loading text in Arabic

Arabic examples:

```text
جاري تحميل البيانات السريرية...
جاري تحميل قائمة المرضى...
جاري تحميل التنبيهات...
```

Do not use annoying full-screen loaders except first app load if needed.

---

# ERROR STATES

Add professional Arabic error states.

Examples:

```text
تعذر تحميل البيانات
حدث خطأ أثناء الاتصال بالخادم
حاول تحديث الصفحة أو تشغيل الخادم المحلي
```

Each API-backed screen should show a scoped error message without breaking the entire app.

---

# EMPTY STATES

Add empty states for:

- No patients
- No sessions
- No alerts
- No research data

Arabic examples:

```text
لا توجد بيانات مرضى حتى الآن
لا توجد جلسات غسيل مسجلة
لا توجد تنبيهات نشطة
```

---

# HEALTH CHECK INDICATOR

Add a subtle backend status indicator in the UI.

Location:

- Top bar or sidebar footer

Display:

```text
متصل بالخادم
غير متصل بالخادم
```

Use colors:

- Green for connected
- Red/orange for disconnected

Do not make it intrusive.

Use:

```text
GET /health
```

---

# DATA NORMALIZATION

Add mapping helpers for Arabic labels.

Examples:

```text
riskLevelLabel("low") => "منخفض"
riskLevelLabel("medium") => "متوسط"
riskLevelLabel("high") => "مرتفع"
riskLevelLabel("critical") => "حرج"
```

Also implement labels for:

```text
study_phase
study_group
gender
alert_status
severity_level
session_status
outcome_type
```

Keep these helpers centralized.

---

# BACKEND ADJUSTMENTS ALLOWED

Only minimal backend changes are allowed if needed to make frontend integration cleaner.

Allowed:

- Improve response schemas
- Add patient_code to session/alert response if easy and safe
- Add count fields to research summary
- Add CORS only if actually needed
- Add stable response ordering

Not allowed:

- Full CRUD
- Auth
- Complex business logic
- NEWS2 calculation engine
- Major schema changes

---

# API RESPONSE QUALITY

Make API responses frontend-friendly.

For patients, include:

```text
id
patient_code
age
gender
study_phase
study_group
dialysis_vintage_months
weekly_sessions_count
```

For sessions, include patient code if available:

```text
id
patient_id
patient_code
session_date
weekday
actual_start_time
actual_end_time
target_ultrafiltration
session_status
```

For alerts, include patient code if available:

```text
id
patient_id
patient_code
risk_level
severity_level
status
priority
trigger_reason
created_at
```

For research summary, include counts:

```text
patients_count
sessions_count
measurements_count
alerts_count
deterioration_events_count
responses_count
outcomes_count
```

---

# ACCESSIBILITY IMPROVEMENTS

While touching UI code, improve accessibility safely:

- Add aria-label to sidebar toggle
- Add meaningful labels to status indicators
- Add chart descriptions where applicable
- Keep keyboard navigation working
- Improve focus visibility if missing

Do not overwork accessibility in this phase, but fix obvious issues.

---

# VALIDATION REQUIREMENTS

Run:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Also manually verify:

```text
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Check:

- Dashboard loads
- Patient list shows seeded patients
- Session list shows seeded sessions
- Alerts list shows seeded alert
- Research dashboard shows seeded summary
- Backend status indicator works
- App does not crash if API fails

---

# TESTS

Update or add tests if backend responses change.

Required tests should still pass:

```text
tests/test_app_health.py
tests/test_database_models.py
```

Add a simple API test file if appropriate:

```text
tests/test_api_read_endpoints.py
```

Test:

- `/api/patients`
- `/api/dialysis-sessions`
- `/api/alerts`
- `/api/research/summary`

---

# README UPDATE

Update README with:

- API-backed frontend note
- How to seed database
- How to run FastAPI
- How to open the UI
- Which screens now use real API data
- Validation commands

---

# FINAL RESPONSE REQUIRED FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Frontend API integration summary
4. API endpoints used
5. Screens now using real data
6. Loading/error/empty states added
7. Backend changes, if any
8. Tests added or updated
9. Validation results
10. Risks and next phase recommendation
11. Git commands

Do not skip validation.
