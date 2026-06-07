# Authentication And Session Security

Phase 16 adds production authentication for the NEWS2 Hemodialysis Monitoring Platform.

## Runtime Configuration

- `NEWS2_SESSION_SECRET`: HMAC secret used to hash session tokens. Set this in production.
- `NEWS2_SESSION_COOKIE_NAME`: session cookie name. Default: `news2_session`.
- `NEWS2_SESSION_MAX_AGE_SECONDS`: session lifetime. Default: `86400`.
- `NEWS2_COOKIE_SECURE`: set `true` when serving over HTTPS. Default: `false` for local development.
- `NEWS2_ALLOW_DEV_ROLE`: allows `X-Dev-Role` impersonation for tests/local development only. Default: `false`.

If `NEWS2_SESSION_SECRET` is absent, the application uses an in-process development secret and emits a runtime warning. That fallback invalidates sessions on restart and must not be used for production.

## Login Flow

- `POST /api/auth/login` accepts `username_or_email` and `password`.
- Passwords are verified against the stored PBKDF2 password hash.
- Successful login creates an `auth_sessions` row with a hashed session token and sets an HTTP-only cookie.
- Raw session tokens are never stored in the database and are not returned in JSON.
- `GET /api/auth/me` returns the authenticated user identity, role label, and permissions.
- `POST /api/auth/logout` deletes the current session and clears the cookie.

Seeded local admin credentials:

```text
username: admin
password: Admin@12345
```

## RBAC Behavior

RBAC permissions are resolved from the authenticated user's stored role. The frontend no longer sends public role headers in normal operation and does not use localStorage authentication tokens.

`X-Dev-Role` is ignored unless `NEWS2_ALLOW_DEV_ROLE=true`. When enabled, it remains a development/test convenience only.

## Protected Reads

The application protects clinical and research read endpoints with RBAC. Examples:

- `GET /api/patients`: `patients:view`
- `GET /api/alerts`: `alerts:view`
- `GET /api/research/summary`: `research:view`
- `GET /api/rbac/me`: authenticated session or explicitly enabled dev role

Public endpoints remain:

- `GET /health`
- `GET /`
- static frontend assets

## Audit Events

Authentication writes audit logs for:

- `auth_login_success`
- `auth_login_failed`
- `auth_logout`
- `auth_unauthorized_access`

Permission failures continue to write `permission_denied`.
