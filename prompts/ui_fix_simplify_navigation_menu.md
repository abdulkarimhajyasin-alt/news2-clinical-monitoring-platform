# UI FIX — SIMPLIFY NAVIGATION AND ADD COLLAPSIBLE MENU

## Objective

Improve the Arabic RTL navigation experience for the NEWS2 Hemodialysis Monitoring Platform.

The current sidebar contains too many visible navigation items, causing poor usability and excessive scrolling. The goal is to simplify the sidebar, move secondary screens into grouped sections, and add a top-right menu button that opens/closes the navigation cleanly.

This is a UX/navigation improvement only. Do not change backend workflows or database logic.

---

# CURRENT PROBLEM

The current sidebar shows nearly every screen directly:

- Dashboard
- Patients
- Sessions
- Measurements
- NEWS2
- Alerts
- Deterioration
- Responses
- Response Time
- Outcomes
- Research
- Export Center
- Study Management
- RBAC
- Audit Logs
- Settings
- Language Settings
- Many detail/history/timeline screens

This creates:

- Too much scrolling
- Repeated sections
- Confusing navigation
- Poor mobile/tablet experience
- Too many screens visible before they are needed

---

# CRITICAL RULES

## Preserve Existing Work

Do not remove routes.

Do not break hash routing.

Do not remove existing screens from the codebase.

Do not break API integration.

Do not redesign the whole visual identity.

Do not change backend logic.

Do not change database models.

Do not remove RBAC checks.

This is only a navigation and UX cleanup.

---

# REQUIRED UX CHANGE

## 1. Add Top-Right Menu Button

Add a clear menu button at the top-right of the page.

Arabic label/icon:

```text
☰
```

or a professional menu icon.

Behavior:

- On desktop: toggles sidebar collapsed/expanded.
- On tablet/mobile: opens sidebar as an overlay drawer.
- Clicking outside drawer closes it on mobile.
- ESC key closes it if open.
- The main content should expand when sidebar is collapsed.

The button should be visible and easy to access in RTL layout.

---

## 2. Simplify Visible Sidebar Items

Keep only the primary operational screens directly visible.

Recommended main sidebar structure:

```text
لوحة التحكم
المرضى
جلسات الغسيل
إدخال العلامات الحيوية
التنبيهات النشطة
أحداث التدهور
الاستجابة السريرية
زمن الاستجابة
المآلات السريرية
التحليلات البحثية
مركز التصدير
إدارة الدراسة
الإدارة
```

---

## 3. Move Secondary Screens Into Submenus

Use collapsible groups.

### المرضى

Visible parent:

```text
المرضى
```

Sub-items:

```text
قائمة المرضى
إضافة مريض
ملف المريض
الخط الأساسي
الوصول الوعائي
```

Only show sub-items when group is expanded.

---

### الجلسات

Sub-items:

```text
جلسات الغسيل
إنشاء جلسة
تفاصيل الجلسة
الرصد أثناء الجلسة
```

---

### التقييم

Sub-items:

```text
إدخال العلامات الحيوية
تقييم NEWS2
اتجاه NEWS2
سجل NEWS2
```

---

### التنبيهات

Sub-items:

```text
التنبيهات النشطة
تفاصيل التنبيه
تسلسل التنبيه
```

---

### الأحداث والاستجابة

Sub-items:

```text
أحداث التدهور
تفاصيل الحدث
تسلسل الحدث
سجل الاستجابة الطبية
سجل الاستجابة التمريضية
مسار الاستجابة
زمن الاستجابة
تحليلات الاستجابة
```

---

### المخرجات

Sub-items:

```text
المآلات السريرية
تتبع المآلات
تحليلات المآلات
```

---

### البحث

Sub-items:

```text
لوحة البحث
مقارنة قبل وبعد
مؤشرات الدراسة
إحصاءات البيانات
مركز التصدير
إدارة الدراسة
بروتوكول البحث
الخط الزمني للدراسة
جاهزية الدراسة
```

---

### الإدارة

Sub-items:

```text
المستخدمون
الأدوار
الصلاحيات
سجلات التدقيق
إعدادات النظام
إعدادات اللغة
```

---

# IMPORTANT ROUTE VISIBILITY RULE

Do not show detail-only screens as main items.

These should NOT be top-level visible items:

```text
ملف المريض
تفاصيل الجلسة
تفاصيل التنبيه
تسلسل التنبيه
تفاصيل الحدث
تسلسل الحدث
بروتوكول البحث
الخط الزمني للدراسة
جاهزية الدراسة
إعدادات اللغة
```

They should be accessible through:

- submenus
- buttons/actions inside related screens
- direct route if needed

---

# MOBILE BEHAVIOR

On narrow screens:

- Sidebar should be hidden by default.
- Menu button opens sidebar overlay.
- Overlay should cover main content with a dim background.
- Close button should appear inside sidebar.
- Body should not horizontally overflow.
- Sidebar should scroll internally if needed.

---

# DESKTOP BEHAVIOR

On desktop:

- Sidebar can remain visible by default.
- Menu button collapses it to icon-only mode or hides it.
- Main content should use available width.
- Current active route should remain highlighted.

---

# VISUAL STYLE

Preserve current medical identity:

- Dark blue sidebar
- Arabic RTL typography
- Soft rounded items
- Medical enterprise dashboard style
- Existing color palette

Improve spacing:

- Reduce vertical padding between menu items.
- Make section titles smaller and clearer.
- Avoid giant sidebar height due to all routes being exposed.

---

# FRONTEND FILES

Update:

```text
app/static/app.js
app/static/styles.css
```

If needed:

```text
app/static/index.html
```

---

# IMPLEMENTATION REQUIREMENTS

## Navigation Data Structure

Refactor navigation into grouped structure:

```javascript
const NAV_GROUPS = [...]
```

Each group should include:

```javascript
{
  label: "...",
  icon: "...",
  route: "... optional",
  permission: "... optional",
  children: [...]
}
```

Respect existing RBAC permission filtering.

If a user lacks permission for a group and all its children, hide the group.

---

## Active State

When current route is a child route:

- Expand parent group automatically.
- Highlight child route.
- Also visually mark parent as active.

---

## Menu Persistence

Store sidebar collapsed/expanded state in:

```text
localStorage
```

Optional but preferred.

---

## Accessibility

Add:

- aria-label for menu button
- aria-expanded
- aria-controls
- keyboard close behavior
- focus-safe behavior if simple

---

# TESTS / VALIDATION

No backend tests required unless route constants are affected.

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual validation:

1. Open app on desktop.
2. Click menu button.
3. Sidebar collapses/opens.
4. Active route remains highlighted.
5. Open patient group.
6. Click Add Patient.
7. Open research group.
8. Click Export Center.
9. Resize browser to mobile width.
10. Sidebar becomes drawer.
11. Click outside drawer closes it.
12. No horizontal overflow.
13. RBAC dev role still hides disabled actions correctly.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Simplify navigation and add collapsible menu"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Navigation structure changes
4. Sidebar/menu behavior
5. Mobile behavior
6. RBAC compatibility
7. Validation results
8. Deployment commands
9. Risks
