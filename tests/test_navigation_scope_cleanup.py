from pathlib import Path


APP_JS = Path(__file__).resolve().parents[1] / "app" / "static" / "app.js"


def _navigation_registry_source() -> str:
    source = APP_JS.read_text(encoding="utf-8")
    start = source.index("const NAV_GROUPS = [")
    end = source.index("const NAV_ROUTE_LABELS =", start)
    return source[start:end]


def _navigation_label_source() -> str:
    source = APP_JS.read_text(encoding="utf-8")
    start = source.index("const ROUTE_LABEL_OVERRIDES =")
    end = source.index("const appState =", start)
    return source[start:end]


def test_sidebar_navigation_keeps_research_monitoring_scope():
    registry = _navigation_registry_source()

    required_routes = {
        "dashboard",
        "patients",
        "patient-profile",
        "patient-baseline",
        "create-patient",
        "sessions",
        "create-session",
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
        "prediction-evaluation",
        "nursing-training",
        "alignment-audit",
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
        "medical-response-log",
        "nursing-response-log",
        "response-time-dashboard",
        "response-analytics",
        "outcome-analytics",
        "pre-post-comparison",
        "study-metrics",
        "dataset-statistics",
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


def test_sidebar_navigation_uses_thesis_scope_visible_labels():
    labels = _navigation_label_source()

    required_labels = {
        "الرئيسية",
        "المرضى",
        "ملف المريض",
        "البيانات الأساسية",
        "إضافة مريض",
        "جلسات الغسيل",
        "تسجيل جلسة",
        "المراقبة الرقمية",
        "إدخال القياسات",
        "نتيجة HD2-mNEWS",
        "سجل HD2-mNEWS",
        "التنبيهات",
        "توثيق التدهور",
        "الاستجابة السريرية",
        "تتبع النتيجة",
        "النتيجة السريرية 72 ساعة",
        "بيانات البحث",
        "التحليل البحثي",
        "تقييم التنبؤ",
        "تدريب التمريض",
        "تدقيق مطابقة الرسالة",
        "بروتوكول الدراسة",
        "إدارة المستخدمين",
    }

    for label in required_labels:
        assert label in labels

    retired_labels = {
        "تقييم NEWS2",
        "سجل NEWS2",
        "اتجاه NEWS2",
    }

    for label in retired_labels:
        assert label not in labels
