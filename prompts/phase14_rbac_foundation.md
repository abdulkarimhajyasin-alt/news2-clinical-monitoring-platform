# PHASE 14 — ROLE BASED ACCESS CONTROL (RBAC)

## Objective

Implement the Role Based Access Control (RBAC) foundation for the NEWS2 Hemodialysis Monitoring Platform.

This phase must define, enforce, document, and expose a professional permission system for the platform roles without yet implementing full authentication.

The goal is to prepare the platform for secure clinical/research operation by centralizing role permissions and protecting sensitive actions such as exports, study management, audit logs, and administrative controls.

This phase must be additive, safe, and compatible with the current development mode.

---

# CURRENT PROJECT STATE

The platform currently supports:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready configuration
- Patient/session/monitoring workflow
- NEWS2 calculation engine
- Alert creation engine
- Deterioration workflow
- Medical/nursing response workflow
- Response tracking engine
- Clinical outcomes workflow
- Research dataset/export center
- Research analytics dashboard
- Study management/research protocol center
- Audit logs
- Seeded users with roles

Current user roles already expected in the platform:

```text
admin
doctor
on_call_doctor
nurse
researcher
```

Phase 14 must formalize permissions for these roles.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI identity.

Do not break existing clinical workflows.

Do not break exports.

Do not break analytics.

Do not implement full password login yet.

Do not implement session/cookie authentication yet.

Do not implement JWT yet.

Do not remove the current development/demo access behavior unless safely replaced.

---

# PHASE BOUNDARY

This phase must do:

```text
Define roles
↓
Define permissions
↓
Create permission matrix
↓
Create backend permission utilities
↓
Apply protection to sensitive endpoints
↓
Expose frontend permission state
↓
Hide/disable restricted UI actions
```

This phase must NOT do:

```text
Full authentication
Password login
JWT
Session management
Password reset
Email verification
Production security hardening
```

Those belong to Phase 15.

---

# RBAC DESIGN PRINCIPLES

Use a centralized permission model.

Do not scatter permission checks randomly.

All role permissions should be defined in one clear place.

Recommended file:

```text
app/rbac.py
```

or:

```text
app/security/rbac.py
```

Keep it simple and production-ready.

---

# ROLES

Support exactly these roles for now:

```text
admin
doctor
on_call_doctor
nurse
researcher
```

Arabic labels:

```text
admin          => مدير النظام
doctor         => طبيب
on_call_doctor => طبيب مناوب
nurse          => ممرض/ممرضة
researcher     => باحث
```

---

# PERMISSION CATEGORIES

Implement permissions as stable string constants.

Recommended format:

```text
resource:action
```

Examples:

```text
patients:view
patients:create
patients:update

sessions:view
sessions:create
sessions:update

measurements:view
measurements:create

news2:view
alerts:view
alerts:manage

deterioration:view
deterioration:create

responses:view
responses:create

outcomes:view
outcomes:create

research:view
research:analytics
research:export

studies:view
studies:create
studies:update

users:view
users:manage

audit:view
settings:view
settings:manage
```

---

# ROLE PERMISSION MATRIX

Implement this baseline matrix.

## admin

Full access to all permissions.

---

## doctor

Allowed:

```text
patients:view
patients:create
patients:update
sessions:view
sessions:create
sessions:update
measurements:view
measurements:create
news2:view
alerts:view
alerts:manage
deterioration:view
deterioration:create
responses:view
responses:create
outcomes:view
outcomes:create
research:view
research:analytics
studies:view
audit:view
```

Not allowed:

```text
users:manage
settings:manage
research:export
```

Research export remains admin/researcher only.

---

## on_call_doctor

Allowed:

```text
patients:view
sessions:view
measurements:view
measurements:create
news2:view
alerts:view
alerts:manage
deterioration:view
deterioration:create
responses:view
responses:create
outcomes:view
outcomes:create
research:view
```

Not allowed:

```text
research:export
studies:update
users:manage
settings:manage
audit:view
```

---

## nurse

Allowed:

```text
patients:view
sessions:view
measurements:view
measurements:create
news2:view
alerts:view
deterioration:view
responses:view
responses:create
outcomes:view
```

Not allowed:

```text
alerts:manage
deterioration:create
outcomes:create
research:export
studies:update
users:manage
audit:view
settings:manage
```

---

## researcher

Allowed:

```text
patients:view
sessions:view
measurements:view
news2:view
alerts:view
deterioration:view
responses:view
outcomes:view
research:view
research:analytics
research:export
studies:view
studies:create
studies:update
audit:view
```

Not allowed:

```text
measurements:create
alerts:manage
deterioration:create
responses:create
outcomes:create
users:manage
settings:manage
```

---

# DEVELOPMENT USER CONTEXT

Because full authentication is not implemented yet, create a safe development user resolver.

Recommended behavior:

- Read role from request header:

```text
X-Dev-Role
```

- Default to:

```text
admin
```

only in local/dev mode.

- Validate role is one of allowed roles.
- Document clearly that this is temporary until Phase 15 authentication.

Do not expose this as production security.

---

# BACKEND PERMISSION UTILITIES

Create dependencies/helpers:

```python
get_current_dev_user()
require_permission(permission)
require_any_permission(permissions)
role_has_permission(role, permission)
```

Expected usage:

```python
@router.get(...)
def endpoint(..., current_user=Depends(require_permission("research:export"))):
    ...
```

The helper should raise:

```text
403 Forbidden
```

when role lacks permission.

---

# PROTECT SENSITIVE ENDPOINTS

Apply permission checks to the most important endpoints.

## Research Exports

Require:

```text
research:export
```

For:

```text
GET /api/research/export/csv
GET /api/research/export/xlsx
GET /api/research/export/spss-codebook
GET /api/research/export/spss-variable-labels
```

---

## Research Dataset Preview / Quality

Require:

```text
research:view
```

---

## Research Analytics

Require:

```text
research:analytics
```

---

## Study Management

Require:

```text
studies:view
studies:create
studies:update
```

According to endpoint.

---

## Audit Logs

If audit endpoint exists:

Require:

```text
audit:view
```

If no audit endpoint exists yet, prepare permission but do not create large new audit module unless simple.

---

## User Management / Settings

If endpoints exist:

Require:

```text
users:manage
settings:manage
```

If endpoints do not exist, only prepare permission constants.

---

## Clinical Write Actions

Protect:

```text
POST /api/monitoring/measurements       => measurements:create
POST /api/deterioration/events          => deterioration:create
POST /api/responses                     => responses:create
POST /api/outcomes                      => outcomes:create
POST /api/alerts/{id}/acknowledge       => alerts:manage
POST /api/alerts/{id}/start             => alerts:manage
POST /api/alerts/{id}/close             => alerts:manage
```

---

# RBAC API ENDPOINTS

Create:

```text
app/routers/rbac.py
```

Required endpoints:

## Current Permission Context

```text
GET /api/rbac/me
```

Returns:

```json
{
  "role": "admin",
  "role_label": "مدير النظام",
  "permissions": ["..."],
  "is_dev_context": true
}
```

---

## Permission Matrix

```text
GET /api/rbac/permissions
```

Returns roles, labels, and permissions.

This is useful for UI and documentation.

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Add frontend permission awareness.

Fetch:

```text
GET /api/rbac/me
```

On app load.

Store:

```text
appState.currentRole
appState.permissions
```

Add helper:

```javascript
hasPermission("research:export")
```

---

# UI BEHAVIOR

Do not break navigation.

For restricted actions:

- Hide or disable sensitive buttons.
- Show Arabic tooltip/message if visible but disabled.

Examples:

If role lacks export permission:

```text
ليست لديك صلاحية تصدير البيانات البحثية
```

If role lacks study update permission:

```text
ليست لديك صلاحية تعديل إعدادات الدراسة
```

---

# DEVELOPMENT ROLE SWITCHER

Add a small dev-only role switcher in the UI if safe.

Purpose:

- Test permissions before full auth.

It can set header behavior in frontend API client.

Suggested:

```text
Dev Role: Admin / Doctor / Nurse / Researcher
```

Arabic label:

```text
وضع الدور التجريبي
```

Do not make it prominent.

Document it as temporary.

---

# PERMISSION MATRIX UI

Create or improve:

```text
Roles
Permissions
```

Screens should display:

- Role list
- Arabic labels
- Permission groups
- Allowed/denied indicators

No write/edit matrix needed yet.

---

# AUDIT LOG

Add audit entries for permission denial if simple:

```text
permission_denied
```

Fields:

```text
role
permission
path
```

Do not overbuild.

---

# TESTS

Create:

```text
tests/test_rbac_permissions.py
```

Required tests:

1. Role permission matrix contains all roles.
2. Admin has all permissions.
3. Researcher can export.
4. Nurse cannot export.
5. Nurse cannot create deterioration event.
6. Doctor can create deterioration event.
7. On-call doctor can manage alerts.
8. Restricted export endpoint returns 403 for nurse.
9. Export endpoint succeeds for researcher/admin.
10. `/api/rbac/me` returns role and permissions.
11. Invalid `X-Dev-Role` returns safe error or fallback behavior.
12. Clinical write endpoint blocks unauthorized role.

---

# DOCUMENTATION

Create:

```text
docs/rbac.md
```

Must document:

- Roles
- Permission matrix
- Development header behavior
- Protected endpoints
- Frontend behavior
- Limitations before Phase 15 auth
- Security warning that this is not production authentication

Update:

```text
README.md
docs/system_architecture.md
docs/study_management.md
docs/research_export_center.md
```

Mention Phase 14 RBAC support.

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Manual validation:

```bash
uvicorn app.main:app --reload
```

Then verify:

1. `/api/rbac/me` returns permissions.
2. Export works as admin/researcher.
3. Export blocked as nurse.
4. Clinical write blocked for unauthorized role.
5. Frontend hides/disables export buttons for unauthorized roles.
6. Role switcher can simulate roles in dev.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. RBAC architecture
4. Permission matrix
5. Protected endpoints
6. Frontend updates
7. Dev role behavior
8. Tests added
9. Validation results
10. Security limitations
11. Risks / next phase recommendation
12. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase:

```text
Phase 15 — Authentication & Security
```

That phase will replace development role context with real authentication:

```text
Login
Password hashing
Session/JWT
Current user resolution
Secure role enforcement
```
