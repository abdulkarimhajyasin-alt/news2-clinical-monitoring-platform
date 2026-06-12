# AUTH FIX — ENSURE STAGING ADMIN CAN LOGIN

## Objective

Fix the production login issue after Phase 16 where `/api/auth/login` returns `401 Unauthorized` for:

```text
username: admin
password: Admin@12345
```

The app is deployed on Render and PostgreSQL/Neon is working, but the admin login fails.

---

# CURRENT PROBLEM

Render logs show:

```text
GET /api/auth/me 401 Unauthorized
POST /api/auth/login 401 Unauthorized
```

This confirms:

- auth endpoints exist
- login endpoint works
- credential verification fails

Likely cause:

The Neon database already had users from Phase 15 before Phase 16 added real password verification. Startup sees users exist and does not create/reset a usable admin password.

---

# CRITICAL RULES

Do not drop tables.

Do not delete users.

Do not reset all staff.

Do not expose password hashes.

Do not store plain text passwords.

Do not weaken authentication.

Keep existing data intact.

---

# REQUIRED FIX

Add a safe startup/admin bootstrap flow that guarantees a valid active admin account exists for staging.

## Behavior

On startup:

1. Check for username:

```text
admin
```

2. If no admin exists:
   - create admin user
   - role = admin
   - is_active = true
   - password hash from configured default password

3. If admin exists but:
   - role is not admin
   - is_active is false
   - password_hash is missing/empty/legacy invalid

   then safely repair only these fields:
   - role = admin
   - is_active = true
   - password_hash = hash(default admin password)

4. Do NOT overwrite admin password every startup if a valid hash exists, unless forced by env var.

---

# ENVIRONMENT VARIABLES

Add support:

```text
NEWS2_DEFAULT_ADMIN_USERNAME=admin
NEWS2_DEFAULT_ADMIN_PASSWORD=Admin@12345
NEWS2_FORCE_ADMIN_PASSWORD_RESET=false
```

Behavior:

- If `NEWS2_FORCE_ADMIN_PASSWORD_RESET=true`, reset admin password on startup to `NEWS2_DEFAULT_ADMIN_PASSWORD`.
- Otherwise only set password if missing/invalid.

For current staging deployment, this lets us temporarily set:

```text
NEWS2_FORCE_ADMIN_PASSWORD_RESET=true
```

for one deployment, login, then later set it back to false.

---

# IMPLEMENTATION LOCATION

Update one or more of:

```text
app/startup.py
app/seed.py
app/config.py
app/security/passwords.py
```

Prefer keeping it in startup/admin bootstrap logic.

Recommended function:

```python
ensure_default_admin_user(db)
```

or:

```python
ensure_staging_admin(db)
```

---

# PASSWORD HASH VALIDATION

Use the existing Phase 16 password hashing utilities.

If possible, add helper:

```python
is_password_hash_usable(password_hash: str) -> bool
```

It should detect:

- empty/null
- invalid format
- legacy placeholder values

Do not verify by logging or exposing password.

---

# LOGGING

Add clear safe logs:

```text
Ensuring default admin user...
Default admin created.
Default admin already usable.
Default admin repaired for staging login.
```

Do not log the password.

---

# TESTS

Add or update:

```text
tests/test_admin_bootstrap_login.py
```

Required tests:

1. No admin exists -> startup creates active admin.
2. Existing admin with missing password hash -> repairs hash.
3. Existing inactive admin -> activates it.
4. Existing admin with non-admin role -> repairs role.
5. Existing valid admin is not overwritten when force reset is false.
6. Force reset true updates admin password hash.
7. Login succeeds after bootstrap.
8. Password hash is never returned.

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

Manual local validation:

1. Start server.
2. Login with:

```text
admin / Admin@12345
```

3. Confirm dashboard loads.

---

# DEPLOYMENT STEPS

After implementation:

```bash
git add .
git commit -m "Ensure default admin login works after auth migration"
git push origin main
```

On Render Environment add:

```text
NEWS2_DEFAULT_ADMIN_USERNAME=admin
NEWS2_DEFAULT_ADMIN_PASSWORD=Admin@12345
NEWS2_FORCE_ADMIN_PASSWORD_RESET=true
```

Deploy once.

After successful login, change:

```text
NEWS2_FORCE_ADMIN_PASSWORD_RESET=false
```

or remove it.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Root cause
4. Admin bootstrap behavior
5. Environment variables added
6. Tests added/updated
7. Validation results
8. Render deployment instructions
9. Security notes
