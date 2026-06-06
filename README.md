# NEWS2 Hemodialysis Monitoring Platform

Arabic-first clinical research MVP for monitoring hemodialysis patients using NEWS2, documenting alerts, deterioration events, medical/nursing responses, response times, and 24-72 hour outcomes.

## Stack

- FastAPI
- SQLAlchemy 2.x
- SQLite for local development
- PostgreSQL-ready `NEWS2_DATABASE_URL` configuration
- Pydantic schemas
- Static RTL frontend served by FastAPI

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Seed Database

```bash
python -m app.seed
```

This creates local SQLite tables and inserts fake anonymized clinical research data.

On application startup the platform also runs safe database initialization:

- missing tables are created with SQLAlchemy `create_all`
- existing tables are not dropped or reset
- demo seed data is inserted only when users/patients are empty
- `NEWS2_AUTO_SEED=false` disables automatic seeding but not table creation

## Run Locally

```bash
uvicorn app.main:app --reload
```

Open:

- UI: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- API docs: `http://127.0.0.1:8000/docs`

## API-Backed Frontend

Phase 03 connects the static Arabic RTL frontend to read-only FastAPI endpoints while preserving hash routing and the existing UI identity.

Phase 04 adds the NEWS2 calculation engine and `POST /api/news2/calculate`. The endpoint returns component scores, total score, risk level, alert flag, and single-parameter trigger status without saving a database record. Seeded NEWS2 assessments are generated through the same engine.

Phase 05 adds the intradialytic monitoring write workflow through `POST /api/monitoring/measurements`. It persists a measurement, calculates NEWS2, persists the linked assessment, and returns the clinical workflow result.

Phase 06 adds governed alert creation. Persisted NEWS2 assessments now create or reuse an active alert when NEWS2 is 5 or higher, or when a single NEWS2 component scores 3.

Phase 07 adds the clinical deterioration event workflow. Active alerts can now be converted into structured deterioration events with duplicate prevention and full patient/session/NEWS2/alert traceability.

Phase 08 adds the medical and nursing response workflow. Deterioration events can now receive one primary response record with patient actions, vascular access actions, response start time, response delay, responder, and notes.

Phase 09 adds the response time tracking engine. It upserts one `response_tracking` row per alert after deterioration/response workflow activity, calculates time to alert/view/response/action/total response time, exposes summary APIs, and powers the Response Time Dashboard and Response Analytics screens.

Phase 10 adds clinical outcome tracking for the 24, 48, and 72 hour windows after deterioration events. Outcomes are created through `POST /api/outcomes`, derive patient/session IDs from the deterioration event, prevent duplicate records for the same event/window, update outcome analytics, and extend the research summary with admission, transfer, ICU, death, and stable completion counts.

Phase 11 adds the Research Dataset & Export Center. It builds privacy-protected research rows from measurement-linked NEWS2 assessments, validates dataset quality, exports CSV and XLSX files, and provides SPSS-ready codebook and variable label downloads.

Phase 12 adds the Research Analytics Dashboard. It provides descriptive KPIs, NEWS2/risk/outcome distributions, response-time analysis, deterioration analysis, group comparison, and research readiness indicators without inferential statistics or predictive modeling.

Phase 13 adds the Study Management & Research Protocol Center. It manages `research_studies`, protocol configuration, study timeline visibility, readiness scoring, and audit logs for study creation, updates, and readiness review.

Phase 14 adds the RBAC foundation. It centralizes role permissions, exposes `/api/rbac/me` and `/api/rbac/permissions`, protects sensitive exports, analytics, study management, clinical writes, and alert lifecycle actions, and adds a temporary `X-Dev-Role` development context until Phase 15 authentication.

Screens now using real database-backed data:

- Dashboard: `/api/research/summary`, `/api/alerts`, `/api/patients`, `/api/dialysis-sessions`
- Patient List: `/api/patients`
- Dialysis Session List: `/api/dialysis-sessions`
- Active Alerts: `/api/alerts`
- Research Dashboard: `/api/research/summary`
- NEWS2 Calculator: `/api/news2/calculate`
- Vital Signs Entry: `/api/monitoring/measurements`
- Monitoring History: `/api/monitoring/measurements`, `/api/news2/assessments`
- Alerts: `/api/alerts`, `/api/alerts/{id}`, `/api/alerts/{id}/view`, `/api/alerts/{id}/acknowledge`, `/api/alerts/{id}/start`, `/api/alerts/{id}/close`
- Clinical Deterioration: `/api/deterioration/events`, `/api/deterioration/events/{id}`
- Responses: `/api/responses`, `/api/responses/{id}`
- Response Tracking: `/api/response-tracking`, `/api/response-tracking/{id}`, `/api/response-tracking/recalculate/{alert_id}`, `/api/response-tracking/summary`
- Clinical Outcomes: `/api/outcomes`, `/api/outcomes/{id}`, `/api/outcomes/summary`
- Research Dataset & Exports: `/api/research/dataset`, `/api/research/dataset/quality`, `/api/research/export/csv`, `/api/research/export/xlsx`, `/api/research/export/spss-codebook`, `/api/research/export/spss-variable-labels`
- Research Analytics: `/api/research/analytics/summary`, `/api/research/analytics/news2-distribution`, `/api/research/analytics/outcomes`, `/api/research/analytics/response-times`, `/api/research/analytics/deterioration`, `/api/research/analytics/group-comparison`
- Study Management: `/api/studies`, `/api/studies/{study_id}`, `/api/studies/{study_id}/readiness`
- RBAC: `/api/rbac/me`, `/api/rbac/permissions`

The frontend includes scoped Arabic loading, error, and empty states. It also shows a subtle backend connection indicator based on `/health`.

NEWS2 is implemented as clinical decision support only. It supports early detection of deterioration but does not replace clinical judgment, and it requires clinical review before real-world deployment.

## Validation

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```
