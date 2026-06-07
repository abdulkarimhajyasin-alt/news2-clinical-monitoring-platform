# UI/FLOW FIX — PATIENT PROFILE MUST ALLOW SELECTING A PATIENT FIRST

## Objective

Fix the Patient Profile screen so that it does not show a random/default patient automatically without allowing the user to select a patient.

When the user clicks:

```text
ملف المريض
```

the app should first show a real patient selection list. Clicking a patient should open that selected patient's profile.

---

# CURRENT PROBLEM

The route/screen:

```text
ملف المريض
```

currently opens a patient profile view directly, showing one patient such as:

```text
patient_code = 512
```

But there is no patient list or selector on that screen.

Expected behavior:

1. User clicks `ملف المريض`.
2. App shows a list of patients from the real API.
3. User clicks a patient row/card.
4. App opens the profile for that selected patient.
5. The profile data must match the selected patient.

---

# CRITICAL RULES

Do not redesign the full UI.

Do not break existing patient list.

Do not break Add Patient.

Do not break API integration.

Do not change backend unless a minimal read endpoint is needed.

Do not remove current patient profile cards/charts.

Do not change database schema.

This is primarily frontend workflow/navigation fix.

---

# REQUIRED UX

## Patient Profile Landing State

When route is:

```text
#patient-profile
```

or the equivalent existing route for:

```text
ملف المريض
```

and no patient is selected:

Show:

```text
اختر مريضاً لعرض الملف
```

Then show patient list/table/cards.

Use real data from:

```text
GET /api/patients
```

Each row/card should include:

```text
patient_code
age
gender
study_phase
study_group
weekly_sessions_count
```

Arabic labels only.

---

## Patient Selection

When clicking a patient:

- Save selected patient ID/code in frontend state.
- Open profile view for that patient.
- Prefer route parameter/hash if current router supports it, for example:

```text
#patient-profile/1
```

or:

```text
#patient-profile?patient_id=1
```

If the router does not support route params cleanly, use internal state safely:

```javascript
appState.selectedPatientId
```

But route-based selection is preferred.

---

## Profile View

After selecting a patient, display:

```text
ملف المريض
```

with selected patient data:

```text
patient_code
age
gender
study_phase
study_group
dialysis_vintage_months
weekly_sessions_count
```

If available, also show:

```text
latest dialysis sessions
NEWS2 trend
alerts
deterioration events
outcomes
```

Only use real API data already available. If some related data is unavailable, show empty states, not fake unrelated data.

---

## Back to Selection

Add button:

```text
اختيار مريض آخر
```

This returns to the patient selector list.

---

# PATIENT LIST IN PROFILE SCREEN

The selector should look professional and match the current medical UI.

Options:

- table
- cards
- search/filter input

Required:

```text
Search by patient code
Search by patient name if available
```

Arabic placeholder:

```text
ابحث برمز المريض أو الاسم...
```

---

# FIELD MAPPING

Use the API patient fields:

```text
id
patient_code
full_name
age
gender
study_phase
study_group
dialysis_vintage_months
weekly_sessions_count
is_anonymized
```

If `full_name` is available and appropriate in UI, it can appear in clinical UI, but do not expose it in research exports.

---

# EMPTY / ERROR STATES

If no patients:

```text
لا توجد بيانات مرضى حتى الآن
```

If API fails:

```text
تعذر تحميل قائمة المرضى
```

If selected patient not found:

```text
لم يتم العثور على المريض المحدد
```

---

# ROUTE INTEGRATION

Update navigation behavior:

- Clicking `ملف المريض` should open the selector, not an arbitrary profile.
- Clicking a patient from `قائمة المرضى` may still route to the profile directly if that behavior already exists.
- If patient list rows are clickable, clicking row should open that patient profile.

---

# FRONTEND FILES

Modify:

```text
app/static/app.js
```

Modify:

```text
app/static/styles.css
```

only if needed for minor selector layout.

---

# OPTIONAL BACKEND SUPPORT

If current APIs do not support `GET /api/patients/{id}`, add it.

Endpoint:

```text
GET /api/patients/{id}
```

Return one patient.

Protect with:

```text
patients:view
```

Only add this if necessary. If the frontend can use existing patient list, no backend change required.

---

# TESTS

If backend endpoint is added, add/update tests:

```text
tests/test_patient_profile_selection.py
```

Required backend tests only if endpoint added:

1. GET /api/patients/{id} returns patient.
2. Invalid ID returns 404.
3. patients:view permission is respected if implemented.

Frontend validation remains manual plus:

```bash
node --check app/static/app.js
```

---

# MANUAL VALIDATION

Verify:

1. Open app.
2. Click `ملف المريض`.
3. Patient selection list appears.
4. Click patient ANON-P-1001.
5. Profile shows ANON-P-1001.
6. Click `اختيار مريض آخر`.
7. Select another patient.
8. Profile changes to that patient.
9. Search/filter works.
10. No random/default patient is shown without selection.
11. Patient list row click from `قائمة المرضى` opens selected profile if supported.

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Add patient selector before profile view"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Patient profile workflow fix
4. Route behavior
5. Selector/search behavior
6. Backend changes if any
7. Validation results
8. Deployment commands
9. Risks
