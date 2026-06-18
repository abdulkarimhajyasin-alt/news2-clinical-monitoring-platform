# Phase 18B — Baseline Patient Form Alignment With Doctor Final Digital Monitoring Form

## Objective
Implement the missing baseline/context patient and dialysis-session fields required by the doctor’s final digital monitoring form, while preserving the existing NEWS2/HD2-mNEWS workflow, RBAC, Arabic RTL design, and production stability.

This phase must align the platform with the first form in the research protocol:

**Context & Baseline Patient Form — الملف الأساسي للمريض وسياق العلاج**

The system must collect and persist the patient baseline and dialysis treatment context needed for HD2-mNEWS scoring, research exports, and later clinical outcome validation.

---

## Current Project State
The project already includes:

- FastAPI backend
- SQLAlchemy models
- PostgreSQL / Neon production deployment
- Arabic RTL SPA frontend
- Authentication and RBAC
- Patient lifecycle workflow
- Dialysis sessions
- Monitoring measurements
- Standard NEWS2 scoring
- HD2-mNEWS scoring engine from Phase 18A
- Alerts, responses, outcomes, research dataset, analytics, study protocol
- 252 passing tests after Phase 18A

Do not remove or break existing functionality.

---

## Source of Truth
The implementation must follow the doctor’s final digital monitoring form.

Required baseline/context fields include:

### Patient Demographic / Baseline Fields
- Encrypted/medical code
- Age
- Sex
- Educational level
- Target dry weight
- Dialysis start date
- Number of dialysis sessions per week
- Comorbidities such as:
  - Heart failure
  - Diabetes mellitus
  - Hypertension
  - Other comorbidities

### Vascular Access Fields
- Vascular access type:
  - AV Fistula
  - AV Graft
  - CVC
- Vascular access location:
  - Arm sections
  - Thigh
  - Jugular
  - Other
- Current access creation/placement date

### Dialysis Session Context Fields
- Session date
- Day of week
- Actual session start time
- Target fluid removal for the session

---

## Implementation Requirements

### 1. Database / Models
Update the existing models safely and add nullable columns only where needed.

Prefer extending existing patient and dialysis session models rather than creating unnecessary parallel entities.

Suggested mapping:

#### Patient model additions
- `medical_code` or reuse existing patient code if already present
- `education_level`
- `dry_weight_kg`
- `dialysis_start_date`
- `weekly_dialysis_sessions`
- `comorbid_heart_failure`
- `comorbid_diabetes`
- `comorbid_hypertension`
- `comorbidities_notes`
- `vascular_access_type`
- `vascular_access_location`
- `vascular_access_placement_date`

#### Dialysis session model additions
- `session_day_of_week`
- `actual_start_time`
- `target_fluid_removal_ml`

If equivalent columns already exist, reuse them and avoid duplication.

All new columns must be nullable and must not break existing records.

Add safe startup/runtime schema guards consistent with the project’s current database compatibility approach.

---

### 2. Schemas
Update Pydantic schemas for:

- Patient create
- Patient update
- Patient read/detail
- Dialysis session create
- Dialysis session update/read if applicable

Ensure validation is practical but not over-restrictive.

Rules:

- `dry_weight_kg` must be positive if provided.
- `weekly_dialysis_sessions` should be between 1 and 7 if provided.
- `target_fluid_removal_ml` must be non-negative if provided.
- Dates and times should use existing project conventions.

---

### 3. Backend Services / Routes
Update patient and dialysis-session services/routes so the new fields are:

- Accepted on create/update.
- Returned in detail endpoints.
- Preserved during patient lifecycle changes.
- Available for monitoring and research dataset generation.

Do not bypass authentication or RBAC.

Do not weaken existing patient lifecycle protections.

---

### 4. Frontend UI
Update the Arabic RTL interface professionally.

The design must remain consistent with the current medical dashboard style.

Add or update forms so users can manage the baseline/context fields.

Required UI areas:

#### Patient form / Patient profile
Add grouped section:

**الملف الأساسي للمريض**

Fields:
- الرقم الطبي المشفر
- العمر
- الجنس
- المستوى التعليمي
- الوزن الجاف المستهدف
- تاريخ بدء الغسيل الكلوي
- عدد الجلسات الأسبوعية
- الأمراض المصاحبة
- نوع الوصلة الوعائية
- موضع الوصلة
- تاريخ تركيب الوصلة الحالية

#### Dialysis session form
Add grouped section:

**سياق جلسة الغسيل**

Fields:
- تاريخ الجلسة
- اليوم من الأسبوع
- توقيت بدء الجلسة الفعلي
- معدل / كمية سحب السوائل المستهدفة للجلسة

If the session day can be derived from session date, derive it automatically but still expose it clearly in the UI.

Use Arabic labels only in the visible UI, except unavoidable clinical abbreviations.

---

### 5. Integration With HD2-mNEWS
The monitoring form already includes dry weight, fluid removal, duration, etc. from Phase 18A.

In this phase:

- Where possible, prefill dry weight from patient baseline.
- Where possible, prefill target fluid removal from the linked session.
- Do not force prefill if data is missing.
- Do not break manual override.
- Do not change HD2-mNEWS scoring thresholds unless required by existing tests.

---

### 6. Research Dataset Export
Update research dataset/export fields to include the baseline/context variables required by the doctor’s form:

- Patient code
- Age
- Sex
- Education level
- Dry weight
- Dialysis start date
- Weekly dialysis sessions
- Comorbidities
- Vascular access type
- Vascular access location
- Vascular access placement date
- Session date
- Session day of week
- Actual session start time
- Target fluid removal

Preserve existing privacy protections.

Deleted patients must remain excluded from research dataset/export logic.

---

### 7. Tests
Add/update regression tests.

Minimum required tests:

1. Patient create/update/read includes baseline fields.
2. Dialysis session create/read includes session context fields.
3. Research dataset includes the new baseline/context variables.
4. Existing monitoring write workflow remains compatible.
5. HD2-mNEWS workflow remains compatible.
6. Deleted patients remain excluded from research exports.
7. Existing RBAC/auth tests continue to pass.

Do not skip existing tests.

---

## Non-Goals
Do not implement in this phase:

- Clinical outcome after 72 hours.
- Prediction validation.
- Nurse training pre/post tests.
- Satisfaction surveys.
- Advanced statistical analytics.
- Complex clinical workflow engine.
- Device/IoT integration.

Those belong to later phases.

---

## Expected Files To Inspect
Inspect before editing:

- `app/models.py`
- `app/schemas.py`
- `app/database.py`
- `app/startup.py`
- `app/routers/patients.py`
- `app/routers/sessions.py` or equivalent session router
- `app/services/patient_service.py` or equivalent
- `app/services/session_service.py` or equivalent
- `app/services/export_service.py`
- `app/static/app.js`
- Existing patient/session/research tests

Names may differ; inspect the project before editing.

---

## Validation Commands
Run:

```bash
python -m compileall app
node --check app\static\app.js
python -m pytest
git diff --check
```

If `pytest` is not available directly, use:

```bash
python -m pytest
```

---

## Final Response Requirements
After implementation, report:

- Objective
- Files changed
- Backend changes
- Frontend changes
- Research dataset changes
- Test results
- Risk analysis
- Git commands

Include final GitHub commands:

```bash
git add .
git commit -m "Align baseline patient form with study protocol"
git push origin main
```
