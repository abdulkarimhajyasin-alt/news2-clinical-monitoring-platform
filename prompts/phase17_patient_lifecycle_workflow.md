# PHASE 17 — PATIENT DISCHARGE, ARCHIVE & SAFE DELETE WORKFLOW

## Objective

Implement a professional Patient Discharge, Archive, Restore, and Safe Delete workflow for the NEWS2 Hemodialysis Monitoring Platform.

The platform is medical/research-oriented, so patient data must not be casually hard-deleted. This phase must support safe operational discharge and archive behavior while preserving research traceability.

Hard delete must be restricted, audited, and protected by strong confirmation.

---

# CURRENT PROJECT STATE

The platform currently supports:

- Real authentication
- HTTP-only session cookies
- RBAC based on authenticated user role
- Patient list
- Add patient
- Patient profile selector
- Dialysis sessions
- Measurements
- NEWS2 assessments
- Alerts
- Deterioration events
- Clinical responses
- Response tracking
- Outcomes
- Research exports
- Research analytics
- Study management
- User management
- Technical admin role

Current problem:

There is no proper way to:

```text
discharge a patient
archive a patient
restore a patient
safely delete a patient file
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not break authentication.

Do not break RBAC.

Do not break patient list/profile/add workflows.

Do not break clinical workflow.

Do not break research exports/analytics.

Do not physically delete clinical data by default.

Do not drop tables.

Do not reset production data.

---

# MEDICAL SAFETY RULE

Default behavior must be:

```text
Discharge / Archive
```

not hard delete.

Hard delete must be exceptional and restricted to admin only.

---

# PATIENT STATUS MODEL

Add or use patient fields:

```text
status
discharged_at
discharge_reason
discharge_notes
archived_at
archived_by_user_id
deleted_at
deleted_by_user_id
delete_reason
```

If current model lacks these fields, add them safely and non-destructively.

Recommended status values:

```text
active
discharged
archived
deleted
```

Arabic labels:

```text
active      => نشط
discharged  => مُخرّج
archived    => مؤرشف
deleted     => محذوف
```

---

# WORKFLOW DEFINITIONS

## 1. Discharge Patient

Discharge means:

- Patient remains in database.
- Clinical/research data remains available.
- Patient disappears from active operational workflows by default.
- Patient appears in discharged patients list.
- No new dialysis sessions/measurements should be created unless patient is restored/reactivated.

Fields:

```text
status = discharged
discharged_at
discharge_reason
discharge_notes
```

---

## 2. Archive Patient

Archive means:

- Patient remains in database.
- Patient is hidden from normal active lists.
- Patient remains available for research/export if filters include archived.
- No new clinical workflow should be created.

Fields:

```text
status = archived
archived_at
archived_by_user_id
```

---

## 3. Restore Patient

Restore means:

```text
status = active
```

Clear or preserve historical discharge/archive fields? Prefer preserving fields as history if possible.

Patient returns to active patient lists.

---

## 4. Safe Delete Patient

Safe delete means:

```text
status = deleted
deleted_at
deleted_by_user_id
delete_reason
```

Do NOT physically delete related rows.

It should hide patient from normal UI and operational workflows.

Hard physical delete is NOT required in this phase.

If implemented, it must be admin-only, typed-confirmation protected, and should be deferred by default.

---

# RBAC PERMISSIONS

Add permissions:

```text
patients:discharge
patients:archive
patients:restore
patients:delete
```

Recommended access:

## admin

All.

## technical_admin

May archive/restore if allowed, but should not discharge clinically unless explicitly granted.

Recommended:

```text
patients:archive
patients:restore
```

No `patients:delete` unless admin.

## doctor

Allowed:

```text
patients:discharge
patients:restore
```

No delete.

## on_call_doctor

View only. No discharge/delete by default.

## nurse

View only.

## researcher

View only, may see discharged/archived in research context if allowed.

---

# BACKEND SERVICE

Create or update:

```text
app/services/patient_lifecycle_service.py
```

Functions:

```python
discharge_patient(db, patient_id, payload, current_user)
archive_patient(db, patient_id, payload, current_user)
restore_patient(db, patient_id, current_user)
soft_delete_patient(db, patient_id, payload, current_user)
```

Responsibilities:

- Validate patient exists.
- Prevent actions on already deleted patients except maybe admin restore.
- Update status fields.
- Write audit logs.
- Commit safely.
- Return updated patient.

---

# PYDANTIC SCHEMAS

Update:

```text
app/schemas.py
```

Add:

```text
PatientDischargeRequest
PatientArchiveRequest
PatientDeleteRequest
PatientLifecycleResult
```

Discharge request:

```text
discharge_reason
discharge_notes
```

Delete request:

```text
delete_reason
confirmation_text
```

Confirmation text must equal:

```text
DELETE PATIENT
```

or Arabic equivalent:

```text
حذف المريض
```

Prefer requiring exact Arabic phrase in UI:

```text
حذف المريض
```

---

# API ENDPOINTS

Update:

```text
app/routers/patients.py
```

Add:

```text
POST /api/patients/{id}/discharge
POST /api/patients/{id}/archive
POST /api/patients/{id}/restore
POST /api/patients/{id}/delete
```

Permissions:

```text
patients:discharge
patients:archive
patients:restore
patients:delete
```

Also update:

```text
GET /api/patients
```

Add filters:

```text
status
include_archived
include_deleted
```

Default behavior:

- Show only `active` patients unless specified.
- Do not show `deleted` unless `include_deleted=true` and user has admin permission.

---

# FRONTEND UI

Update:

```text
app/static/app.js
app/static/styles.css
```

## Patient List

Add filter tabs:

```text
المرضى النشطون
المرضى المُخرّجون
المرضى المؤرشفون
```

Admin only:

```text
المرضى المحذوفون
```

Show patient status badge.

---

## Patient Profile

Add lifecycle actions according to permissions:

For active patient:

```text
تخريج المريض
أرشفة المريض
```

For discharged/archived patient:

```text
استعادة المريض
```

For admin only:

```text
حذف ملف المريض
```

---

## Discharge Modal

Arabic title:

```text
تخريج المريض
```

Fields:

```text
سبب التخريج
ملاحظات التخريج
```

Buttons:

```text
تأكيد التخريج
إلغاء
```

Success:

```text
تم تخريج المريض بنجاح
```

---

## Archive Modal

Title:

```text
أرشفة المريض
```

Message:

```text
سيتم إخفاء المريض من القوائم التشغيلية مع الحفاظ على البيانات البحثية.
```

Button:

```text
تأكيد الأرشفة
```

---

## Restore Action

Confirm:

```text
هل تريد استعادة المريض إلى الحالة النشطة؟
```

Success:

```text
تمت استعادة المريض بنجاح
```

---

## Safe Delete Modal

Admin only.

Strong warning:

```text
تحذير مهم

سيتم إخفاء ملف المريض من النظام التشغيلي. ستبقى البيانات محفوظة في السجلات البحثية والتدقيق.
```

Require typing:

```text
حذف المريض
```

Field:

```text
سبب الحذف
```

Button:

```text
تأكيد الحذف
```

Success:

```text
تم حذف ملف المريض بشكل آمن
```

---

# CLINICAL WORKFLOW BLOCKING

If patient status is not active:

Prevent or warn when attempting:

```text
create session
create measurement
NEWS2 assessment
new alert workflow
```

At minimum, frontend should disable actions for discharged/archived/deleted patients.

Backend should enforce for patient-specific create endpoints where practical.

---

# RESEARCH EXPORT BEHAVIOR

Do not remove discharged/archived patients from research datasets by default unless the dataset filter specifies active only.

Deleted patients should preferably be excluded from normal exports unless admin/research governance says include deleted.

For this phase:

- active/discharged/archived may remain in research dataset.
- deleted should be excluded from default operational views.

---

# AUDIT LOGS

Add audit entries:

```text
patient_discharged
patient_archived
patient_restored
patient_soft_deleted
```

Include:

```text
patient_id
patient_code
actor_user_id
reason
```

Do not log sensitive unnecessary details.

---

# TESTS

Create:

```text
tests/test_patient_lifecycle_workflow.py
```

Required tests:

1. Discharge active patient.
2. Discharged patient no longer appears in default GET /api/patients.
3. GET /api/patients?status=discharged shows discharged patient.
4. Archive patient.
5. Restore patient.
6. Soft delete patient requires admin permission.
7. Doctor can discharge but cannot delete.
8. Nurse cannot discharge/delete.
9. Delete requires confirmation text.
10. Audit logs created.
11. Research summary does not crash with discharged/archived patients.
12. Existing patient profile/list tests still pass.

Update RBAC tests for new permissions.

---

# DOCUMENTATION

Create:

```text
docs/patient_lifecycle.md
```

Update:

```text
README.md
docs/system_architecture.md
docs/rbac.md
docs/research_workflow.md
```

Document:

- difference between discharge/archive/delete
- why hard delete is avoided
- permissions
- research implications
- audit behavior

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual validation:

1. Login as admin.
2. Open Patient List.
3. Open patient profile.
4. Discharge patient.
5. Confirm it disappears from active list.
6. Switch to discharged tab.
7. Restore patient.
8. Archive patient.
9. Confirm archived tab works.
10. Try delete as doctor; should be blocked.
11. Delete as admin with confirmation.
12. Confirm audit log exists.
13. Confirm research dashboard still loads.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Add patient discharge archive and safe delete workflow"
git push origin main
```

Render auto-deploys.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Patient lifecycle architecture
4. API endpoints added
5. RBAC permissions added
6. Frontend lifecycle UI
7. Audit logs
8. Research/export behavior
9. Tests added/updated
10. Validation results
11. Deployment commands
12. Risks

---

# NEXT PHASE

Recommended next phase:

```text
Phase 18 — Production Security Hardening
```

Focus:

```text
CSRF
rate limiting
password change
admin password rotation
security headers
favicon/branding cleanup
