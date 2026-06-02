from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import admin, alerts, deterioration, dialysis_sessions, health, monitoring, news2, outcomes, patients, research, responses


settings = get_settings()
app = FastAPI(
    title="NEWS2 Hemodialysis Monitoring Platform",
    description="Arabic-first clinical research platform for hemodialysis NEWS2 monitoring.",
    version="0.2.0",
)

app.include_router(health.router)
app.include_router(patients.router)
app.include_router(dialysis_sessions.router)
app.include_router(alerts.router)
app.include_router(research.router)
app.include_router(monitoring.router)
app.include_router(news2.router)
app.include_router(deterioration.router)
app.include_router(responses.router)
app.include_router(outcomes.router)
app.include_router(admin.router)

static_dir = Path(settings.static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/styles.css", include_in_schema=False)
def serve_legacy_styles() -> FileResponse:
    return FileResponse(static_dir / "styles.css")


@app.get("/app.js", include_in_schema=False)
def serve_legacy_app_js() -> FileResponse:
    return FileResponse(static_dir / "app.js")
