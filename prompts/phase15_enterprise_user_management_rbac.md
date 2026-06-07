# PHASE 15 — ENTERPRISE USER MANAGEMENT & RBAC HARDENING

## Objective

Implement Enterprise User Management and RBAC hardening for the NEWS2 Hemodialysis Monitoring Platform.

This phase must allow the system administrator to add staff users, define their job/role, activate/deactivate them, and control which navigation sections and API actions are visible/allowed according to role permissions.

This phase must also add a new technical role:

```text
technical_admin
```

Arabic label:

```text
تقني النظام
```

The Administration navigation group must be visible only to:

```text
admin
technical_admin
```

This phase is still not full production authentication yet. It is an enterprise user management and RBAC visibility/hardening phase that prepares the platform for Phase 16 Authentication & Security.

---

# CURRENT PROJECT STATE

The platform currently supports:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- PostgreSQL on Render/Neon
- Startup database initialization
- Patient/session/monitoring workflows
- NEWS2 engine
- Alert engine
- Deterioration workflow
- Response workflow
- Response time tracking
- Clinical outcomes
- Research export center
- Research analytics dashboard
- Study management
- RBAC foundation
- Dev role switcher using `X-Dev-Role`
- Grouped sidebar navigation

Current roles:

```text
admin
doctor
on_call_doctor
nurse
researcher
```

Phase 15 must add:

```text
technical_admin
```

and implement real staff management screens/APIs.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the full UI.

Do not break current deployment on Render.

Do not break Neon/PostgreSQL startup initialization.

Do not break patient creation or patient profile selector.

Do not break existing clinical workflows.

Do not remove current RBAC behavior.

Do not implement full login/password authentication yet unless minimal password fields already exist safely.

Do not introduce JWT/session logic in this phase.

Full authentication belongs to Phase 16.

---

# PHASE BOUNDARY

This phase must do:

```text
Add technical_admin role
↓
Add employee/staff user management
↓
Allow admin to create staff users
↓
Assign role/job/department/status
↓
Control Administration menu visibility
↓
Protect user-management APIs
↓
Expose role/permission matrix cleanly
```

This phase must NOT do:

```text
JWT authentication
Session cookies
Password reset email
MFA
Full production login hardening
External identity provider
```

---

# ROLE MODEL UPDATE

Update centralized RBAC in:

```text
app/rbac.py
```

Add role:

```text
technical_admin
```

Arabic label:

```text
تقني النظام
```

---

# TECHNICAL ADMIN PERMISSIONS

Technical Admin should manage technical/admin configuration but not clinical decisions.

Allowed:

```text
users:view
users:create
users:update
users:manage
rbac:view
rbac:manage
audit:view
settings:view
settings:manage
```

Also allow basic read-only platform visibility if needed:

```text
patients:view
sessions:view
alerts:view
research:view
```

Not allowed by default:

```text
patients:create
measurements:create
alerts:manage
deterioration:create
responses:create
outcomes:create
research:export
studies:update
```

Admin still has all permissions.

---

# NEW PERMISSIONS

Add missing permissions if not already present:

```text
users:create
users:update
users:disable
rbac:view
rbac:manage
staff:view
staff:create
staff:update
```

You can map staff permissions to users permissions internally if preferred.

---

# ADMINISTRATION NAVIGATION VISIBILITY

The Administration navigation group currently includes:

```text
المستخدمون
الأدوار
الصلاحيات
سجلات التدقيق
إعدادات النظام
إعدادات اللغة
```

This whole group must be visible only when the current role has at least one of:

```text
users:view
users:manage
rbac:view
rbac:manage
audit:view
settings:view
settings:manage
```

Practically this means:

- admin sees الإدارة
- technical_admin sees الإدارة
- doctor does not see الإدارة
- on_call_doctor does not see الإدارة
- nurse does not see الإدارة
- researcher should not see الإدارة unless explicitly allowed

If researcher currently has audit:view from previous phase, decide whether to:
- remove audit:view from researcher, or
- keep audit:view but do not show full الإدارة group; show audit under research only if needed.

Preferred for this phase:

```text
Researcher should NOT see the Administration group.
```

---

# STAFF / USER MANAGEMENT MODEL

Use existing `users` table/model if it already exists.

Required fields for staff management:

```text
id
full_name
username
email
phone
department
job_title
role
is_active
temporary_password_hash or password_hash
created_at
updated_at
```

If existing model has fewer fields, add missing fields safely and non-destructively.

Do not drop existing columns.

If password_hash exists, use it.

If no password system exists yet, store a temporary password hash safely for Phase 16, but do not enable login yet unless already supported.

---

# PASSWORD HANDLING FOR THIS PHASE

Because Phase 16 will implement real authentication, Phase 15 should:

- accept a temporary password field when creating staff
- hash it using a safe standard library method or existing hashing helper
- never store plain text password
- never return password or password_hash in API responses

If no hashing utility exists, create:

```text
app/security/passwords.py
```

Use a safe approach. Prefer `passlib` only if dependency already exists. If not, use `hashlib.pbkdf2_hmac` with salt from `secrets.token_bytes`.

Do not add heavy dependencies unless necessary.

---

# BACKEND SERVICE

Create or update:

```text
app/services/user_management_service.py
```

Recommended functions:

```python
create_staff_user(db, payload)
update_staff_user(db, user_id, payload)
list_staff_users(db, filters)
get_staff_user(db, user_id)
set_staff_user_active_status(db, user_id, is_active)
```

Responsibilities:

- Validate role exists.
- Validate username/email uniqueness.
- Hash temporary password.
- Never return password hash.
- Create audit logs.
- Commit/rollback safely.
- Return clean staff user response.

---

# PYDANTIC SCHEMAS

Update:

```text
app/schemas.py
```

Add:

```text
StaffUserCreate
StaffUserUpdate
StaffUserRead
StaffUserStatusUpdate
StaffUserCreateResult
```

Create fields:

```text
full_name
username
email
phone
department
job_title
role
temporary_password
is_active
```

Validation:

- full_name required
- username required
- role required
- role must be valid
- temporary_password required for create
- email optional but if provided must be valid
- is_active default true

Response must exclude:

```text
password
password_hash
temporary_password
```

---

# API ENDPOINTS

Create or update:

```text
app/routers/users.py
```

Required endpoints:

## List Staff Users

```text
GET /api/users
```

Requires:

```text
users:view
```

Support filters:

```text
role
is_active
department
search
```

---

## Create Staff User

```text
POST /api/users
```

Requires:

```text
users:create
```

Returns created staff user.

---

## Get Staff User

```text
GET /api/users/{id}
```

Requires:

```text
users:view
```

---

## Update Staff User

```text
PUT /api/users/{id}
```

Requires:

```text
users:update
```

Allows updating:

```text
full_name
email
phone
department
job_title
role
is_active
```

---

## Activate / Deactivate User

```text
POST /api/users/{id}/status
```

Requires:

```text
users:disable
```

Payload:

```json
{
  "is_active": false
}
```

---

# FRONTEND USER MANAGEMENT

Update:

```text
app/static/app.js
```

Implement real screens:

```text
المستخدمون
إضافة موظف
الأدوار
الصلاحيات
```

---

# USERS LIST UI

Arabic title:

```text
إدارة المستخدمين
```

Display table/cards:

```text
الاسم الكامل
اسم المستخدم
البريد الإلكتروني
القسم
الوظيفة
الدور
الحالة
إجراءات
```

Actions:

```text
تعديل
تفعيل / إيقاف
```

Only visible for admin/technical_admin according to permissions.

---

# ADD STAFF FORM UI

Arabic title:

```text
إضافة موظف
```

Fields:

```text
الاسم الكامل
اسم المستخدم
البريد الإلكتروني
رقم الهاتف
القسم
الوظيفة / المهمة
الدور
كلمة مرور مؤقتة
الحالة
```

Role dropdown:

```text
مدير النظام
تقني النظام
طبيب
طبيب مناوب
ممرض/ممرضة
باحث
```

Job examples:

```text
طبيب كلى
طبيب مناوب
ممرض غسيل
باحث سريري
تقني نظام
مدير منصة
```

Submit button:

```text
حفظ الموظف
```

Success:

```text
تم إنشاء الموظف بنجاح
```

Duplicate username/email:

```text
اسم المستخدم أو البريد الإلكتروني مستخدم مسبقاً
```

---

# ROLE PERMISSION MATRIX UI

Improve roles/permissions screen.

Show:

- role name
- Arabic label
- permission groups
- allowed permissions

Make it read-only for now unless `rbac:manage` exists and implementation is simple.

No need to allow editing permission matrix from UI yet.

---

# FRONTEND PERMISSION FILTERING

Update navigation:

- Administration group hidden unless allowed role/permission.
- Users screen hidden unless `users:view`.
- Roles/Permissions hidden unless `rbac:view`.
- Audit Logs hidden unless `audit:view`.
- Settings hidden unless `settings:view`.

Do not rely only on UI hiding; backend endpoints must also enforce permissions.

---

# DEV ROLE SWITCHER UPDATE

Add:

```text
technical_admin
```

to the dev role switcher.

Arabic display:

```text
تقني النظام
```

Test:

- selecting technical_admin should show الإدارة
- selecting doctor should hide الإدارة
- selecting nurse should hide الإدارة
- selecting researcher should hide الإدارة

---

# AUDIT LOGS

Create audit logs for:

```text
staff_user_created
staff_user_updated
staff_user_status_changed
permission_denied
```

Use existing audit infrastructure.

---

# TESTS

Create:

```text
tests/test_user_management_rbac.py
```

Required tests:

1. technical_admin role exists.
2. technical_admin has users/manage/settings permissions.
3. technical_admin cannot create clinical response.
4. admin can create staff user.
5. technical_admin can create staff user if allowed.
6. nurse cannot create staff user.
7. doctor cannot access /api/users.
8. created staff user does not expose password hash.
9. duplicate username returns conflict.
10. invalid role returns 422 or 400.
11. deactivate user endpoint works.
12. /api/rbac/me supports technical_admin.
13. Administration navigation data is permission-compatible if testable.

Update existing RBAC tests if role matrix changes.

---

# DOCUMENTATION

Create:

```text
docs/user_management.md
```

Update:

```text
docs/rbac.md
docs/system_architecture.md
README.md
```

Document:

- role matrix
- technical_admin role
- staff creation workflow
- temporary password limitation
- Phase 16 authentication dependency
- security warning that Phase 15 is not full login security

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual validation:

1. Open app as admin.
2. Administration group is visible.
3. Open users screen.
4. Add staff user.
5. Confirm user appears in list.
6. Switch dev role to technical_admin.
7. Administration group remains visible.
8. Switch dev role to doctor.
9. Administration group disappears.
10. Switch dev role to nurse.
11. Administration group disappears.
12. Try direct `/api/users` as nurse using header; confirm 403.
13. Verify no password hash is returned.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Add enterprise user management and technical admin role"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Role/RBAC updates
4. Staff user management backend
5. Add employee frontend workflow
6. Administration menu visibility behavior
7. Password handling behavior
8. Tests added or updated
9. Validation results
10. Security limitations
11. Deployment commands
12. Risks

---

# NEXT PHASE

After this phase:

```text
Phase 16 — Authentication & Security
```

Phase 16 must replace the temporary dev-role behavior with:

```text
real login
session/JWT
current authenticated user
secure password verification
logout
route protection
```
