# FIX — ENABLE REAL PATIENT CREATION WORKFLOW

## Objective

Fix the "Add Patient" screen so that new patients are actually saved to the backend database and become visible in the patient list.

The deployed app currently shows the Add Patient form, but submitting the form does not persist a patient. This fix must implement the missing real patient creation workflow end-to-end.

---

# CURRENT PROBLEM

The Add Patient screen exists in the Arabic RTL frontend, but clicking:

```text
حفظ
```

does not create a new patient in the database.

The current production deployment is live on Render with Neon PostgreSQL, and read APIs work:

```text
GET /api/patients
GET /api/research/summary
```

But patient creation is missing or not connected.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.
Do not break existing patient list.
Do not break monitoring, NEWS2, alerts, deterioration, responses, outcomes, exports, analytics, RBAC, or deployment startup initialization.
Do not remove seeded patients.
Do not change database tables destructively.
Do not implement full authentication in this fix.
Use current RBAC development role behavior.

---

# REQUIRED BACKEND WORK

## Add Patient Create Schema

Update:

```text
app/schemas.py
```

Add or complete:

```python
PatientCreate
PatientRead
PatientCreateResult
```

PatientCreate should support at minimum:

```text
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
```

Because the current UI may use Arabic labels and older fields like birth date / access type / dialysis plan, map only what belongs to the existing patients table.

Do not add unnecessary columns unless already present in the model.

---

## Add Service Function

Update or create in:

```text
app/services/patient_service.py
```

Function:

```python
create_patient(db, payload)
```

Responsibilities:

1. Validate patient_code is unique.
2. Create patient row.
3. Apply safe defaults:
   - study_phase = post_implementation if missing
   - study_group = intervention if missing
   - is_anonymized = true by default
4. Commit safely.
5. Return created patient.

If full_name is considered sensitive, it may be stored internally but should not be exported by research exports.

---

## Add POST API

Update:

```text
app/routers/patients.py
```

Add:

```text
POST /api/patients
```

Requirements:

- Protected by RBAC permission:

```text
patients:create
```

- Returns created patient JSON.
- Returns 409 if patient_code already exists.
- Returns 422 for invalid input.
- Returns 201 on success.

---

# FRONTEND WORK

Update:

```text
app/static/app.js
```

Connect the Add Patient screen to:

```text
POST /api/patients
```

Required behavior:

1. Collect form values.
2. Normalize Arabic form inputs into backend fields.
3. Generate safe defaults for missing required research fields.
4. Submit to API.
5. Show loading state while saving.
6. Show success message:

```text
تم حفظ المريض بنجاح
```

7. Show error message:

```text
تعذر حفظ المريض
```

8. After success:
   - Refresh patient list data.
   - Navigate to Patient List or clear form.
   - Ensure the new patient appears in `/api/patients`.

---

# FIELD MAPPING

The current visible form contains:

```text
الاسم الكامل
رقم الملف
تاريخ الميلاد
الجنس
نوع الوصول الوعائي
الأمراض المصاحبة
خطة الغسيل
ملاحظات سريرية
```

Map as follows:

```text
رقم الملف             => patient_code
الاسم الكامل          => full_name
الجنس                 => gender
الأمراض المصاحبة      => comorbidities
```

If age is required but the UI has birth date:

- Calculate age from birth date if possible.
- Otherwise require age input or add age field.
- Prefer adding an age field if missing to avoid incorrect calculations.

Temporary defaults if not provided:

```text
target_dry_weight = null
dialysis_start_date = null
dialysis_vintage_months = null
weekly_sessions_count = 3
charlson_comorbidity_index = null
baseline_functional_status = null
study_phase = post_implementation
study_group = intervention
is_anonymized = true
```

Do not store vascular access in patient table unless the existing model supports it. Vascular access workflow can be handled separately later.

---

# UI REQUIREMENTS

Keep Arabic RTL.

Add professional validation:

- Patient code required.
- Full name required.
- Gender required.
- Age or date of birth required if model requires age.

Add duplicate patient_code error handling:

```text
رقم الملف مستخدم مسبقاً
```

Add save button disabled state while submitting.

Do not make the page look different from current design.

---

# API CLIENT

Extend frontend API client with:

```javascript
api.createPatient(payload)
```

Use the existing fetch wrapper and RBAC dev role header.

---

# TESTS

Add or update:

```text
tests/test_patient_create_workflow.py
```

Required tests:

1. Create patient succeeds.
2. Created patient appears in GET /api/patients.
3. Duplicate patient_code returns 409.
4. Invalid payload returns 422.
5. Nurse cannot create patient if RBAC matrix does not allow it.
6. Doctor/admin can create patient.
7. Research exports still exclude patient full_name.
8. Existing tests still pass.

---

# DOCUMENTATION

Update:

```text
README.md
docs/system_architecture.md
```

Add note:

```text
Patient creation workflow is now connected to the backend and persists to PostgreSQL.
```

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Also run locally:

```bash
uvicorn app.main:app --reload
```

Manual validation:

1. Open Add Patient screen.
2. Enter a new patient.
3. Click حفظ.
4. Confirm success message.
5. Open Patient List.
6. Confirm patient appears.
7. Open:

```text
/api/patients
```

Confirm new patient exists.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Enable patient creation workflow"
git push origin main
```

Render will auto-deploy.

After deploy, validate on production:

```text
https://news2-clinical-monitoring.onrender.com/api/patients
```

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Backend patient creation implementation
4. Frontend form integration
5. Validation and duplicate handling
6. RBAC behavior
7. Tests added or updated
8. Validation results
9. Deployment commands
10. Risks
