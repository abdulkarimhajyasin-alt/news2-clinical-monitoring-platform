# Role Based Access Control Foundation

Phase 14 added centralized RBAC for the NEWS2 Hemodialysis Monitoring Platform. Phase 15 hardened it with enterprise staff management and the `technical_admin` role. Phase 16 resolves RBAC from authenticated user sessions.

## Roles

- `admin`: مدير النظام
- `technical_admin`: تقني النظام
- `doctor`: طبيب
- `on_call_doctor`: طبيب مناوب
- `nurse`: ممرض/ممرضة
- `researcher`: باحث

## Permission Model

Permissions use stable `resource:action` strings such as:

- `patients:view`
- `measurements:create`
- `alerts:manage`
- `research:export`
- `studies:update`
- `users:create`
- `users:update`
- `users:disable`
- `rbac:view`
- `rbac:manage`
- `audit:view`
- `settings:manage`

The permission matrix is centralized in `app/rbac.py`.

## Authenticated User Context

The backend reads the current user from the HTTP-only `news2_session` cookie and derives permissions from the user's stored database role.

For local development and automated tests only, `X-Dev-Role` can be enabled with:

```text
NEWS2_ALLOW_DEV_ROLE=true
```

When `NEWS2_ALLOW_DEV_ROLE=false` or unset, `X-Dev-Role` is ignored and unauthenticated requests receive `401`.

## RBAC API

- `GET /api/rbac/me`: returns the current authenticated user role and permissions.
- `GET /api/rbac/permissions`: returns the full role and permission matrix. Requires `rbac:view`.
- `/api/users`: staff user management endpoints. Require `users:view`, `users:create`, `users:update`, or `users:disable`.

## Protected Endpoints

Research:

- Dataset preview and quality require `research:view`.
- Analytics require `research:analytics`.
- CSV/XLSX/SPSS exports require `research:export`.

Study management:

- Listing and readiness require `studies:view`.
- Creating studies requires `studies:create`.
- Updating studies requires `studies:update`.

Clinical writes:

- Clinical/research reads such as patients, alerts, monitoring history, NEWS2 assessments, deterioration events, responses, outcomes, and research summary require the matching `*:view` permission.
- `POST /api/monitoring/measurements` requires `measurements:create`.
- `POST /api/deterioration/events` requires `deterioration:create`.
- `POST /api/responses` requires `responses:create`.
- `POST /api/outcomes` requires `outcomes:create`.
- Alert acknowledge/start/close require `alerts:manage`.

## Frontend Behavior

The frontend loads `/api/auth/me`, stores the authenticated user and permissions, and sends cookie-authenticated API requests. It does not store auth tokens in localStorage.

A development role switcher is hidden unless the backend returns `allow_dev_role=true`.

Restricted export buttons and study-management actions are hidden or disabled with Arabic messages.

The Administration navigation group is visible only to roles with administration permissions. By default that means `admin` and `technical_admin`; `doctor`, `on_call_doctor`, `nurse`, and `researcher` do not see the Administration group.

## Audit Logging

Permission denials write a simple `permission_denied` audit log with role, permission, and path when the database is available. Authentication writes `auth_login_success`, `auth_login_failed`, `auth_logout`, and `auth_unauthorized_access`.

## Limitations

Phase 16 does not add password reset, MFA, SSO, device management, or institution-specific identity-provider integration.
