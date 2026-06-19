# Phase 20 — Nurse Training, Competency, and Acceptance Module

## Objective
Implement the research-aligned nursing training and acceptance module required by the doctoral protocol. This phase must focus only on what is directly required by the final study documents: pre-test, post-test, practical competency readiness, and staff acceptance/satisfaction with the HD2-mNEWS digital monitoring system.

The platform is a NEWS2 / HD2-mNEWS hemodialysis clinical monitoring and research platform. Preserve the current architecture, Arabic RTL UI, existing RBAC, authentication, patient lifecycle protection, HD2-mNEWS engine, 72-hour outcome validation workflow, prediction evaluation, and research export behavior.

## Current Baseline
The project already includes:
- FastAPI + SQLAlchemy + PostgreSQL/SQLite-compatible startup guards
- Arabic RTL SPA frontend in `app/static/app.js` and `app/static/styles.css`
- Authentication, cookie sessions, RBAC, and admin user management
- Patient baseline/context form aligned with the digital monitoring form
- Dialysis session context
- Standard NEWS2 and HD2-mNEWS scoring
- HD2 risk color and nursing protocol guidance
- Alerts, clinical responses, outcomes
- 72-hour post-dialysis clinical outcome validation
- Prediction accuracy research evaluation
- Research dataset/export center
- Research analytics
- Tests currently passing: 285+

## Scope
Add a dedicated research training and acceptance module for staff.

This module must support:
1. Nurse/staff training records
2. Pre-test knowledge assessment
3. Post-test knowledge assessment
4. Practical competency checklist
5. Acceptance/satisfaction survey
6. Research export fields
7. Arabic UI screens under the study/research scope
8. RBAC protection
9. Regression tests

Do not add unrelated hospital, HR, scheduling, payroll, shift-management, or LMS features.

## Terminology
Use Arabic UI labels. Keep code, database columns, APIs, and internal identifiers in English.

Preferred Arabic labels:
- تدريب التمريض
- الاختبار القبلي
- الاختبار البعدي
- تقييم الكفاءة العملية
- قبول النظام ورضا المستخدمين
- جاهزية التمريض
- نتيجة التدريب
- قبل التدريب
- بعد التدريب

## Backend Requirements

### 1. Data Model
Add models/tables as needed, using additive nullable-safe schema changes and startup/runtime guards.

Suggested model: `StaffTrainingEvaluation`

Fields should include, at minimum:
- `id`
- `staff_user_id` nullable FK to users if available
- `staff_name` fallback text
- `staff_role` text/enum: nurse, doctor, on_call_doctor, researcher, other
- `study_id` nullable FK if compatible with current study module
- `training_date`
- `pre_test_score`
- `pre_test_total`
- `post_test_score`
- `post_test_total`
- `knowledge_improvement_score` derived or persisted
- `knowledge_improvement_percent` derived or persisted
- `competency_items_json`
- `competency_passed`
- `competency_score`
- `competency_notes`
- `acceptance_survey_json`
- `acceptance_total_score`
- `acceptance_mean_score`
- `acceptance_level` such as low/medium/high
- `general_notes`
- `created_by_user_id`
- `updated_by_user_id`
- `created_at`
- `updated_at`

Keep schema compatible with SQLite and PostgreSQL.

### 2. Service Layer
Create a deterministic service, for example:
- `app/services/training_evaluation_service.py`

Service responsibilities:
- Validate test scores are non-negative and do not exceed totals.
- Calculate improvement:
  - raw difference = post score - pre score
  - percent improvement = difference / pre score when pre score > 0, otherwise safe fallback.
- Evaluate competency checklist:
  - support configurable/default checklist items.
  - passed if required items are completed and score threshold is met.
- Calculate acceptance score:
  - Likert-style values, preferably 1–5.
  - mean score.
  - level: low / medium / high.
- Return Arabic labels for frontend display.

### 3. API Router
Add protected endpoints, for example:
- `POST /api/training/evaluations`
- `GET /api/training/evaluations`
- `GET /api/training/evaluations/{id}`
- `PUT /api/training/evaluations/{id}`
- `GET /api/training/summary`

Use existing auth/RBAC patterns.

Permissions:
- View: reuse `studies:view` or `research:view` if no dedicated permission system update is desired.
- Create/update: reuse `studies:create` / `studies:update` or `research:create` if available.

Do not weaken authorization.

### 4. Summary Endpoint
`GET /api/training/summary` should return:
- total evaluated staff
- average pre-test score percent
- average post-test score percent
- average improvement percent
- competency pass rate
- average acceptance score
- acceptance distribution by low/medium/high

Exclude deleted/deactivated users only if the existing project has clear conventions. Do not break historical research records.

## Frontend Requirements

### 1. Navigation
Add one focused sidebar item only if it fits the cleaned scope:
- `تدريب التمريض`

Place it near:
- بروتوكول الدراسة
- التحليل البحثي

Do not reintroduce deleted/out-of-scope menu items.

### 2. UI Page
Add an Arabic RTL page for training evaluation.

The page should include:
- Summary cards
- Form to add/update staff training evaluation
- Table/list of existing evaluations
- Clear sections:
  1. بيانات الكادر
  2. الاختبار القبلي
  3. الاختبار البعدي
  4. تقييم الكفاءة العملية
  5. رضا وقبول النظام
  6. ملاحظات

### 3. Competency Checklist
Default practical competency items should align with the study:
- فهم متغيرات HD2-mNEWS
- إدخال العلامات الحيوية بشكل صحيح
- إدخال متغيرات الغسيل الإضافية
- قراءة لون الخطورة
- اتباع البروتوكول التمريضي حسب اللون
- توثيق الاستجابة السريرية
- توثيق النتيجة السريرية بعد 72 ساعة

### 4. Acceptance Survey Items
Default Likert items should include:
- سهولة استخدام النظام
- وضوح التنبيهات
- فائدة لون الخطورة
- فائدة البروتوكول التمريضي
- تقليل أخطاء الحساب اليدوي
- دعم سرعة الاستجابة
- ملاءمة النظام للعمل اليومي في وحدة الغسيل
- الرضا العام عن النظام

Use 1–5 scoring.

## Research Export Requirements
Extend research dataset/export center with training/acceptance fields where appropriate.

Add either:
- a separate training export endpoint, or
- include aggregated staff training metrics in existing research export if architecture supports it safely.

Preferred safe approach:
- Add dedicated endpoint(s):
  - `GET /api/training/export/csv`
  - optional XLSX if current export patterns make this simple.

Export fields:
- staff role
- training date
- pre-test score percent
- post-test score percent
- improvement score
- improvement percent
- competency passed
- competency score
- acceptance mean score
- acceptance level

## Audit Logging
Create audit log events for:
- training evaluation created
- training evaluation updated

Use the existing audit logging pattern if available.

## Tests
Add/extend tests for:
- service calculations
- score validation
- competency pass/fail
- acceptance score levels
- API RBAC protection
- create/list/update behavior
- summary endpoint
- export endpoint/fields
- navigation does not reintroduce out-of-scope routes

Keep all existing tests passing.

## Validation Commands
Run:
```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

## Git Commands to Provide After Implementation
After successful validation, provide:
```bash
git add .
git commit -m "Add nursing training and acceptance evaluation"
git push origin main
```

## Constraints
- Preserve Arabic-first RTL UI.
- Preserve existing visual identity.
- Preserve authentication and RBAC.
- Preserve existing patient/session/HD2/outcome/prediction workflows.
- Do not remove existing APIs.
- Do not add destructive database operations.
- Do not introduce unrelated clinical/hospital management features.
- Keep implementation production-grade, additive, tested, and research-aligned.
