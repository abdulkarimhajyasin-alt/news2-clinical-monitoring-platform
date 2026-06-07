# Role Based Access Control Foundation

Phase 14 added centralized RBAC for the NEWS2 Hemodialysis Monitoring Platform. Phase 15 hardens it with enterprise staff management and the `technical_admin` role.

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

## Development User Context

Until Phase 16 authentication is implemented, the backend reads a temporary development role from:

```text
X-Dev-Role
```

If the header is absent, the role defaults to `admin` for local/demo continuity. Invalid roles return `400 Bad Request`.

This is not production authentication.

## RBAC API

- `GET /api/rbac/me`: returns the current development role and permissions.
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

- `POST /api/monitoring/measurements` requires `measurements:create`.
- `POST /api/deterioration/events` requires `deterioration:create`.
- `POST /api/responses` requires `responses:create`.
- `POST /api/outcomes` requires `outcomes:create`.
- Alert acknowledge/start/close require `alerts:manage`.

## Frontend Behavior

The frontend loads `/api/rbac/me`, stores the current role and permissions, and sends `X-Dev-Role` with API requests. A small development role switcher allows testing role behavior before full authentication.

Restricted export buttons and study-management actions are hidden or disabled with Arabic messages.

The Administration navigation group is visible only to roles with administration permissions. By default that means `admin` and `technical_admin`; `doctor`, `on_call_doctor`, `nurse`, and `researcher` do not see the Administration group.

## Audit Logging

Permission denials write a simple `permission_denied` audit log with role, permission, and path when the database is available.

## Limitations

Phase 15 does not implement login, sessions, cookies, JWT, password reset, MFA, or production authentication. It stores hashed temporary passwords for staff accounts so Phase 16 can add real authentication safely.
