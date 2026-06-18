# Codex Prompt — Phase 18 Navigation Scope Cleanup

## Objective
Clean up the right-side navigation menu and remove or hide all pages/options that are not directly required by the final doctor-provided digital monitoring form and the PhD research scope.

The platform must stay focused only on the NEWS2 / HD2-mNEWS hemodialysis monitoring workflow, patient baseline context, session measurements, alerts, clinical response, 72-hour clinical outcome validation, research dataset, and research analytics.

Do not add new large features in this task. This task is strictly a scope-cleanup and navigation-hardening phase.

---

## Source of Truth
Use the doctor-provided form as the functional boundary:

- Patient baseline/context form
- Hemodialysis session context
- HD2-mNEWS variables
- Vital signs and dialysis-specific variables
- Risk levels: green, yellow, red
- Nursing protocol by risk color
- Clinical deterioration documentation
- Clinical outcome after 72 hours
- Prediction validation: whether the platform predicted deterioration
- Data verification sources

The system should not expose pages that are unrelated to this scope.

---

## Current Project Context
The project is a FastAPI + SQLAlchemy + PostgreSQL + Vanilla JavaScript + Arabic RTL single-page clinical research platform.

Already implemented phases include:

- Patients
- Dialysis sessions
- Measurements
- NEWS2 assessments
- Alerts
- Deterioration events
- Responses
- Response tracking
- Outcomes
- Research dataset/export
- Research analytics
- Study management
- RBAC
- Authentication
- User management
- Patient lifecycle

The current task is not to remove backend capabilities blindly. It is to simplify visible navigation and remove/disable unnecessary right-sidebar options and their linked frontend pages if they are outside the research form scope.

---

## Main Requirement
Review the right-side/sidebar navigation menu and remove every item that is not necessary for the doctor-approved research workflow.

Keep the platform clinically focused and easy for nurses/doctors/researchers to use.

---

## Navigation Items That Should Remain
Keep only the navigation items/pages that directly support the study workflow.

Recommended final visible navigation:

1. Dashboard / الرئيسية
   - High-level overview only.
   - Must remain simple and connected to the study workflow.

2. Patients / المرضى
   - Patient list.
   - Patient baseline/context data.
   - Patient profile.
   - Patient lifecycle actions only if already implemented and useful.

3. Sessions / جلسات الغسيل
   - Dialysis session date/time.
   - Actual session start time.
   - Weekly session count/context when applicable.
   - Fluid removal target / UFR-related context.

4. Digital Monitoring / المراقبة الرقمية
   - Measurement entry.
   - NEWS2 or HD2-mNEWS assessment display.
   - Risk color result.
   - Alert/protocol guidance.

5. Alerts / التنبيهات
   - Active alerts.
   - Acknowledge/start/close workflow if already implemented.
   - Must stay focused on clinical deterioration alerts.

6. Clinical Response / الاستجابة السريرية
   - Response logging.
   - Actions taken.
   - Doctor response time.

7. Clinical Outcome / النتيجة السريرية
   - Outcome after 72 hours.
   - Deterioration type.
   - Whether the platform predicted deterioration.
   - Intervention and result.
   - Verification source.

8. Research Dataset / بيانات البحث
   - Dataset generation.
   - CSV/XLSX/SPSS exports if already implemented.

9. Research Analytics / التحليل البحثي
   - Research KPIs.
   - Deterioration analytics.
   - Response-time analytics.
   - Prediction/validation analytics if currently present.

10. Study Management / إدارة الدراسة
   - Keep only if it is already useful for the PhD protocol and does not clutter the UI.
   - If it is too broad, rename/simplify it to Protocol / بروتوكول الدراسة.

11. User Management / إدارة المستخدمين
   - Visible only for admin / technical_admin.
   - Keep because authentication and RBAC already exist.

12. Logout / تسجيل الخروج

---

## Navigation Items To Remove or Hide
Remove or hide from the sidebar any item that is not directly tied to the form or research workflow.

Examples of items that should be removed if present:

- Generic hospital management pages.
- Complex operational workflow pages not required by the study.
- Any placeholder/demo pages.
- Any duplicate pages for the same workflow.
- Any pages related to advanced enterprise features not needed for this research phase.
- Any experimental pages not connected to the doctor form.
- Any broad administrative pages beyond user management.
- Any multi-center, shift, assignment, department, bed, or staff scheduling pages unless they are already required by the current research workflow.

Important: Do not delete critical backend code unless it is clearly only supporting a removed frontend page and has no test coverage dependency. Prefer hiding/removing navigation and cleaning associated frontend routing first.

---

## Required Implementation Steps

### Step 1 — Inspect Current Navigation
Find all files responsible for the right-side/sidebar menu.

Likely locations may include:

- `app/templates/base.html`
- `app/templates/*.html`
- `app/static/js/*.js`
- `app/static/css/style.css`
- Any SPA route registry or navigation renderer

Identify:

- All visible menu items.
- Their route IDs or URLs.
- Their permission checks.
- The frontend sections/pages they open.

---

### Step 2 — Define a Clean Navigation Registry
If the project already has a navigation registry, update it.

If navigation is hardcoded, refactor minimally and safely so the visible menu becomes easy to maintain.

Each navigation item should have:

- Arabic label
- Route/section target
- Required permission/role when needed
- Clear relationship to the study workflow

Do not introduce over-engineering.

---

### Step 3 — Remove Unnecessary Sidebar Items
Remove/hide all sidebar entries outside the allowed scope.

The sidebar should become short, clinical, and research-oriented.

The user should not see pages that make the system look broader than the PhD study.

---

### Step 4 — Remove or Disable Linked Frontend Pages
For every removed navigation item:

- Remove its SPA route button/link.
- Remove dead click handlers if they are now unused.
- Remove unused empty frontend sections if safe.
- If the backend endpoint is still used by tests or future planned features, leave it intact but inaccessible from navigation.

Avoid breaking current tests.

---

### Step 5 — Preserve RBAC
Do not weaken authentication or RBAC.

Admin-only pages must remain admin-only.

Clinical pages must remain available only to the intended roles.

Do not re-enable frontend role switching.

Do not expose hidden/admin pages to unauthorized users.

---

### Step 6 — Improve Arabic Labels
Make labels concise and aligned with the research scope.

Recommended labels:

- الرئيسية
- المرضى
- جلسات الغسيل
- المراقبة الرقمية
- التنبيهات
- الاستجابة السريرية
- النتيجة السريرية
- بيانات البحث
- التحليل البحثي
- بروتوكول الدراسة
- إدارة المستخدمين
- تسجيل الخروج

Use these labels unless the existing app has better consistent Arabic wording.

---

### Step 7 — Remove Visual Clutter
Make the sidebar cleaner:

- Keep grouping only if it improves clarity.
- Avoid too many nested groups.
- Preserve existing RTL and Dark/medical visual identity.
- Do not redesign the whole UI.
- Do not break mobile drawer/collapse behavior.

---

### Step 8 — Add Regression Tests Where Practical
If the project already has frontend/backend tests for navigation, update them.

If not, add lightweight backend/template tests only if the existing test structure supports it.

At minimum, ensure existing tests still pass.

---

## Strict Non-Goals
Do not implement the HD2-mNEWS scoring engine in this task.

Do not add the 72-hour clinical outcome form in this task unless it already exists and only needs menu cleanup.

Do not change NEWS2 formulas in this task.

Do not change patient lifecycle logic.

Do not change authentication/session logic.

Do not change database schema unless absolutely necessary for removing dead frontend-only pages, which is unlikely.

Do not remove research exports.

Do not remove audit logs from backend if they are used by security/compliance; if there is a visible sidebar item for audit logs and it feels too technical, hide it from normal clinical users and keep it admin-only or accessible through admin tools only.

---

## Expected Output
After implementation:

1. The right sidebar should show only study-relevant options.
2. Removed options should not open dead/empty pages.
3. The application should still run normally.
4. Existing clinical/research workflows should remain intact.
5. Mobile sidebar/drawer behavior should remain stable.
6. RBAC visibility should remain correct.
7. Tests should pass.

---

## Files To Inspect Carefully
Inspect and update as needed:

- `app/templates/base.html`
- `app/templates/index.html` or main SPA template if present
- `app/static/js/*.js`
- `app/static/css/style.css`
- `app/routes/*.py` only if frontend route/page cleanup requires it
- `tests/*` if navigation expectations exist

Do not modify unrelated files.

---

## Validation Commands
Run these commands before finishing:

```bash
python -m compileall app
pytest
```

If JavaScript files are changed, also run Node syntax checks on the changed JS files, for example:

```bash
node --check app/static/js/main.js
```

Use the actual changed JS filenames.

Also run:

```bash
git diff --check
```

---

## Final Response Requirements
When finished, provide:

1. Summary of removed sidebar items.
2. Summary of remaining sidebar items.
3. Files changed.
4. Tests/validation results.
5. Any intentionally preserved backend routes that were hidden from navigation.
6. Final GitHub commands:

```bash
git add .
git commit -m "Simplify navigation around research monitoring scope"
git push origin main
```
