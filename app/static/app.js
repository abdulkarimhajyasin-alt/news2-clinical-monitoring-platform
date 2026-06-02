const routes = [
  { id: "dashboard", label: "لوحة التحكم", group: "الرصد السريري", icon: "D", type: "dashboard" },
  { id: "patients", label: "قائمة المرضى", group: "المرضى", icon: "P", type: "patients" },
  { id: "create-patient", label: "إضافة مريض", group: "المرضى", icon: "+", type: "form", entity: "patient" },
  { id: "patient-profile", label: "ملف المريض", group: "المرضى", icon: "ID", type: "profile" },
  { id: "patient-baseline", label: "الخط الأساسي", group: "المرضى", icon: "B", type: "baseline" },
  { id: "vascular-access", label: "الوصول الوعائي", group: "المرضى", icon: "V", type: "vascular" },
  { id: "sessions", label: "جلسات الغسيل", group: "الجلسات", icon: "S", type: "sessions" },
  { id: "create-session", label: "إنشاء جلسة", group: "الجلسات", icon: "+", type: "form", entity: "session" },
  { id: "session-details", label: "تفاصيل الجلسة", group: "الجلسات", icon: "SD", type: "details", entity: "session" },
  { id: "intradialytic-monitoring", label: "الرصد أثناء الجلسة", group: "الجلسات", icon: "M", type: "monitoring" },
  { id: "vital-signs-entry", label: "إدخال العلامات الحيوية", group: "التقييم", icon: "VS", type: "form", entity: "vitals" },
  { id: "news2-assessment", label: "تقييم NEWS2", group: "التقييم", icon: "N2", type: "assessment" },
  { id: "news2-trend", label: "اتجاه NEWS2", group: "التقييم", icon: "T", type: "trend" },
  { id: "news2-history", label: "سجل NEWS2", group: "التقييم", icon: "H", type: "table", entity: "news2" },
  { id: "active-alerts", label: "التنبيهات النشطة", group: "التنبيهات", icon: "A", type: "alerts" },
  { id: "alert-details", label: "تفاصيل التنبيه", group: "التنبيهات", icon: "AD", type: "details", entity: "alert" },
  { id: "alert-timeline", label: "تسلسل التنبيه", group: "التنبيهات", icon: "TL", type: "timeline", entity: "alert" },
  { id: "deterioration-events", label: "أحداث التدهور", group: "الأحداث", icon: "E", type: "table", entity: "events" },
  { id: "event-details", label: "تفاصيل الحدث", group: "الأحداث", icon: "ED", type: "details", entity: "event" },
  { id: "event-timeline", label: "تسلسل الحدث", group: "الأحداث", icon: "ET", type: "timeline", entity: "event" },
  { id: "medical-response-log", label: "سجل الاستجابة الطبية", group: "الاستجابة", icon: "MR", type: "table", entity: "medical" },
  { id: "nursing-response-log", label: "سجل الاستجابة التمريضية", group: "الاستجابة", icon: "NR", type: "table", entity: "nursing" },
  { id: "response-workflow", label: "مسار الاستجابة", group: "الاستجابة", icon: "WF", type: "workflow" },
  { id: "response-time-dashboard", label: "زمن الاستجابة", group: "الاستجابة", icon: "RT", type: "analytics" },
  { id: "response-analytics", label: "تحليلات الاستجابة", group: "التحليلات", icon: "RA", type: "analytics" },
  { id: "clinical-outcomes", label: "المخرجات السريرية", group: "المخرجات", icon: "CO", type: "table", entity: "outcomes" },
  { id: "outcome-tracking", label: "تتبع المخرجات", group: "المخرجات", icon: "OT", type: "workflow" },
  { id: "outcome-analytics", label: "تحليلات المخرجات", group: "المخرجات", icon: "OA", type: "analytics" },
  { id: "research-dashboard", label: "لوحة البحث", group: "البحث", icon: "R", type: "research" },
  { id: "pre-post-comparison", label: "مقارنة قبل وبعد", group: "البحث", icon: "PP", type: "comparison" },
  { id: "study-metrics", label: "مؤشرات الدراسة", group: "البحث", icon: "SM", type: "analytics" },
  { id: "dataset-statistics", label: "إحصاءات البيانات", group: "البحث", icon: "DS", type: "analytics" },
  { id: "export-center", label: "مركز التصدير", group: "البحث", icon: "EX", type: "export" },
  { id: "users", label: "المستخدمون", group: "الإدارة", icon: "U", type: "table", entity: "users" },
  { id: "roles", label: "الأدوار", group: "الإدارة", icon: "RO", type: "table", entity: "roles" },
  { id: "permissions", label: "الصلاحيات", group: "الإدارة", icon: "PR", type: "permissions" },
  { id: "audit-logs", label: "سجلات التدقيق", group: "الإدارة", icon: "AL", type: "table", entity: "audit" },
  { id: "system-settings", label: "إعدادات النظام", group: "الإعدادات", icon: "ST", type: "settings" },
  { id: "language-settings", label: "إعدادات اللغة", group: "الإعدادات", icon: "LG", type: "language" }
];

const appState = {
  health: null,
  patients: [],
  dialysisSessions: [],
  alerts: [],
  researchSummary: null,
  loading: {},
  errors: {}
};

const api = {
  async request(path) {
    try {
      const response = await fetch(path, { headers: { Accept: "application/json" } });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw new Error(error.message || "network_error");
    }
  },
  getHealth() {
    return this.request("/health").then(normalizeHealth);
  },
  getPatients() {
    return this.request("/api/patients").then((rows) => rows.map(normalizePatient));
  },
  getDialysisSessions() {
    return this.request("/api/dialysis-sessions").then((rows) => rows.map(normalizeSession));
  },
  getAlerts() {
    return this.request("/api/alerts").then((rows) => rows.map(normalizeAlert));
  },
  getResearchSummary() {
    return this.request("/api/research/summary").then(normalizeResearchSummary);
  }
};

const app = document.getElementById("app");

const fallbackRows = {
  news2: [["N-771", "ANON-P-1002", "06:00", "3", "متوسط", "تمت المراجعة"], ["N-772", "ANON-P-1002", "08:30", "16", "حرج", "تصعيد نشط"]],
  events: [["E-310", "هبوط ضغط حاد", "ANON-P-1002", "08:42", "حرج", "مفتوح"]],
  medical: [["08:43", "طبيب كلى", "تقييم فوري", "تعديل معدل السحب", "مكتمل"]],
  nursing: [["08:41", "تمريض الجلسة", "إعادة قياس العلامات", "مكتمل"]],
  outcomes: [["O-120", "ANON-P-1002", "إيقاف الجلسة مبكرا", "24 ساعة", "مستقر"]],
  users: [["U-01", "د. باحث سريري 01", "إدارة", "نشط", "بيانات تجريبية"]],
  roles: [["طبيب", "18 صلاحية", "تقييم وتصعيد", "نشط"], ["تمريض", "14 صلاحية", "إدخال ومتابعة", "نشط"]],
  audit: [["09:10", "U-01", "تهيئة قاعدة البيانات", "seed_v1", "نجاح"]]
};

const formFields = {
  patient: ["الاسم الكامل", "رقم الملف", "تاريخ الميلاد", "الجنس", "نوع الوصول الوعائي", "الأمراض المصاحبة", "خطة الغسيل", "ملاحظات سريرية"],
  session: ["المريض", "تاريخ الجلسة", "وقت البدء", "الوزن قبل الجلسة", "معدل السحب", "الضغط الابتدائي", "حالة الوصول", "ملاحظات الفريق"],
  vitals: ["معدل التنفس", "تشبع الأكسجين", "ضغط الدم الانقباضي", "النبض", "درجة الحرارة", "مستوى الوعي", "الأكسجين الإضافي", "ملاحظات القياس"]
};

const subtitles = {
  dashboard: "رصد تشغيلي مباشر للمخاطر والتنبيهات وجودة الاستجابة.",
  patients: "قائمة مرضى الغسيل الكلوي من قاعدة البيانات المحلية.",
  sessions: "جلسات الغسيل المسجلة في قاعدة البيانات.",
  "active-alerts": "تنبيهات سريرية حقيقية من بيانات التهيئة المحلية.",
  "research-dashboard": "ملخص بحثي مباشر من قاعدة البيانات.",
  default: "واجهة سريرية متصلة ضمن نظام NEWS2."
};

function normalizeHealth(data) {
  return {
    status: data?.status || "unknown",
    service: data?.service || "",
    database: data?.database || "unknown",
    connected: data?.status === "ok" && data?.database === "connected"
  };
}

function normalizePatient(row) {
  return {
    id: row.id,
    patientCode: row.patient_code || `P-${row.id}`,
    age: row.age ?? "-",
    gender: row.gender || "unknown",
    studyPhase: row.study_phase || "unknown",
    studyGroup: row.study_group || "unknown",
    dialysisVintageMonths: row.dialysis_vintage_months ?? "-",
    weeklySessionsCount: row.weekly_sessions_count ?? "-"
  };
}

function normalizeSession(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    sessionDate: row.session_date || "-",
    weekday: row.weekday || "-",
    actualStartTime: row.actual_start_time || null,
    actualEndTime: row.actual_end_time || null,
    targetUltrafiltration: row.target_ultrafiltration ?? "-",
    sessionStatus: row.session_status || "unknown"
  };
}

function normalizeAlert(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    riskLevel: row.risk_level || "unknown",
    severityLevel: row.severity_level || "unknown",
    status: row.status || "unknown",
    priority: row.priority || "-",
    triggerReason: row.trigger_reason || "-",
    createdAt: row.created_at || null
  };
}

function normalizeResearchSummary(row) {
  return {
    patientsCount: row?.patients_count ?? 0,
    sessionsCount: row?.sessions_count ?? 0,
    measurementsCount: row?.measurements_count ?? 0,
    news2AssessmentsCount: row?.news2_assessments_count ?? 0,
    alertsCount: row?.alerts_count ?? 0,
    activeAlertsCount: row?.active_alerts_count ?? 0,
    deteriorationEventsCount: row?.deterioration_events_count ?? 0,
    responsesCount: row?.responses_count ?? 0,
    outcomesCount: row?.outcomes_count ?? 0,
    averageNews2: row?.average_news2 ?? null
  };
}

const labels = {
  risk: { low: "منخفض", medium: "متوسط", high: "مرتفع", critical: "حرج" },
  studyPhase: { pre_implementation: "قبل التطبيق", post_implementation: "بعد التطبيق" },
  studyGroup: { control: "ضابطة", intervention: "تدخل" },
  gender: { male: "ذكر", female: "أنثى" },
  status: { new: "جديد", viewed: "تمت المشاهدة", acknowledged: "تم التأكيد", in_progress: "قيد التنفيذ", closed: "مغلق", cancelled: "ملغى" },
  sessionStatus: { scheduled: "مجدولة", active: "نشطة", completed: "مكتملة", cancelled: "ملغاة" }
};

function label(map, value) {
  return map[value] || value || "-";
}

function riskLevelLabel(value) {
  return label(labels.risk, value);
}

function riskTone(value) {
  if (value === "critical" || value === "high" || value === "حرج" || value === "مرتفع") return "danger";
  if (value === "medium" || value === "متوسط") return "warning";
  if (value === "low" || value === "منخفض") return "success";
  return "neutral";
}

function currentRoute() {
  return location.hash.replace("#/", "") || "login";
}

function setRoute(routeId) {
  location.hash = `/${routeId}`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
}

function formatDateTime(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("ar", { dateStyle: "short", timeStyle: "short" });
}

function badge(text, tone = "neutral", critical = false) {
  return `<span class="badge ${tone} ${critical ? "critical" : ""}">${escapeHtml(text)}</span>`;
}

function healthBadge() {
  const connected = appState.health?.connected;
  const text = connected ? "متصل بالخادم" : "غير متصل بالخادم";
  const tone = connected ? "success" : "warning";
  return `<span class="server-status ${tone}" aria-label="حالة الاتصال بالخادم">${text}</span>`;
}

function loadingBlock(text = "جاري تحميل البيانات السريرية...") {
  return `<div class="loading-state" role="status" aria-live="polite"><span class="ecg-loader"></span><span>${text}</span></div><div class="grid cols-3">${[1, 2, 3].map(() => `<div class="card skeleton-card"><div></div><div></div><div></div></div>`).join("")}</div>`;
}

function tableSkeleton(text) {
  return `${loadingBlock(text)}<div class="card table-skeleton"><div class="card-body">${[1, 2, 3, 4].map(() => `<div class="skeleton-row"></div>`).join("")}</div></div>`;
}

function errorBlock(key) {
  const message = appState.errors[key] || "حدث خطأ أثناء الاتصال بالخادم";
  return `<div class="state-message error" role="alert"><strong>تعذر تحميل البيانات</strong><span>${escapeHtml(message)}</span><span>حاول تحديث الصفحة أو تشغيل الخادم المحلي.</span></div>`;
}

function emptyBlock(text) {
  return `<div class="state-message empty"><strong>${escapeHtml(text)}</strong><span>ستظهر البيانات هنا بعد تهيئة قاعدة البيانات أو توفر سجلات جديدة.</span></div>`;
}

function setLoading(key, value) {
  appState.loading[key] = value;
}

async function loadResource(key, loader) {
  setLoading(key, true);
  appState.errors[key] = null;
  render();
  try {
    appState[key] = await loader();
  } catch (error) {
    appState.errors[key] = error.message;
  } finally {
    setLoading(key, false);
    render();
  }
}

async function loadHealth() {
  try {
    appState.health = await api.getHealth();
    appState.errors.health = null;
  } catch (error) {
    appState.health = { connected: false };
    appState.errors.health = error.message;
  }
  render();
}

function ensureDataForRoute(route) {
  if (route.id === "dashboard") {
    if (!appState.researchSummary && !appState.loading.researchSummary) loadResource("researchSummary", api.getResearchSummary.bind(api));
    if (!appState.alerts.length && !appState.loading.alerts) loadResource("alerts", api.getAlerts.bind(api));
    if (!appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
    if (!appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
  }
  if (route.type === "patients" && !appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
  if (route.type === "sessions" && !appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
  if (route.type === "alerts" && !appState.alerts.length && !appState.loading.alerts) loadResource("alerts", api.getAlerts.bind(api));
  if (route.type === "research" && !appState.researchSummary && !appState.loading.researchSummary) loadResource("researchSummary", api.getResearchSummary.bind(api));
}

function renderLogin() {
  app.innerHTML = `
    <main class="auth-page">
      <section class="auth-panel">
        <h1>NEWS2 Hemodialysis Monitoring</h1>
        <p>منصة رصد سريرية وبحثية للكشف المبكر عن التدهور لدى مرضى الغسيل الكلوي باستخدام NEWS2.</p>
      </section>
      <section class="login-card">
        <h2>تسجيل الدخول</h2>
        <p class="subtitle">دخول تجريبي للواجهة. المصادقة الحقيقية ليست ضمن هذه المرحلة.</p>
        <div class="field"><label>البريد الإلكتروني</label><input type="email" value="clinician@karamixlabs.local"></div>
        <div class="field" style="margin-top:14px"><label>كلمة المرور</label><input type="password" value="password"></div>
        <div class="footer-actions">
          <button class="btn primary" onclick="setRoute('dashboard')">دخول المنصة</button>
          <button class="btn">استعادة الوصول</button>
        </div>
      </section>
    </main>`;
}

function renderShell(route) {
  const groups = routes.reduce((acc, item) => {
    acc[item.group] = acc[item.group] || [];
    acc[item.group].push(item);
    return acc;
  }, {});

  app.innerHTML = `
    <div class="shell">
      <aside class="sidebar">
        <div class="brand">
          <h2 class="brand-title"><span class="brand-mark">N2</span><span>منصة NEWS2</span></h2>
          <p class="brand-subtitle">Karamix Labs Clinical Research</p>
        </div>
        ${Object.entries(groups).map(([group, items]) => `
          <nav class="nav-group" aria-label="${group}">
            <div class="nav-group-title">${group}</div>
            ${items.map((item) => `
              <button class="nav-link ${item.id === route.id ? "active" : ""}" onclick="setRoute('${item.id}')">
                <span class="nav-icon">${item.icon}</span><span>${item.label}</span>
              </button>`).join("")}
          </nav>`).join("")}
      </aside>
      <main class="main">
        <header class="topbar">
          <button class="icon-btn mobile-toggle" aria-label="فتح القائمة الجانبية" onclick="document.body.classList.toggle('nav-open')">☰</button>
          <div>
            <h1>${route.label}</h1>
            <p>${subtitles[route.id] || subtitles.default}</p>
          </div>
          <div class="top-actions">
            ${healthBadge()}
            ${badge("RTL", "info")}
            <button class="icon-btn" aria-label="عرض التنبيهات" title="التنبيهات" onclick="setRoute('active-alerts')">!</button>
            <button class="btn" onclick="setRoute('login')">خروج</button>
          </div>
        </header>
        <section class="content">${renderScreen(route)}</section>
      </main>
    </div>`;
}

function renderScreen(route) {
  const renderers = {
    dashboard: renderDashboard,
    patients: renderPatients,
    sessions: renderSessions,
    alerts: renderAlerts,
    research: renderResearch,
    table: () => renderStaticTable(route),
    form: () => renderFormScreen(route),
    profile: renderProfile,
    baseline: renderBaseline,
    vascular: renderVascular,
    details: () => renderDetails(route),
    monitoring: renderMonitoring,
    assessment: renderAssessment,
    trend: renderTrend,
    timeline: () => renderTimeline(route),
    workflow: () => renderWorkflow(route),
    analytics: () => renderAnalytics(route),
    comparison: renderComparison,
    export: renderExport,
    permissions: renderPermissions,
    settings: renderSettings,
    language: renderLanguage
  };
  return (renderers[route.type] || renderDashboard)();
}

function renderDashboard() {
  if (appState.loading.researchSummary && !appState.researchSummary) return loadingBlock("جاري تحميل البيانات السريرية...");
  const summary = appState.researchSummary || {};
  const alerts = appState.alerts || [];
  const criticalAlerts = alerts.filter((item) => item.riskLevel === "critical" || item.severityLevel === "critical").length;
  const latestAlerts = alerts.slice(0, 5).map(alertRow);
  return `
    ${appState.errors.researchSummary ? errorBlock("researchSummary") : ""}
    <div class="dashboard-hero">
      <div class="hero-band">
        <h2>رصد مبكر للتدهور السريري أثناء جلسات الغسيل الكلوي</h2>
        <p>البيانات المعروضة هنا تقرأ من قاعدة البيانات المحلية عبر FastAPI وتبقى الواجهة جاهزة للتوسع المرحلي.</p>
      </div>
      <div class="status-panel">
        ${renderKpi(["حالة الخادم", appState.health?.connected ? "متصل" : "غير متصل", "فحص /health", appState.health?.connected ? "success" : "warning"])}
        ${renderKpi(["تنبيهات حرجة", String(criticalAlerts), "من بيانات التنبيهات", criticalAlerts > 0 ? "danger" : "success"], criticalAlerts > 0)}
      </div>
    </div>
    <div class="grid cols-4">
      ${renderKpi(["إجمالي المرضى", summary.patientsCount ?? appState.patients.length, "من /api/patients", "info"])}
      ${renderKpi(["جلسات الغسيل", summary.sessionsCount ?? appState.dialysisSessions.length, "من /api/dialysis-sessions", "info"])}
      ${renderKpi(["التنبيهات النشطة", summary.activeAlertsCount ?? alerts.length, "من /api/alerts", alerts.length ? "warning" : "success"])}
      ${renderKpi(["متوسط NEWS2", summary.averageNews2 ?? "-", "من الملخص البحثي", (summary.averageNews2 || 0) >= 5 ? "danger" : "success"], (summary.averageNews2 || 0) >= 5)}
    </div>
    <div class="grid cols-2" style="margin-top:16px">
      ${card("منحنى NEWS2 اليوم", renderLineChart("اتجاه NEWS2 تجريبي لحين توفير endpoint للاتجاهات"))}
      ${card("توزيع مؤشرات البحث", renderBarChart([summary.patientsCount || 0, summary.sessionsCount || 0, summary.measurementsCount || 0, summary.alertsCount || 0]))}
    </div>
    <div style="margin-top:16px">
      ${appState.loading.alerts ? tableSkeleton("جاري تحميل التنبيهات...") : card("أحدث التنبيهات", latestAlerts.length ? renderTable(["المعرف", "المريض", "الخطورة", "الحالة", "وقت الإنشاء"], latestAlerts) : emptyBlock("لا توجد تنبيهات نشطة"))}
    </div>`;
}

function renderPatients() {
  if (appState.loading.patients) return tableSkeleton("جاري تحميل قائمة المرضى...");
  if (appState.errors.patients) return errorBlock("patients");
  if (!appState.patients.length) return emptyBlock("لا توجد بيانات مرضى حتى الآن");
  const rows = appState.patients.map((patient) => [
    patient.patientCode,
    patient.age,
    label(labels.gender, patient.gender),
    label(labels.studyPhase, patient.studyPhase),
    label(labels.studyGroup, patient.studyGroup),
    patient.dialysisVintageMonths,
    patient.weeklySessionsCount
  ]);
  return `
    <div class="grid cols-3">
      ${renderKpi(["إجمالي المرضى", appState.patients.length, "بيانات قاعدة محلية", "info"])}
      ${renderKpi(["مرحلة التدخل", appState.patients.filter((p) => p.studyGroup === "intervention").length, "مجموعة الدراسة", "success"])}
      ${renderKpi(["متوسط الجلسات", "3/أسبوع", "من بيانات التهيئة", "info"])}
    </div>
    <div style="margin-top:16px">${card("قائمة المرضى", renderTable(["رمز المريض", "العمر", "الجنس", "مرحلة الدراسة", "مجموعة الدراسة", "مدة الغسيل بالشهور", "جلسات أسبوعية"], rows))}</div>`;
}

function renderSessions() {
  if (appState.loading.dialysisSessions) return tableSkeleton("جاري تحميل جلسات الغسيل المسجلة...");
  if (appState.errors.dialysisSessions) return errorBlock("dialysisSessions");
  if (!appState.dialysisSessions.length) return emptyBlock("لا توجد جلسات غسيل مسجلة");
  const rows = appState.dialysisSessions.map((session) => [
    session.id,
    session.patientCode,
    session.sessionDate,
    session.weekday,
    formatDateTime(session.actualStartTime),
    formatDateTime(session.actualEndTime),
    session.targetUltrafiltration,
    label(labels.sessionStatus, session.sessionStatus)
  ]);
  return card("جلسات الغسيل", renderTable(["المعرف", "رمز المريض", "تاريخ الجلسة", "اليوم", "وقت البدء", "وقت الانتهاء", "السحب المستهدف", "الحالة"], rows));
}

function renderAlerts() {
  if (appState.loading.alerts) return tableSkeleton("جاري تحميل التنبيهات...");
  if (appState.errors.alerts) return errorBlock("alerts");
  if (!appState.alerts.length) return emptyBlock("لا توجد تنبيهات نشطة");
  const critical = appState.alerts.filter((item) => item.riskLevel === "critical").length;
  return `
    <div class="grid cols-3">
      ${renderKpi(["حرجة", critical, "تحتاج تصعيد فوري", critical ? "danger" : "success"], critical > 0)}
      ${renderKpi(["إجمالي التنبيهات", appState.alerts.length, "من قاعدة البيانات", "info"])}
      ${renderKpi(["قيد المتابعة", appState.alerts.filter((a) => a.status !== "closed").length, "غير مغلقة", "warning"])}
    </div>
    <div style="margin-top:16px">${card("التنبيهات النشطة", renderTable(["المعرف", "رمز المريض", "مستوى الخطر", "الشدة", "الحالة", "الأولوية", "سبب التنبيه", "وقت الإنشاء"], appState.alerts.map(alertFullRow)))}</div>`;
}

function renderResearch() {
  if (appState.loading.researchSummary) return loadingBlock("جاري تحميل ملخص البحث...");
  if (appState.errors.researchSummary) return errorBlock("researchSummary");
  if (!appState.researchSummary) return emptyBlock("لا توجد بيانات بحثية حتى الآن");
  const s = appState.researchSummary;
  return `
    <div class="dashboard-hero">
      <div class="hero-band">
        <h2>لوحة بحثية لقياس أثر الرصد المبكر</h2>
        <p>ملخص مباشر من قاعدة البيانات المحلية لقياس جاهزية بيانات الدراسة قبل ربط التحليلات المتقدمة.</p>
      </div>
      <div class="status-panel">
        ${renderKpi(["اكتمال الملخص", "متاح", "من /api/research/summary", "success"])}
        ${renderKpi(["متوسط NEWS2", s.averageNews2 ?? "-", "قابل للتوسع", (s.averageNews2 || 0) >= 5 ? "danger" : "info"], (s.averageNews2 || 0) >= 5)}
      </div>
    </div>
    <div class="grid cols-4">
      ${renderKpi(["إجمالي المرضى", s.patientsCount, "عينة بحثية", "info"])}
      ${renderKpi(["إجمالي الجلسات", s.sessionsCount, "جلسات موثقة", "info"])}
      ${renderKpi(["القياسات", s.measurementsCount, "علامات حيوية", "success"])}
      ${renderKpi(["التنبيهات", s.alertsCount, "سجلات إنذار", s.alertsCount ? "warning" : "success"])}
      ${renderKpi(["أحداث التدهور", s.deteriorationEventsCount, "موثقة", s.deteriorationEventsCount ? "danger" : "success"], s.deteriorationEventsCount > 0)}
      ${renderKpi(["الاستجابات", s.responsesCount, "إجراءات سريرية", "info"])}
      ${renderKpi(["المخرجات", s.outcomesCount, "خلال 24-72 ساعة", "success"])}
      ${renderKpi(["تقييمات NEWS2", s.news2AssessmentsCount, "تقييمات مخزنة", "info"])}
    </div>
    <div class="grid cols-2" style="margin-top:16px">
      ${card("توزيع البيانات", renderBarChart([s.patientsCount, s.sessionsCount, s.measurementsCount, s.news2AssessmentsCount, s.alertsCount, s.outcomesCount]))}
      ${card("مؤشرات البحث", renderTable(["المؤشر", "القيمة", "المصدر"], [["المرضى", s.patientsCount, "patients"], ["الجلسات", s.sessionsCount, "dialysis_sessions"], ["أحداث التدهور", s.deteriorationEventsCount, "clinical_deterioration_events"], ["المخرجات", s.outcomesCount, "clinical_outcomes"]]))}
    </div>`;
}

function alertRow(alert) {
  return [alert.id, alert.patientCode, badge(riskLevelLabel(alert.riskLevel), riskTone(alert.riskLevel), alert.riskLevel === "critical"), label(labels.status, alert.status), formatDateTime(alert.createdAt)];
}

function alertFullRow(alert) {
  return [alert.id, alert.patientCode, badge(riskLevelLabel(alert.riskLevel), riskTone(alert.riskLevel), alert.riskLevel === "critical"), badge(riskLevelLabel(alert.severityLevel), riskTone(alert.severityLevel), alert.severityLevel === "critical"), label(labels.status, alert.status), alert.priority, alert.triggerReason, formatDateTime(alert.createdAt)];
}

function renderKpi(item, critical = false) {
  const [labelText, value, meta, tone] = item;
  return `<div class="card kpi ${critical ? "critical" : ""}"><div class="card-body"><div class="kpi-label">${escapeHtml(labelText)}</div><div class="kpi-value">${escapeHtml(value)}</div><div class="kpi-meta">${badge(meta, tone, critical)}</div></div></div>`;
}

function renderStaticTable(route) {
  const rows = fallbackRows[route.entity] || fallbackRows.events;
  return `<div class="grid cols-3">${renderKpi(["إجمالي السجلات", rows.length, "بيانات مؤقتة حتى إضافة endpoint", "info"])}${renderKpi(["جاهزية التكامل", "جزئية", "سيتم ربطها لاحقا", "warning"])}${renderKpi(["حالة الشاشة", "تعمل", "hash routing محفوظ", "success"])}</div><div style="margin-top:16px">${card(route.label, renderTable(["المعرف", "المرجع", "الوقت", "الحالة", "المؤشر"], rows))}</div>`;
}

function renderTable(headers, rows) {
  return `<div class="table-wrap"><table><thead><tr>${headers.map((h) => `<th>${escapeHtml(h)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${String(cell).startsWith("<span") ? cell : formatCell(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function formatCell(cell) {
  const value = String(cell ?? "-");
  if (["حرج", "مرتفع", "critical", "high"].includes(value)) return badge(value, "danger", value === "حرج" || value === "critical");
  if (["متوسط", "medium", "متابعة", "قيد المتابعة"].includes(value)) return badge(value, "warning");
  if (["منخفض", "low", "مكتمل", "مستقر", "نجاح", "نشط", "مكتملة"].includes(value)) return badge(value, "success");
  return escapeHtml(value);
}

function renderFormScreen(route) {
  const fields = formFields[route.entity] || formFields.patient;
  return card(route.label, `<div class="form-grid">${fields.map((field, index) => `<div class="field ${index === fields.length - 1 ? "full" : ""}"><label>${field}</label>${index === fields.length - 1 ? `<textarea placeholder="${field}"></textarea>` : `<input placeholder="${field}">`}</div>`).join("")}</div><div class="footer-actions"><button class="btn primary">حفظ</button><button class="btn">حفظ كمسودة</button><button class="btn">إلغاء</button></div>`);
}

function renderProfile() {
  const patient = appState.patients[0];
  return `${card("ملخص المريض", `<div class="patient-summary">${[
    ["الرمز", patient?.patientCode || "ANON-P-1001"],
    ["العمر", patient?.age || "58"],
    ["مرحلة الدراسة", patient ? label(labels.studyPhase, patient.studyPhase) : "بعد التطبيق"],
    ["المجموعة", patient ? label(labels.studyGroup, patient.studyGroup) : "تدخل"]
  ].map(([a, b]) => `<div class="summary-cell"><span>${a}</span><strong>${b}</strong></div>`).join("")}</div>`)}
  <div class="grid cols-2" style="margin-top:16px">${card("اتجاه NEWS2", renderLineChart("اتجاه NEWS2 للمريض"))}${card("آخر الجلسات", renderTable(["المعرف", "المريض", "التاريخ", "الحالة"], appState.dialysisSessions.slice(0, 3).map((s) => [s.id, s.patientCode, s.sessionDate, label(labels.sessionStatus, s.sessionStatus)])))}</div>`;
}

function renderBaseline() {
  return `<div class="grid cols-2">${card("القيم المرجعية", renderTable(["المؤشر", "القيمة المرجعية", "آخر قراءة", "التقييم"], [["ضغط الدم", "135/82", "118/70", "انخفاض"], ["النبض", "78", "96", "ارتفاع"], ["تشبع الأكسجين", "96%", "91%", "متابعة"]]))}${card("سياق سريري", renderFormText(["الأمراض المصاحبة", "الأدوية المؤثرة", "ملاحظات خط الأساس"]))}</div>`;
}

function renderVascular() {
  return `<div class="grid cols-3">${renderKpi(["نوع الوصول", "CVC", "قسطرة وريدية مركزية", "warning"])}${renderKpi(["تقييم العدوى", "متوسط", "يحتاج متابعة", "warning"])}${renderKpi(["كفاءة التدفق", "82%", "مقبول", "success"])}</div><div style="margin-top:16px">${card("توثيق الوصول الوعائي", renderFormText(["موقع الوصول", "حالة الجلد", "معدل التدفق", "ملاحظات التمريض"]))}</div>`;
}

function renderDetails(route) {
  const title = route.entity === "alert" ? "تنبيه NEWS2 عالي الخطورة" : route.entity === "event" ? "حدث تدهور سريري" : "جلسة غسيل نشطة";
  return `<div class="split"><div>${card(title, `<div class="patient-summary">${[["المريض", "ANON-P-1002"], ["NEWS2", "16"], ["الوقت", "08:42"], ["الحالة", "مفتوح"]].map(([a, b]) => `<div class="summary-cell"><span>${a}</span><strong>${b}</strong></div>`).join("")}</div><div style="margin-top:18px">${renderLineChart("تفاصيل الاتجاه السريري")}</div>`)}</div><aside>${card("إجراءات مطلوبة", renderActions())}</aside></div>`;
}

function renderMonitoring() {
  return `<div class="grid cols-4">${[["ضغط الدم", "92/58", "انخفاض عن الخط الأساسي", "warning"], ["النبض", "112", "صاعد", "warning"], ["SpO2", "91%", "حرج", "danger"], ["NEWS2", "16", "تصعيد", "danger"]].map((x) => renderKpi(x, x[3] === "danger")).join("")}</div><div class="grid cols-2" style="margin-top:16px">${card("منحنى العلامات الحيوية", renderLineChart("منحنى العلامات الحيوية"))}${card("ملاحظات الجلسة", renderTimelineItems())}</div>`;
}

function renderAssessment() {
  return `<div class="grid cols-2">${card("مكونات NEWS2", renderTable(["المكون", "القراءة", "النقاط", "التقييم"], [["التنفس", "24", "2", "متوسط"], ["الأكسجين", "91%", "3", "حرج"], ["الضغط", "92", "3", "حرج"], ["الوعي", "ارتباك جديد", "3", "حرج"], ["الحرارة", "37.9", "1", "متابعة"]]))}${card("قرار التصعيد", `<div class="kpi-value risk-high">NEWS2 16</div><p class="kpi-meta">تصعيد طبي ومراقبة كل 15 دقيقة.</p>${renderActions()}`)}</div>`;
}

function renderTrend() {
  return `<div class="grid cols-3">${renderKpi(["آخر قراءة", "16", "عالية الخطورة", "danger"], true)}${renderKpi(["أعلى قراءة", "16", "من بيانات التهيئة", "warning"])}${renderKpi(["متوسط النظام", appState.researchSummary?.averageNews2 ?? "-", "من API", "info"])}</div><div style="margin-top:16px">${card("اتجاه NEWS2", renderLineChart("اتجاه NEWS2"))}</div>`;
}

function renderTimeline(route) {
  return `<div class="split"><div>${card(route.label, renderTimelineItems())}</div><aside>${card("مؤشرات زمنية", `${renderKpi(["زمن الاكتشاف", "0 د", "آلي", "success"])}${renderKpi(["زمن التصعيد", "9 د", "ضمن الهدف", "success"])}${renderKpi(["زمن الإغلاق", "قيد المتابعة", "لم يغلق بعد", "warning"])}`)}</aside></div>`;
}

function renderWorkflow(route) {
  return `<div class="grid cols-4">${["اكتشاف", "تأكيد", "تصعيد", "إغلاق"].map((step, index) => renderKpi([step, index < 3 ? "تم" : "نشط", index < 3 ? "موثق" : "بانتظار المخرج", index < 3 ? "success" : "warning"])).join("")}</div><div style="margin-top:16px">${card(route.label, renderTimelineItems())}</div>`;
}

function renderAnalytics(route) {
  return `<div class="grid cols-4">${[
    ["المرضى", appState.researchSummary?.patientsCount ?? "-", "API عند التوفر", "info"],
    ["الجلسات", appState.researchSummary?.sessionsCount ?? "-", "API عند التوفر", "info"],
    ["التنبيهات", appState.researchSummary?.alertsCount ?? "-", "API عند التوفر", "warning"],
    ["المخرجات", appState.researchSummary?.outcomesCount ?? "-", "API عند التوفر", "success"]
  ].map((item) => renderKpi(item)).join("")}</div><div class="grid cols-2" style="margin-top:16px">${card("تحليل الاتجاهات", renderLineChart("تحليل الاتجاهات"))}${card("توزيع المؤشرات", renderBarChart([30, 48, 24, 16, 10]))}</div><div style="margin-top:16px">${card(route.label, renderTable(["المؤشر", "قبل", "بعد", "التحسن"], [["زمن الاستجابة", "18 د", "9 د", "50%"], ["اكتمال التوثيق", "82%", "97%", "15%"], ["التنبيهات المغلقة", "70%", "91%", "21%"]]))}</div>`;
}

function renderComparison() {
  return `<div class="grid cols-3">${renderKpi(["قبل التطبيق", "18 د", "متوسط الاستجابة", "warning"])}${renderKpi(["بعد التطبيق", "9 د", "متوسط الاستجابة", "success"])}${renderKpi(["فرق التحسن", "50%", "دلالة تشغيلية", "success"])}</div><div style="margin-top:16px">${card("مقارنة المؤشرات", renderTable(["المؤشر", "قبل", "بعد", "النتيجة"], [["اكتشاف مبكر", "62%", "88%", "تحسن"], ["تصعيد موثق", "71%", "94%", "تحسن"], ["مخرجات مستقرة", "84%", "91%", "تحسن"]]))}</div>`;
}

function renderExport() {
  return `<div class="grid cols-2">${card("إنشاء تصدير", renderFormText(["نوع البيانات", "الفترة الزمنية", "صيغة الملف", "سبب التصدير"]))}${card("طلبات التصدير", renderTable(["المعرف", "النوع", "الوقت", "الحالة", "المراجع"], [["EX-41", "Dataset", "09:00", "مكتمل", "IRB-2026"], ["EX-42", "Audit", "09:20", "نشط", "ADMIN"]]))}</div>`;
}

function renderPermissions() {
  return card("مصفوفة الصلاحيات", renderTable(["الصلاحية", "طبيب", "تمريض", "باحث", "إدارة"], [["عرض المرضى", "نعم", "نعم", "مقيد", "نعم"], ["تعديل NEWS2", "نعم", "نعم", "لا", "نعم"], ["تصدير البيانات", "مقيد", "لا", "نعم", "نعم"], ["إدارة المستخدمين", "لا", "لا", "لا", "نعم"]]));
}

function renderSettings() {
  return `<div class="grid cols-2">${card("إعدادات الرصد", renderFormText(["فاصل القياس الافتراضي", "عتبة التنبيه العالي", "زمن التصعيد المستهدف", "سياسة الإغلاق"]))}${card("إعدادات السلامة", renderFormText(["تفعيل التدقيق", "سياسة الجلسة", "قواعد الإشعار", "حفظ البيانات"]))}</div>`;
}

function renderLanguage() {
  return `<div class="grid cols-2">${card("اللغة الحالية", `<div class="kpi-value">العربية</div><p class="kpi-meta">الاتجاه الحالي RTL مع قابلية دعم الإنجليزية لاحقا.</p><div class="footer-actions"><button class="btn primary">تطبيق RTL</button><button class="btn">تحضير English</button></div>`)}${card("إعدادات الترجمة", renderFormText(["اللغة الافتراضية", "تنسيق التاريخ", "تنسيق الأرقام", "نطاق الترجمة"]))}</div>`;
}

function renderFormText(fields) {
  return `<div class="form-grid">${fields.map((field, index) => `<div class="field ${index === fields.length - 1 ? "full" : ""}"><label>${field}</label><input placeholder="${field}"></div>`).join("")}</div><div class="footer-actions"><button class="btn primary">حفظ</button><button class="btn">إلغاء</button></div>`;
}

function renderActions() {
  return `<div class="timeline"><div class="timeline-item"><strong>إعادة قياس العلامات الحيوية</strong><span>خلال 15 دقيقة</span></div><div class="timeline-item"><strong>إبلاغ الطبيب المسؤول</strong><span>تصعيد موثق</span></div><div class="timeline-item"><strong>تعديل خطة الجلسة</strong><span>حسب القرار الطبي</span></div></div>`;
}

function renderTimelineItems() {
  const items = [["08:30", "ارتفاع NEWS2 إلى 16", "هبوط ضغط مع نقص أكسجة وارتباك جديد."], ["08:35", "تأكيد تمريضي", "إعادة قياس العلامات الحيوية وتثبيت حالة الوصول الوعائي."], ["08:43", "تصعيد طبي", "تقييم الطبيب وتعديل خطة الجلسة ومعدل السحب."], ["09:05", "تحسن تدريجي", "استمرار المراقبة كل 15 دقيقة."]];
  return `<div class="timeline">${items.map(([time, title, text]) => `<div class="timeline-item"><strong>${time} - ${title}</strong><span>${text}</span></div>`).join("")}</div>`;
}

function renderBarChart(values) {
  const max = Math.max(...values, 1);
  return `<div class="chart" aria-label="مخطط أعمدة للمؤشرات البحثية">${values.map((value) => `<div class="bar" style="height:${Math.max(12, (value / max) * 92)}%"></div>`).join("")}</div>`;
}

function renderLineChart(description = "NEWS2 trend chart") {
  return `<svg class="line-chart" viewBox="0 0 640 230" role="img" aria-label="${escapeHtml(description)}">
    <title>${escapeHtml(description)}</title>
    <line x1="28" y1="200" x2="615" y2="200" stroke="#e2e8f0" />
    <line x1="28" y1="40" x2="28" y2="200" stroke="#e2e8f0" />
    <polyline points="40,170 120,150 205,162 285,118 365,132 445,80 540,96 610,58"></polyline>
    ${[[40,170], [120,150], [205,162], [285,118], [365,132], [445,80], [540,96], [610,58]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="6"></circle>`).join("")}
  </svg>`;
}

function card(title, body) {
  return `<article class="card"><div class="card-header"><h2 class="card-title">${escapeHtml(title)}</h2></div><div class="card-body">${body}</div></article>`;
}

function render() {
  document.body.classList.remove("nav-open");
  const id = currentRoute();
  if (id === "login") {
    renderLogin();
    return;
  }
  const route = routes.find((item) => item.id === id) || routes[0];
  ensureDataForRoute(route);
  renderShell(route);
}

window.setRoute = setRoute;
window.addEventListener("hashchange", render);
loadHealth();
render();
