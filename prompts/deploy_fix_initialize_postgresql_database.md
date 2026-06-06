# DEPLOY FIX — INITIALIZE POSTGRESQL DATABASE ON STARTUP

## Objective

Fix the Render + Neon deployment issue where the FastAPI app starts successfully but API endpoints fail with:

```text
psycopg2.errors.UndefinedTable: relation "alerts" does not exist
```

This means the production PostgreSQL database is connected but tables were not created.

The fix must safely initialize database tables on startup and optionally seed initial demo/research data only when the database is empty.

---

# CURRENT PROBLEM

Render deployment is live, but `/api/patients` returns:

```text
Internal Server Error
```

Render logs show:

```text
relation "alerts" does not exist
LINE 3: FROM alerts
```

Because Render Free does not support Shell access, we cannot manually run:

```bash
python -m app.seed
```

Therefore, the application must create tables automatically on startup in staging/deployment.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.
Do not break existing routes.
Do not destroy existing data.
Do not drop tables.
Do not reset the production database.
Do not force duplicate seed data.
Do not remove local SQLite support.

---

# REQUIRED FIX

Add a safe startup initialization flow.

On FastAPI startup:

1. Create all database tables if missing.
2. Do not drop or recreate existing tables.
3. If the database is empty, optionally run the existing idempotent seed logic.
4. Log clear startup messages.

Use existing SQLAlchemy metadata:

```python
Base.metadata.create_all(bind=engine)
```

---

# IMPLEMENTATION OPTIONS

Prefer adding a small initialization helper.

Recommended file:

```text
app/startup.py
```

Functions:

```python
initialize_database()
seed_database_if_empty()
```

Then call from:

```text
app/main.py
```

using FastAPI lifespan or startup event.

Prefer modern FastAPI lifespan if simple.

---

# DATABASE INITIALIZATION

Use:

```text
app.database.Base
app.database.engine
```

or the actual project equivalents.

Required:

```python
Base.metadata.create_all(bind=engine)
```

This must run before requests are served.

---

# SAFE SEEDING

If the existing `app.seed` has a safe idempotent function, reuse it.

If `app.seed` only works as a script, refactor carefully to expose a function like:

```python
seed_database()
```

or:

```python
run_seed()
```

Rules:

- Seed only if no patients exist or no users exist.
- Do not duplicate rows.
- Do not overwrite existing production data.
- Keep local seed behavior working:

```bash
python -m app.seed
```

---

# ENVIRONMENT CONTROL

Add environment setting if useful:

```text
NEWS2_AUTO_SEED
```

Default:

```text
true
```

for now in staging/demo.

If implemented, document:

```text
NEWS2_AUTO_SEED=true
```

But avoid requiring the environment variable for table creation.

Table creation must always be safe.

---

# LOGGING

On startup, print or log clear messages:

```text
Initializing database tables...
Database tables ready.
Checking seed data...
Seed data already exists.
```

or:

```text
Seed data created.
```

---

# TESTS

Add or update tests:

```text
tests/test_startup_database_initialization.py
```

Required tests:

1. `initialize_database()` can be called without crashing.
2. Tables are created in an empty database.
3. Calling initialization twice is safe.
4. Seed flow does not duplicate data.
5. Existing tests still pass.

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Also run locally:

```bash
uvicorn app.main:app --reload
```

Verify:

```text
http://127.0.0.1:8000/api/patients
```

returns JSON, not 500.

---

# DEPLOYMENT AFTER FIX

After implementing, run:

```bash
git add .
git commit -m "Initialize production database on startup"
git push origin main
```

Render should auto-deploy.

After deploy, verify:

```text
https://news2-clinical-monitoring.onrender.com/api/patients
https://news2-clinical-monitoring.onrender.com/api/research/summary
```

Both must return JSON.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Startup initialization implementation
4. Seed safety behavior
5. Tests added or updated
6. Validation results
7. Deployment commands
8. Risks
