# UI FIX — MAKE DASHBOARD HIGH-RISK ALERT CARD NAVIGATE TO FILTERED ALERTS

## Objective

Fix the dashboard high-risk alert card so clicking it navigates the user to the relevant high-risk/active alerts screen instead of doing nothing.

The user expects the card showing:

```text
تنبيهات عالية الخطورة
```

to behave as an actionable shortcut.

---

# CURRENT PROBLEM

On the dashboard, the KPI card:

```text
تنبيهات عالية الخطورة
1
من بيانات التنبيهات
```

is visually shown but not clickable, or clicking it does not navigate to the dangerous/high-risk alert state.

Expected behavior:

- Clicking the high-risk alert card opens the Active Alerts screen.
- The Active Alerts screen should be filtered to high-risk/urgent/active alerts when possible.
- The user should clearly see the risky alert(s) related to that KPI.

---

# CRITICAL RULES

Do not redesign the dashboard.

Do not break existing dashboard cards.

Do not break active alerts screen.

Do not change backend database logic.

Do not change alert creation logic.

Do not change RBAC logic.

This is a frontend navigation/actionability fix, with minimal backend only if already supported filters are missing.

---

# REQUIRED FRONTEND BEHAVIOR

## Dashboard Card Click

The high-risk alert card must be clickable.

Add:

- pointer cursor
- hover state
- accessible button/card role
- click handler

Click should navigate to:

```text
#/active-alerts?risk_level=high
```

or the actual existing active alerts route with equivalent query params.

If route naming differs, use current route key for:

```text
التنبيهات النشطة
```

---

# FILTER BEHAVIOR

When Active Alerts screen loads with query/filter:

```text
risk_level=high
```

or:

```text
severity_level=high
```

or:

```text
priority=urgent
```

it should display only relevant dangerous alerts.

Prefer filtering by:

```text
risk_level=high
```

and include:

```text
severity_level=high
priority=urgent
status in new/viewed/acknowledged/in_progress
```

If current backend `/api/alerts` supports query filters, use it.

If not, fetch alerts and filter client-side safely.

---

# CLICKABLE DASHBOARD CARDS

Make these dashboard KPI cards actionable too if simple:

```text
إجمالي المرضى        => #/patients
التنبيهات النشطة     => #/active-alerts
تنبيهات عالية الخطورة => #/active-alerts?risk_level=high
أحداث التدهور        => #/deterioration-events
الاستجابات المسجلة   => #/medical-response-log
المآلات              => #/clinical-outcomes
```

Do not overbuild. Main required fix is high-risk alerts.

---

# UI LABELING

On filtered Active Alerts screen, show a small filter badge:

```text
عرض التنبيهات عالية الخطورة
```

Add clear reset link/button:

```text
عرض كل التنبيهات
```

---

# EMPTY STATE

If no high-risk alerts exist:

```text
لا توجد تنبيهات عالية الخطورة حالياً
```

Do not show a generic empty message only.

---

# ACCESSIBILITY

For clickable KPI cards:

- Use `role="button"` or actual button/link semantics.
- Add `tabindex="0"` if needed.
- Support Enter key activation if implemented easily.
- Add `aria-label` in Arabic.

---

# FILES TO MODIFY

Likely:

```text
app/static/app.js
app/static/styles.css
```

No backend changes unless absolutely necessary.

---

# VALIDATION

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual validation:

1. Open Dashboard.
2. Click `تنبيهات عالية الخطورة`.
3. App navigates to Active Alerts.
4. Active Alerts shows only high-risk/urgent alert(s).
5. Filter badge appears.
6. Click `عرض كل التنبيهات`.
7. Full alert list returns.
8. Click `إجمالي المرضى`.
9. App navigates to Patient List if implemented.
10. No console errors.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Make dashboard alert cards navigate to filtered alerts"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Dashboard clickable card behavior
4. Active Alerts filter behavior
5. Accessibility improvements
6. Validation results
7. Deployment commands
8. Risks
