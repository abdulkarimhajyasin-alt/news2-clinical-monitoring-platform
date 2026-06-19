# Phase 21 — Final Research Alignment Audit

## Objective
Perform a final, strict alignment audit to ensure the NEWS2 Hemodialysis Monitoring Platform matches only the two doctor-approved source documents:

1. The PhD research proposal for NEWS2-based digital monitoring in hemodialysis patients.
2. The final digital monitoring form defining the baseline/context fields, HD2-mNEWS scoring, nursing protocol, 72-hour clinical outcome validation, prediction question, and data verification fields.

This phase is an audit, correction, cleanup, and export-alignment phase. Do not add broad hospital-management, EMR, AI, mobile, IoT, scheduling, billing, or unrelated operational features.

## Current Baseline
The project already includes:
- Authentication, RBAC, user management, audit logs.
- Patient lifecycle.
- Dialysis sessions.
- Monitoring measurements.
- Standard NEWS2 preserved for compatibility.
- HD2-mNEWS engine with 10 variables.
- Risk color and nursing protocol guidance.
- 72-hour clinical outcome validation.
- Prediction accuracy research evaluation.
- Nurse training, competency, acceptance scoring, and CSV export.
- Research dataset/export center.

## Source-of-Truth Scope
The platform must support only what is required by the research documents:

### Research Proposal Requirements
- Quasi-experimental study design.
- Control group versus experimental group.
- Patient demographic and clinical data collection.
- Digital NEWS2/HD2-mNEWS monitoring.
- Response time measurement.
- ICU transfer / emergency events / mortality outcome tracking.
- Nurse pre-test and post-test.
- Training/competency evaluation.
- Staff satisfaction/acceptance survey.
- Research dataset and export.

### Digital Monitoring Form Requirements
- Baseline patient/context form.
- HD2-mNEWS 10-variable scoring.
- Risk colors: green, yellow, red.
- Automatic red for critical variables.
- Nursing protocol by risk color.
- 72-hour clinical outcome validation.
- Deterioration type fields.
- Prediction question.
- Intervention/result fields.
- Verification-source fields.

## Tasks

### 1. Build a Final Alignment Matrix
Create a backend service and protected API endpoint that returns a structured alignment matrix:

`GET /api/research/alignment-audit`

The matrix should include rows for each required item from the two source documents:
- requirement key
- Arabic label
- English technical label
- source document category
- status: implemented / partial / missing / out_of_scope
- related API route if available
- related frontend route if available
- related export field names if available
- notes

Do not invent requirements beyond the two documents.

### 2. Add Arabic UI Page
Add a sidebar/page named:

`تدقيق مطابقة الرسالة`

The page should show:
- overall completion percentage
- implemented count
- partial count
- missing count
- out-of-scope count
- grouped requirement table
- clear Arabic notes explaining what remains

Keep the page visually consistent with the current Arabic RTL medical UI.

### 3. Export Field Audit
Verify that the research dataset/export includes all thesis-relevant fields:

Baseline/context:
- encrypted/medical patient code
- age
- gender
- education level
- dry weight
- dialysis start date
- weekly sessions count
- comorbidities
- vascular access type
- vascular access location
- vascular access placement date
- session date
- weekday
- actual session start time
- target fluid removal ml

HD2-mNEWS:
- RR, SpO2, Temp, SBP, HR, AVPU
- Fistula/access status
- IDWG%
- UFR
- potassium
- component scores
- total HD2 score
- risk color
- critical trigger metadata
- nursing protocol label / reassessment window

Clinical outcome validation:
- 72h validation completion
- deterioration occurred
- deterioration types
- timing category
- timing values
- prediction status
- intervention list
- doctor response time
- final result
- verification sources

Training/acceptance:
- pre-test score
- post-test score
- improvement
- competency score/status
- acceptance score/level

Prediction evaluation:
- prediction classification
- true positive / false negative / true negative / false positive markers
- early detection marker
- classification reason

If fields are missing, add them in a backward-compatible way.

### 4. Out-of-Scope Visibility Check
Ensure the sidebar does not expose unrelated pages. Keep backend compatibility routes if already present, but do not expose unrelated features in the sidebar.

Required visible sidebar scope should remain focused on:
- الرئيسية
- المرضى
- جلسات الغسيل
- المراقبة الرقمية
- التنبيهات
- الاستجابة السريرية
- النتيجة السريرية
- بيانات البحث
- التحليل البحثي
- تقييم التنبؤ
- تدريب التمريض
- بروتوكول الدراسة
- تدقيق مطابقة الرسالة
- إدارة المستخدمين only for authorized admin users

### 5. Regression Tests
Add tests covering:
- alignment audit endpoint permissions
- alignment matrix includes the two document-driven requirement groups
- no unrelated broad hospital-management requirements are added
- export dataset includes required final research fields
- deleted patients remain excluded
- sidebar includes the alignment audit page and does not reintroduce out-of-scope items

### 6. Do Not Break Existing Behavior
Preserve:
- authentication
- RBAC
- current tests
- NEWS2 compatibility
- HD2-mNEWS scoring
- monitoring workflow
- alert workflow
- 72-hour validation
- prediction evaluation
- training module
- research exports
- deleted patient exclusion

## Validation Commands
Run:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

All tests must pass.

## Final Response Requirements
After implementation, report:
- changed files
- alignment audit summary
- missing/partial items if any
- test results
- risk analysis
- final GitHub commands

Include final commands:

```bash
git add .
git commit -m "Add final thesis alignment audit"
git push origin main
```
