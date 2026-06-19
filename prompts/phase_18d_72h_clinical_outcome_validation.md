# Phase 18D — 72-Hour Clinical Outcome Validation

## Objective
Implement the doctor’s final **Clinical Outcome after 72 hours** form exactly as a study-aligned validation workflow for the NEWS2 / HD2-mNEWS hemodialysis monitoring platform.

This phase must make the platform compliant with the latest doctor-provided digital monitoring form by adding a dedicated post-session clinical validation module that appears only after 72 hours from the dialysis session.

The purpose is to document whether clinical deterioration occurred, what type occurred, when it occurred, whether the platform predicted it, what intervention was performed, and what the final result was.

## Critical Scope Rule
Do not build generic hospital outcome management. Implement only what is required by the doctor’s final monitoring form.

Preserve:
- Existing NEWS2 workflow
- Existing HD2-mNEWS workflow
- Existing alert behavior
- Existing response workflow
- Existing research export behavior
- Existing RBAC/authentication/session security
- Existing patient lifecycle restrictions
- Existing Arabic RTL design identity

Do not add unrelated EMR, hospital, scheduling, bed, staff shift, or broad clinical modules.

---

## Required Feature Name
Use a clear internal naming convention such as:

- `ClinicalOutcomeValidation`
- `SessionOutcomeValidation`
- `OutcomeValidation72h`

Prefer names that clearly indicate this is a **72-hour post-dialysis clinical validation** feature.

---

## Functional Requirements

### 1. Add 72-Hour Visibility Rule
Add a new patient/session outcome validation tab or section named in Arabic:

`النتيجة السريرية بعد 72 ساعة`

It must be linked to a dialysis session.

Visibility / access logic:
- The form should not be available for completion until 72 hours have passed from the session start time or session end time.
- If end time exists, prefer session end time.
- If no end time exists, use actual session start time plus session duration when available.
- If neither end time nor duration is available, use actual start time.
- Before 72 hours, show a professional Arabic message such as:
  - `لا يمكن توثيق النتيجة السريرية قبل مرور 72 ساعة على الجلسة.`
  - Show the remaining time if reasonably easy.

Do not block viewing already completed records, but do block creation/update before eligibility unless the current user has an explicit admin override permission already present in the system.

If no such override permission exists, do not invent a broad permission. Keep the rule strict.

---

### 2. Main Question: Did Deterioration Occur?
The form must start with:

`هل حدث تدهور؟`

Allowed values:
- `yes`
- `no`

Arabic labels:
- `نعم`
- `لا`

Behavior:
- If `no`, show only:
  - Notes field
  - Data validation/source verification field
- If `yes`, show all detailed follow-up fields below.

---

### 3. Deterioration Type
If deterioration occurred, allow selecting one or more deterioration types from the exact study list:

1. `severe_hypotension` — `هبوط ضغط شديد`
2. `cardiac_arrhythmia` — `اضطراب نظم قلبي`
3. `electrolyte_disorder` — `اضطراب كهرلي`
4. `vascular_access_complication` — `مضاعفات فيستولا / وصول وعائي`
5. `neurological_deterioration` — `تدهور عصبي`
6. `emergency_admission` — `دخول طارئ`
7. `icu_transfer` — `تحويل للعناية`
8. `death` — `وفاة`

Support multi-select because more than one outcome may occur.

---

### 4. Conditional Fields by Deterioration Type
Implement conditional fields as described by the doctor’s form.

#### Severe Hypotension
When selected, show:
- `lowest_sbp` — lowest systolic blood pressure
- `required_treatment` — did it require treatment? yes/no

Arabic labels:
- `الضغط الأدنى`
- `هل تطلب علاج؟`

#### Cardiac Arrhythmia
When selected, show:
- `arrhythmia_type`

Arabic label:
- `نوع اضطراب النظم`

Suggested values:
- `tachycardia`
- `bradycardia`
- `irregular_rhythm`
- `unknown`
- `other`

Allow free notes for other.

#### Electrolyte Disorder
When selected, show:
- `potassium_value`

Arabic label:
- `قيمة البوتاسيوم`

#### Vascular Access Complication
When selected, show:
- `vascular_complication_type`

Arabic options:
- `تجلط`
- `نزيف`
- `عدوى`
- `أخرى`

#### Neurological Deterioration
When selected, show:
- `neurological_type`

Arabic options:
- `فقدان وعي`
- `تشنج`
- `سكتة`
- `أخرى`

#### Emergency Admission
When selected, show:
- `emergency_admission_datetime`
- `emergency_admission_reason`

Arabic labels:
- `تاريخ ووقت الدخول الطارئ`
- `سبب الدخول الطارئ`

#### ICU Transfer
When selected, show:
- `icu_transfer_datetime`

Arabic label:
- `تاريخ ووقت التحويل للعناية`

#### Death
When selected, show:
- `death_datetime`
- `death_reason`

Arabic labels:
- `تاريخ ووقت الوفاة`
- `سبب الوفاة`

---

### 5. When Did Deterioration Occur?
If deterioration occurred, add:

`متى حدث التدهور؟`

Allowed timing categories:
1. `during_session` — `أثناء الجلسة`
2. `within_6h_after_session` — `بعد الجلسة خلال 6 ساعات`
3. `within_24_72h` — `خلال 24-72 ساعة`

Conditional fields:
- During session: time field only
- Within 6h: time field only if same date is known; otherwise datetime field
- Within 24-72h: datetime field

Keep this practical and consistent with existing date/time handling.

---

### 6. Did the Platform Predict Deterioration?
If deterioration occurred, add:

`هل تنبأت المنصة بالتدهور؟`

Allowed values:
1. `predicted_before` — `نعم - تنبأت قبل الحدوث`
2. `predicted_concurrent` — `نعم - متزامناً مع الحدوث`
3. `not_predicted` — `لا - حدث بدون تنبيه`
4. `false_negative` — `لم يُصدر تنبيه - False Negative`

This field is essential for the research study and must be included in API, persistence, UI, and research export.

---

### 7. Intervention Taken and Result
If deterioration occurred, add multi-select interventions:

- `doctor_called` — `استدعاء الطبيب`
- `fluids_given` — `إعطاء محاليل`
- `machine_settings_adjusted` — `تعديل إعدادات الجهاز`
- `dialysis_stopped` — `إيقاف الغسيل`
- `emergency_medications_given` — `إعطاء أدوية طارئة`
- `ed_transfer` — `تحويل للطوارئ`

Conditional rule:
- If `doctor_called` is selected, show:
  - `doctor_response_time_minutes`
  - Arabic label: `زمن استجابة الطبيب بالدقائق`

Final result — single choice:
- `full_improvement` — `تحسن كامل`
- `partial_improvement` — `تحسن جزئي`
- `no_improvement` — `لم يتحسن`
- `further_deterioration` — `تدهور إضافي`

---

### 8. Data Verification / Source Validation
Add required multi-select field:

`التحقق من صحة البيانات`

At least one option must be selected before saving:
- `medical_record_reviewed` — `تمت مراجعة السجل الطبي`
- `nurse_interviewed` — `تمت مقابلة الممرض`
- `phone_followup_done` — `تمت المتابعة الهاتفية`
- `independent_doctor_verified` — `تم التحقق من طبيب مستقل`

This field is required whether deterioration occurred or not.

---

### 9. Notes
Add general notes field:

`ملاحظات`

Required only when deterioration did not occur, optional otherwise.

---

## Backend Requirements

### Database
Add a dedicated table if one does not already exist.

Recommended fields:
- id
- patient_id
- session_id
- deterioration_occurred
- deterioration_types JSON/list
- type_specific_details JSON
- deterioration_timing_category
- deterioration_time
- deterioration_datetime
- platform_prediction_status
- interventions JSON/list
- doctor_response_time_minutes
- final_result
- verification_sources JSON/list
- notes
- completed_by_user_id
- completed_at
- created_at
- updated_at

Use nullable fields where appropriate.

Add safe startup/runtime schema guards compatible with existing SQLite/PostgreSQL deployment style.

Do not physically delete records by default.

### API
Add protected endpoints, for example:

- `GET /api/outcome-validations`
- `GET /api/outcome-validations/session/{session_id}`
- `POST /api/outcome-validations`
- `PUT /api/outcome-validations/{id}`

Rules:
- One validation per dialysis session unless there is a strong existing project pattern for versioning.
- Validate patient/session relationship.
- Enforce 72-hour eligibility on create/update.
- Enforce patient lifecycle restrictions where appropriate.
- Use existing RBAC patterns. If there are outcome permissions already, reuse them. Do not invent unrelated roles.

### Schemas
Add Pydantic request/response schemas with clear enum-like validation where possible.

### Audit Logs
Create audit log events for:
- validation created
- validation updated

Use the existing audit logging pattern.

---

## Frontend Requirements

### UI Placement
Add or update the existing Arabic page/route:

`النتيجة السريرية`

The page should allow selecting:
- patient
- dialysis session

Then display:
- eligibility status
- existing validation if present
- form if eligible

### Arabic RTL UX
Use clear section headings:

1. `هل حدث تدهور؟`
2. `نوع التدهور`
3. `توقيت التدهور`
4. `تنبؤ المنصة`
5. `الإجراء المتخذ والنتيجة`
6. `التحقق من صحة البيانات`
7. `ملاحظات`

Keep the UI professional, medical, and consistent with the existing design.

### Conditional Display
Implement frontend conditional logic matching the doctor’s form.

### List / Summary
Where existing outcome lists are shown, add compact badges for:
- deterioration occurred yes/no
- prediction status
- final result
- verification status

---

## Research Dataset / Export Requirements
Extend the research dataset and CSV/XLSX/SPSS export/codebook outputs with fields such as:

- outcome_validation_completed
- outcome_validation_completed_at
- deterioration_occurred
- deterioration_types
- deterioration_timing_category
- platform_prediction_status
- interventions
- doctor_response_time_minutes
- final_result
- verification_sources
- severe_hypotension_lowest_sbp
- severe_hypotension_required_treatment
- arrhythmia_type
- potassium_value
- vascular_complication_type
- neurological_type
- emergency_admission_datetime
- emergency_admission_reason
- icu_transfer_datetime
- death_datetime
- death_reason

Preserve deleted-patient exclusion.

---

## Analytics Preparation
Do not build full sensitivity/specificity analytics in this phase unless trivial.

However, add enough structured fields so Phase 19 can calculate:
- predicted before deterioration
- predicted concurrently
- not predicted
- false negative
- deterioration occurred yes/no
- intervention type
- doctor response time
- outcome result

---

## Tests Required
Add or update tests covering:

1. Cannot create validation before 72 hours.
2. Can create validation after 72 hours.
3. `no deterioration` path requires notes and verification source.
4. `yes deterioration` path requires deterioration type, timing, prediction status, intervention/result, and verification source.
5. Conditional type-specific details persist correctly.
6. Doctor response time is required/accepted when doctor called is selected.
7. One validation per session duplicate protection.
8. Research export includes validation fields.
9. Deleted patients remain excluded from research exports.
10. Existing tests continue passing.

Run:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

---

## GitHub Commands
After successful validation, provide final Git commands:

```bash
git add .
git commit -m "Add 72-hour clinical outcome validation"
git push origin main
```

---

## Final Response Required from Codex
When finished, respond with:

- Objective summary
- Files changed
- Backend changes
- Frontend changes
- Research/export changes
- Tests added/updated
- Validation results
- Risk analysis
- Final GitHub commands
