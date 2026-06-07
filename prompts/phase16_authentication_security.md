# PHASE 16 — AUTHENTICATION & SECURITY

## Objective

Implement real authentication and security for the NEWS2 Hemodialysis Monitoring Platform.

The current platform still uses a development role switcher and `X-Dev-Role`, which allows any user to simulate another role. This is acceptable for development only, but it is not secure for staging/production.

This phase must replace the development role selector with real login-based user identity, secure password verification, session handling, logout, current-user resolution, and RBAC enforcement based on the authenticated user's stored role.

---

# CURRENT PROBLEM

The UI currently shows a role dropdown:

```text
الدور: مدير / طبيب / ممرض / باحث / تقني النظام
```

Any user can change their role from the frontend.

The backend currently accepts:

```text
X-Dev-Role
```

This means any user can simulate:

```text
admin
technical_admin
doctor
nurse
researcher
```

This must be removed or disabled outside local development.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the full UI.

Do not break Render deployment.

Do not break Neon/PostgreSQL startup initialization.

Do not break RBAC permission matrix.

Do not break user management.

Do not break patient/session/monitoring workflows.

Do not break research exports/analytics.

Do not store plain-text passwords.

Do not expose password hashes through APIs.

---

# PHASE BOUNDARY

This phase must do:

```text
Login
↓
Password verification
↓
Session or secure token
↓
Current authenticated user
↓
RBAC from real user role
↓
Logout
↓
Remove public role switching
```

This phase must NOT do:

```text
MFA
Email password reset
External identity provider
SSO
Hospital LDAP integration
Advanced audit dashboards
```

Those can be later phases.

---

# AUTHENTICATION STRATEGY

Use a simple secure session-based authentication suitable for FastAPI.

Preferred approach:

- HTTP-only secure cookie session
- Server-side signed session token or secure random token
- Store token/session in database if needed
- Current user resolved from cookie

If this is too much for current architecture, use a secure signed cookie token with expiration.

Do not rely on localStorage for auth tokens.

---

# PASSWORD HANDLING

Use existing:

```text
app/security/passwords.py
```

from Phase 15 if available.

Required functions:

```python
hash_password(password)
verify_password(password, password_hash)
```

Password rules:

- Never store plain password.
- Never return password hash.
- Login must verify entered password against stored hash.
- Temporary passwords created in Phase 15 must work.

---

# USER MODEL REQUIREMENTS

Use existing `users` model/table.

Required fields:

```text
id
full_name
username
email
role
is_active
password_hash
created_at
updated_at
last_login_at
```

Add missing fields safely and non-destructively.

---

# SEED / INITIAL ADMIN

Ensure seed data creates a safe initial admin user if none exists.

Default development/staging admin:

```text
username: admin
temporary password: Admin@12345
role: admin
```

Important:

- Document this is for staging only.
- Do not expose password in API.
- Require changing later in production hardening.

If an admin already exists, do not overwrite it.

---

# BACKEND AUTH SERVICE

Create:

```text
app/services/auth_service.py
```

Recommended functions:

```python
authenticate_user(db, username_or_email, password)
create_session_for_user(db, user)
get_current_user_from_request(db, request)
logout_user(db, request)
```

---

# AUTH ROUTER

Create:

```text
app/routers/auth.py
```

Required endpoints:

## Login

```text
POST /api/auth/login
```

Payload:

```json
{
  "username_or_email": "admin",
  "password": "Admin@12345"
}
```

Behavior:

- Validate credentials.
- Reject inactive users.
- Set HTTP-only auth cookie.
- Return current user profile without password hash.

---

## Current User

```text
GET /api/auth/me
```

Returns:

```json
{
  "id": 1,
  "full_name": "...",
  "username": "admin",
  "role": "admin",
  "role_label": "مدير النظام",
  "permissions": [...]
}
```

---

## Logout

```text
POST /api/auth/logout
```

Clears auth cookie/session.

---

# UPDATE RBAC CURRENT USER RESOLUTION

Update:

```text
app/rbac.py
```

Current behavior:

```text
X-Dev-Role
```

New behavior:

1. Resolve authenticated user from cookie/session.
2. Use user's actual stored role.
3. Use that role for `require_permission()` and `require_any_permission()`.

Development fallback:

- Allow `X-Dev-Role` only when:

```text
NEWS2_ALLOW_DEV_ROLE=true
```

Default in production/staging should be:

```text
false
```

For Render deployment, do not depend on dev role.

---

# REMOVE FRONTEND ROLE SWITCHER

Update:

```text
app/static/app.js
```

Remove or hide the role dropdown from normal users.

Instead show:

```text
المستخدم الحالي
الدور
```

Example:

```text
د. أحمد خالد — طبيب
```

Only in development mode, optionally show a small hidden dev switcher if backend confirms dev role is enabled.

But for deployed app, do not show role switching.

---

# LOGIN UI

Implement real Arabic login screen.

Fields:

```text
اسم المستخدم أو البريد الإلكتروني
كلمة المرور
```

Button:

```text
تسجيل الدخول
```

Error messages:

```text
بيانات الدخول غير صحيحة
الحساب غير مفعل
تعذر تسجيل الدخول
```

Success:

- Load user from `/api/auth/me`
- Load app data
- Navigate to dashboard

---

# ROUTE PROTECTION

If user is not authenticated:

- Show login screen.
- Do not load clinical/research data.
- Do not show sidebar.
- Do not allow access to hash routes.

After login:

- Show dashboard.
- Apply RBAC navigation filtering.

---

# API CLIENT

Update frontend fetch wrapper:

- Include credentials:

```javascript
credentials: "include"
```

- On `401`, redirect to login screen.
- Remove `X-Dev-Role` header unless backend/dev mode explicitly allows it.

---

# BACKEND PROTECTED ENDPOINTS

All endpoints already protected by RBAC should now use the authenticated user role.

For read endpoints that are currently public, decide minimum permissions:

Examples:

```text
GET /api/patients              => patients:view
GET /api/alerts                => alerts:view
GET /api/research/summary      => research:view
GET /api/rbac/me               => authenticated user context
```

Keep `/health` public.

Keep `/` and static assets public.

---

# COOKIES / SECURITY SETTINGS

Add config options:

```text
NEWS2_SESSION_SECRET
NEWS2_SESSION_COOKIE_NAME
NEWS2_SESSION_MAX_AGE_SECONDS
NEWS2_COOKIE_SECURE
NEWS2_ALLOW_DEV_ROLE
```

Defaults:

```text
NEWS2_SESSION_COOKIE_NAME=news2_session
NEWS2_SESSION_MAX_AGE_SECONDS=86400
NEWS2_COOKIE_SECURE=false for local
NEWS2_ALLOW_DEV_ROLE=false
```

On Render, set `NEWS2_COOKIE_SECURE=true` if HTTPS works.

If `NEWS2_SESSION_SECRET` is missing, generate safe dev warning locally, but production should require it or use a strong fallback with warning.

---

# RENDER ENVIRONMENT VARIABLES

After implementation, Render should add:

```text
NEWS2_SESSION_SECRET=<strong random secret>
NEWS2_COOKIE_SECURE=true
NEWS2_ALLOW_DEV_ROLE=false
NEWS2_AUTO_SEED=true
```

Do not remove:

```text
NEWS2_DATABASE_URL
```

---

# AUDIT LOGS

Add audit logs for:

```text
auth_login_success
auth_login_failed
auth_logout
auth_unauthorized_access
```

Do not log passwords.

---

# TESTS

Create:

```text
tests/test_authentication_security.py
```

Required tests:

1. Login succeeds with valid admin credentials.
2. Login fails with wrong password.
3. Inactive user cannot login.
4. `/api/auth/me` returns authenticated user.
5. Logout clears session.
6. Protected endpoint returns 401 when unauthenticated.
7. Protected endpoint works when authenticated.
8. RBAC uses stored user role, not arbitrary frontend role.
9. `X-Dev-Role` ignored when `NEWS2_ALLOW_DEV_ROLE=false`.
10. `X-Dev-Role` allowed only when explicit dev setting is true.
11. Password hash is never returned.
12. Role dropdown/switcher no longer appears in production frontend if testable.

Update existing RBAC tests to authenticate users properly where needed.

---

# DOCUMENTATION

Create:

```text
docs/authentication_security.md
```

Update:

```text
README.md
docs/rbac.md
docs/user_management.md
docs/system_architecture.md
```

Document:

- login flow
- session/cookie strategy
- how RBAC now uses authenticated user role
- how to set Render environment variables
- initial staging admin
- security limitations
- next hardening steps

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual local validation:

1. Open app.
2. Login screen appears.
3. Login as admin.
4. Dashboard appears.
5. Role dropdown is gone.
6. Administration visible for admin.
7. Logout.
8. Login as nurse.
9. Administration hidden.
10. Direct protected API without login returns 401.
11. Role cannot be changed manually from UI.

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Add real authentication and secure RBAC user context"
git push origin main
```

Render auto-deploys.

After deploy, set Render env vars:

```text
NEWS2_SESSION_SECRET
NEWS2_COOKIE_SECURE=true
NEWS2_ALLOW_DEV_ROLE=false
```

Then test production login.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Authentication architecture
4. Session/cookie behavior
5. RBAC current-user changes
6. Login/logout frontend behavior
7. Role switcher removal
8. Protected endpoint behavior
9. Tests added/updated
10. Validation results
11. Render environment variables required
12. Security limitations
13. Deployment commands
14. Risks

---

# NEXT PHASE

After this phase:

```text
Phase 17 — Production Security Hardening
```

Recommended focus:

```text
CSRF protection
Rate limiting
Password change workflow
Admin password rotation
Audit log viewer hardening
Security headers
Favicon/branding cleanup
```
