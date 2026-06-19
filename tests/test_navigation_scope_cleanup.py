from pathlib import Path


APP_JS = Path(__file__).resolve().parents[1] / "app" / "static" / "app.js"


def _navigation_registry_source() -> str:
    source = APP_JS.read_text(encoding="utf-8")
    start = source.index("const NAV_GROUPS = [")
    end = source.index("const NAV_ROUTE_LABELS =", start)
    return source[start:end]


def test_sidebar_navigation_keeps_research_monitoring_scope():
    registry = _navigation_registry_source()

    required_routes = {
        "dashboard",
        "patients",
        "patient-profile",
        "patient-baseline",
        "sessions",
        "intradialytic-monitoring",
        "vital-signs-entry",
        "news2-assessment",
        "news2-history",
        "active-alerts",
        "deterioration-events",
        "response-workflow",
        "clinical-outcomes",
        "outcome-tracking",
        "export-center",
        "research-dashboard",
        "study-metrics",
        "prediction-evaluation",
        "nursing-training",
        "alignment-audit",
        "dataset-statistics",
        "study-management",
        "users",
    }

    for route in required_routes:
        assert f'route: "{route}"' in registry


def test_sidebar_navigation_hides_out_of_scope_routes():
    registry = _navigation_registry_source()

    hidden_routes = {
        "vascular-access",
        "session-details",
        "news2-trend",
        "alert-details",
        "alert-timeline",
        "event-details",
        "event-timeline",
        "response-analytics",
        "outcome-analytics",
        "pre-post-comparison",
        "research-protocol",
        "study-timeline",
        "study-readiness",
        "create-user",
        "roles",
        "permissions",
        "audit-logs",
        "system-settings",
        "language-settings",
    }

    for route in hidden_routes:
        assert f'route: "{route}"' not in registry
