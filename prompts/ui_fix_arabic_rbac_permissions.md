# UI FIX — DISPLAY RBAC PERMISSIONS IN ARABIC

## Objective

Improve the Roles / Permissions screen so permission groups and permissions are displayed in professional Arabic instead of raw technical labels like:

```text
alerts (2), audit (1), deterioration (2), measurements (2)
```

The current technical labels are useful for developers but not suitable for doctors, admins, or hospital staff.

---

# CURRENT PROBLEM

The Roles screen currently displays permission summaries using raw backend permission resource names:

```text
alerts (2), audit (1), deterioration (2), measurements (2), news2 (1), outcomes (2), patients (3), rbac (2), research (3), responses (2), sessions (3), settings (2), staff (3), studies (3), users (5)
```

This must be translated to Arabic and made readable.

---

# CRITICAL RULES

Do not change the actual backend permission keys.
Do not change RBAC authorization logic.
Do not change API permission names.
Do not break `/api/rbac/permissions`.
Do not break tests.

This is a UI/display translation improvement only unless adding a backend label map is cleaner.

---

# REQUIRED BEHAVIOR

In the Roles / Permissions UI:

Instead of:

```text
alerts (2)
```

show:

```text
التنبيهات: عرض، إدارة
```

Instead of:

```text
patients (3)
```

show:

```text
المرضى: عرض، إضافة، تعديل
```

Instead of:

```text
users (5)
```

show:

```text
المستخدمون: عرض، إضافة، تعديل، إدارة، إيقاف
```

---

# ARABIC PERMISSION RESOURCE LABELS

Add frontend mapping:

```javascript
const PERMISSION_RESOURCE_LABELS = {
  patients: "المرضى",
  sessions: "جلسات الغسيل",
  measurements: "العلامات الحيوية",
  news2: "تقييم NEWS2",
  alerts: "التنبيهات",
  deterioration: "أحداث التدهور",
  responses: "الاستجابات",
  outcomes: "المآلات السريرية",
  research: "البحث",
  studies: "الدراسة",
  users: "المستخدمون",
  staff: "الموظفون",
  rbac: "الأدوار والصلاحيات",
  audit: "سجلات التدقيق",
  settings: "الإعدادات"
}
```

---

# ARABIC ACTION LABELS

Add frontend mapping:

```javascript
const PERMISSION_ACTION_LABELS = {
  view: "عرض",
  create: "إضافة",
  update: "تعديل",
  manage: "إدارة",
  disable: "إيقاف",
  analytics: "تحليلات",
  export: "تصدير"
}
```

If unknown action appears, convert it safely:

- replace `_` with spaces
- keep readable fallback

---

# DISPLAY FORMAT

For each role, display permission groups as clean Arabic chips or lines.

Preferred format:

```text
التنبيهات: عرض، إدارة
المرضى: عرض، إضافة، تعديل
البحث: عرض، تحليلات، تصدير
```

Use badges/chips if already consistent with UI.

Avoid long unwrapped English text.

---

# OPTIONAL DETAILS VIEW

If the table becomes too wide, use:

- Summary count in table
- Button:

```text
عرض الصلاحيات
```

Opening an expandable details section/card with Arabic permission groups.

But the minimum required fix is to translate the current displayed permission groups.

---

# ROLE LABELS

Ensure role labels remain Arabic:

```text
admin => مدير النظام
technical_admin => تقني النظام
doctor => طبيب
on_call_doctor => طبيب مناوب
nurse => ممرض/ممرضة
researcher => باحث
```

---

# UI QUALITY

The permission column should be readable.

Requirements:

- Arabic RTL display.
- No raw English resource names visible in the main roles table.
- No raw `alerts (2)` style text.
- Preserve permission count if useful.
- Keep responsive behavior.

---

# FILES TO MODIFY

Likely:

```text
app/static/app.js
app/static/styles.css
```

Backend changes are not required unless already centralizing label metadata in `/api/rbac/permissions`.

---

# VALIDATION

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual validation:

1. Open Roles screen.
2. Confirm permission groups are Arabic.
3. Confirm no `alerts (2)` raw English text appears.
4. Confirm admin row shows readable full permissions.
5. Confirm technical admin permissions are readable.
6. Confirm doctor/nurse/researcher rows remain aligned.
7. Confirm no console errors.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Display RBAC permissions in Arabic"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Arabic permission label mapping
4. UI display changes
5. Validation results
6. Deployment commands
7. Risks
