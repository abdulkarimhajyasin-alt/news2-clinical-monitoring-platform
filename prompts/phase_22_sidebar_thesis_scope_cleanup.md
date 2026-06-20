# Phase 22 — Sidebar Thesis Scope Cleanup & HD2-mNEWS Navigation Alignment

## Objective

Refine the right sidebar navigation so the platform exposes only the screens that directly serve the PhD research scope and the final digital monitoring form.

The platform must stay focused on:

1. Patient baseline/context data.
2. Dialysis sessions.
3. Digital monitoring measurements.
4. HD2-mNEWS scoring and history.
5. Alerts.
6. Clinical deterioration documentation.
7. Clinical response documentation.
8. 72-hour clinical outcome validation.
9. Research dataset/export.
10. Research analytics and prediction evaluation.
11. Nurse training and acceptance.
12. Study protocol.
13. Final thesis alignment audit.
14. Admin-only user management.

Do not add broad hospital-system features, technical admin pages, unrelated dashboards, or duplicate sidebar entries.

---

## Source of Truth

Use only the two thesis documents already used in this project:

1. The PhD research proposal about the effectiveness of NEWS2-based digital monitoring in detecting clinical deterioration among hemodialysis patients.
2. The final digital monitoring form defining:
   - Patient baseline/context form.
   - HD2-mNEWS variables.
   - Green/yellow/red risk colors.
   - Nursing protocol by risk level.
   - 72-hour clinical outcome validation.
   - Prediction validation.

The sidebar must not expose anything outside this scope.

---

## Current Problem

The sidebar still contains items that either:

- use old NEWS2 wording after the project moved to HD2-mNEWS,
- duplicate functionality,
- expose pages that are technically useful but not directly needed by the doctor/research workflow,
- split one research workflow into too many subpages.

Examples seen in the current sidebar:

- `تقييم NEWS2`
- `سجل NEWS2`
- `استجابة الطبيب`
- `استجابة التمريض`
- `زمن الاستجابة`
- `مؤشرات البحث`
- `جودة البيانات`

These should be renamed, merged, or hidden from the sidebar according to the rules below.

---

## Required Final Sidebar Structure

### 1. الرئيسية

Keep:
- `الرئيسية`

### 2. المرضى

Keep:
- `المرضى`
- `ملف المريض`
- `البيانات الأساسية`
- `إضافة مريض`

Reason: These directly support the baseline/context patient form.

### 3. جلسات الغسيل

Keep:
- `جلسات الغسيل`
- `تسجيل جلسة`

Reason: Dialysis session context is required by the study and the HD2-mNEWS calculation.

### 4. المراقبة الرقمية

Keep:
- `إدخال القياسات`

Rename old NEWS2 items:
- `تقييم NEWS2` → `نتيجة HD2-mNEWS`
- `سجل NEWS2` → `سجل HD2-mNEWS`

Reason: The final monitoring form is based on the modified hemodialysis score HD2-mNEWS, not only standard NEWS2.

Important:
If the existing routes are still internally named with NEWS2 identifiers, do not break them. Keep route keys if needed, but update visible Arabic labels and page titles to HD2-mNEWS wording.

### 5. التنبيهات

Keep:
- `التنبيهات`

### 6. الاستجابة السريرية

Keep:
- `توثيق التدهور`
- `الاستجابة السريرية`

Hide from sidebar and merge conceptually into `الاستجابة السريرية`:
- `استجابة الطبيب`
- `استجابة التمريض`
- `زمن الاستجابة`

Do not delete backend endpoints or service code. Only hide unnecessary sidebar entries unless safely removable without breaking tests.

### 7. النتيجة السريرية

Keep:
- `تتبع النتيجة`
- `النتيجة السريرية`

If possible, adjust visible label to:
- `النتيجة السريرية 72 ساعة`

### 8. بيانات البحث

Keep:
- `بيانات البحث`

### 9. التحليل البحثي

Keep:
- `التحليل البحثي`
- `تقييم التنبؤ`
- `تدريب التمريض`
- `تدقيق مطابقة الرسالة`

Hide from sidebar:
- `مؤشرات البحث`
- `جودة البيانات`

These can remain internal sections/cards inside analytics or dataset pages.

### 10. بروتوكول الدراسة

Keep:
- `بروتوكول الدراسة`

### 11. إدارة المستخدمين

Keep:
- `إدارة المستخدمين`

Keep admin-only permission gates.

---

## Critical UI Naming Requirements

Replace or adjust these user-visible labels:

- `تقييم NEWS2` → `نتيجة HD2-mNEWS`
- `سجل NEWS2` → `سجل HD2-mNEWS`
- `اتجاه NEWS2` → `اتجاه HD2-mNEWS` or `اتجاه NEWS2 / HD2-mNEWS`
- `NEWS2 Assessments` → `HD2-mNEWS Assessments` or Arabic equivalent where visible.
- Any page title that shows only NEWS2 for the study-specific monitoring workflow should mention HD2-mNEWS.

Do not rename the original standard NEWS2 API endpoint if it is still used for compatibility. This task is primarily navigation and visible UI scope alignment.

---

## Implementation Rules

1. Preserve backend APIs unless a route is clearly unused and tests prove safe removal.
2. Preserve RBAC permission checks.
3. Preserve internal deep routes if other workflows depend on them.
4. Do not remove data, models, services, or database columns.
5. Do not break existing tests.
6. Do not add new unrelated features.
7. Keep Arabic RTL labels professional and clinically understandable.
8. Keep the current design identity and layout.
9. Avoid destructive migrations.
10. If a removed sidebar item still has a valid internal screen, hide it from navigation rather than deleting it.

---

## Expected Files to Inspect / Modify

Likely files:

- `app/static/app.js`
- `app/static/styles.css` only if minor visual spacing is needed.
- Existing navigation-related tests.
- Add or update a regression test for sidebar scope.

Do not modify backend unless needed for visible labels returned by APIs or tests.

---

## Regression Test Requirements

Add or update tests to verify:

1. Sidebar contains required thesis-scope items:
   - `الرئيسية`
   - `المرضى`
   - `ملف المريض`
   - `البيانات الأساسية`
   - `إضافة مريض`
   - `جلسات الغسيل`
   - `تسجيل جلسة`
   - `المراقبة الرقمية`
   - `إدخال القياسات`
   - `نتيجة HD2-mNEWS`
   - `سجل HD2-mNEWS`
   - `التنبيهات`
   - `توثيق التدهور`
   - `الاستجابة السريرية`
   - `النتيجة السريرية`
   - `بيانات البحث`
   - `التحليل البحثي`
   - `تقييم التنبؤ`
   - `تدريب التمريض`
   - `تدقيق مطابقة الرسالة`
   - `بروتوكول الدراسة`
   - `إدارة المستخدمين`

2. Sidebar does not contain out-of-scope or duplicate items:
   - `استجابة الطبيب`
   - `استجابة التمريض`
   - `زمن الاستجابة`
   - `مؤشرات البحث`
   - `جودة البيانات`
   - old visible `تقييم NEWS2`
   - old visible `سجل NEWS2`

3. Internal routes may remain available if compatibility requires them, but they must not be visible in sidebar navigation.

---

## Validation Commands

Run:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

If the project uses Windows path separators, the equivalent is acceptable:

```powershell
python -m compileall app
node --check app\static\app.js
python -m pytest
git diff --check
```

---

## Deliverable Summary Required From Codex

After implementation, report:

1. Objective.
2. Files changed.
3. Exact sidebar items kept.
4. Exact sidebar items renamed.
5. Exact sidebar items hidden/removed.
6. Whether internal routes were preserved.
7. Tests added/updated.
8. Validation results.
9. Risk analysis.
10. Final Git commands.

---

## Final Git Commands

After successful validation, provide:

```bash
git add .
git commit -m "Align sidebar with thesis monitoring scope"
git push origin main
```
