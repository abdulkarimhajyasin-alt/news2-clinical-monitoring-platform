# Enterprise User Management

Phase 15 adds staff user management and RBAC hardening without enabling production login.

## Scope

Administrators and technical administrators can create staff accounts, assign platform roles, set department and job title metadata, and activate or deactivate users.

This phase does not implement JWT, sessions, password reset, MFA, or external identity providers. Phase 16 must replace the temporary `X-Dev-Role` context with real authentication.

## Staff Fields

The staff management API uses the existing `users` table and safely extends it with:

- `username`
- `job_title`
- `is_active`

Existing columns such as `full_name`, `email`, `phone`, `department`, `role`, `status`, `password_hash`, `created_at`, and `updated_at` remain in place.

## API

- `GET /api/users`: list staff users. Requires `users:view`.
- `POST /api/users`: create staff user. Requires `users:create`.
- `GET /api/users/{id}`: read one staff user. Requires `users:view`.
- `PUT /api/users/{id}`: update staff metadata and role. Requires `users:update`.
- `POST /api/users/{id}/status`: activate/deactivate staff user. Requires `users:disable`.

List filters:

- `role`
- `is_active`
- `department`
- `search`

## Password Handling

Create staff accepts `temporary_password`. The backend hashes it using PBKDF2-HMAC with a random salt and stores only `password_hash`.

API responses never include:

- plain password
- temporary password
- password hash

The temporary password is reserved for Phase 16 authentication and cannot be used to log in during Phase 15.

## Roles

Phase 15 adds:

- `technical_admin`: `تقني النظام`

Technical administrators can manage users, RBAC visibility, audit viewing, and settings. They can view basic platform data but cannot perform clinical write actions such as creating measurements, deterioration events, responses, outcomes, or managing alerts.

## Frontend

The Administration navigation group is visible only when the current role has administration permissions. In the development role switcher:

- `admin` sees Administration.
- `technical_admin` sees Administration.
- `doctor`, `on_call_doctor`, `nurse`, and `researcher` do not see Administration by default.

The Users screen lists staff and supports activating/deactivating accounts. The Add Staff screen posts to `POST /api/users`.
