# NEWS2 Hemodialysis Monitoring Platform

Arabic-first clinical research MVP for monitoring hemodialysis patients using NEWS2, documenting alerts, deterioration events, medical/nursing responses, response times, and 24-72 hour outcomes.

## Stack

- FastAPI
- SQLAlchemy 2.x
- SQLite for local development
- PostgreSQL-ready `NEWS2_DATABASE_URL` configuration
- Pydantic schemas
- Static RTL frontend served by FastAPI

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Seed Database

```bash
python -m app.seed
```

This creates local SQLite tables and inserts fake anonymized clinical research data.

## Run Locally

```bash
uvicorn app.main:app --reload
```

Open:

- UI: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- API docs: `http://127.0.0.1:8000/docs`

## Validation

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```
