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
  { id: "create-user", label: "إضافة موظف", group: "الإدارة", icon: "+U", type: "form", entity: "staff" },
  { id: "roles", label: "الأدوار", group: "الإدارة", icon: "RO", type: "table", entity: "roles" },
  { id: "permissions", label: "الصلاحيات", group: "الإدارة", icon: "PR", type: "permissions" },
  { id: "audit-logs", label: "سجلات التدقيق", group: "الإدارة", icon: "AL", type: "table", entity: "audit" },
  { id: "system-settings", label: "إعدادات النظام", group: "الإعدادات", icon: "ST", type: "settings" },
  { id: "language-settings", label: "إعدادات اللغة", group: "الإعدادات", icon: "LG", type: "language" }
];

routes.splice(
  routes.findIndex((route) => route.id === "users"),
  0,
  { id: "study-management", label: "إدارة الدراسة", group: "البحث", icon: "SG", type: "study" },
  { id: "research-protocol", label: "بروتوكول البحث", group: "البحث", icon: "RP", type: "study" },
  { id: "study-timeline", label: "الخط الزمني للدراسة", group: "البحث", icon: "ST", type: "study" },
  { id: "study-readiness", label: "جاهزية الدراسة", group: "البحث", icon: "SR", type: "study" }
);

const NAV_GROUPS = [
  { label: "لوحة التحكم", icon: "D", route: "dashboard" },
  {
    label: "المرضى",
    icon: "P",
    children: [
      { route: "patients" },
      { route: "create-patient", permission: "patients:create" },
      { route: "patient-profile" },
      { route: "patient-baseline" },
      { route: "vascular-access" }
    ]
  },
  {
    label: "الجلسات",
    icon: "S",
    children: [
      { route: "sessions" },
      { route: "create-session" },
      { route: "session-details" },
      { route: "intradialytic-monitoring" }
    ]
  },
  {
    label: "التقييم",
    icon: "VS",
    children: [
      { route: "vital-signs-entry", permission: "measurements:create" },
      { route: "news2-assessment" },
      { route: "news2-trend" },
      { route: "news2-history" }
    ]
  },
  {
    label: "التنبيهات",
    icon: "A",
    children: [
      { route: "active-alerts" },
      { route: "alert-details" },
      { route: "alert-timeline" }
    ]
  },
  {
    label: "الأحداث والاستجابة",
    icon: "E",
    children: [
      { route: "deterioration-events" },
      { route: "event-details" },
      { route: "event-timeline" },
      { route: "medical-response-log" },
      { route: "nursing-response-log" },
      { route: "response-workflow" },
      { route: "response-time-dashboard" },
      { route: "response-analytics" }
    ]
  },
  {
    label: "المآلات",
    icon: "CO",
    children: [
      { route: "clinical-outcomes" },
      { route: "outcome-tracking" },
      { route: "outcome-analytics" }
    ]
  },
  {
    label: "البحث",
    icon: "R",
    children: [
      { route: "research-dashboard" },
      { route: "pre-post-comparison" },
      { route: "study-metrics", permission: "research:analytics" },
      { route: "dataset-statistics", permission: "research:view" },
      { route: "export-center", permission: "research:view" },
      { route: "study-management", permission: "studies:view" },
      { route: "research-protocol", permission: "studies:view" },
      { route: "study-timeline", permission: "studies:view" },
      { route: "study-readiness", permission: "studies:view" }
    ]
  },
  {
    label: "الإدارة",
    icon: "U",
    children: [
      { route: "users", permission: "users:view" },
      { route: "create-user", permission: "users:create" },
      { route: "roles", permission: "rbac:view" },
      { route: "permissions", permission: "rbac:view" },
      { route: "audit-logs", permission: "audit:view" },
      { route: "system-settings", permission: "settings:view" },
      { route: "language-settings", permission: "settings:view" }
    ]
  }
];

const NAV_ROUTE_LABELS = {
  patients: "قائمة المرضى",
  "create-patient": "إضافة مريض",
  "patient-profile": "ملف المريض",
  "patient-baseline": "الخط الأساسي",
  "vascular-access": "الوصول الوعائي",
  sessions: "جلسات الغسيل",
  "create-session": "إنشاء جلسة",
  "session-details": "تفاصيل الجلسة",
  "intradialytic-monitoring": "الرصد أثناء الجلسة",
  "vital-signs-entry": "إدخال العلامات الحيوية",
  "news2-assessment": "تقييم NEWS2",
  "news2-trend": "اتجاه NEWS2",
  "news2-history": "سجل NEWS2",
  "active-alerts": "التنبيهات النشطة",
  "alert-details": "تفاصيل التنبيه",
  "alert-timeline": "تسلسل التنبيه",
  "deterioration-events": "أحداث التدهور",
  "event-details": "تفاصيل الحدث",
  "event-timeline": "تسلسل الحدث",
  "medical-response-log": "سجل الاستجابة الطبية",
  "nursing-response-log": "سجل الاستجابة التمريضية",
  "response-workflow": "مسار الاستجابة",
  "response-time-dashboard": "زمن الاستجابة",
  "response-analytics": "تحليلات الاستجابة",
  "clinical-outcomes": "المآلات السريرية",
  "outcome-tracking": "تتبع المآلات",
  "outcome-analytics": "تحليلات المآلات",
  "research-dashboard": "لوحة البحث",
  "pre-post-comparison": "مقارنة قبل وبعد",
  "study-metrics": "مؤشرات الدراسة",
  "dataset-statistics": "إحصاءات البيانات",
  "export-center": "مركز التصدير",
  "study-management": "إدارة الدراسة",
  "research-protocol": "بروتوكول البحث",
  "study-timeline": "الخط الزمني للدراسة",
  "study-readiness": "جاهزية الدراسة",
  users: "المستخدمون",
  roles: "الأدوار",
  permissions: "الصلاحيات",
  "audit-logs": "سجلات التدقيق",
  "system-settings": "إعدادات النظام",
  "language-settings": "إعدادات اللغة"
};

const appState = {
  health: null,
  patients: [],
  dialysisSessions: [],
  alerts: [],
  researchSummary: null,
  news2Demo: null,
  monitoringMeasurements: [],
  news2Assessments: [],
  monitoringSubmission: null,
  deteriorationEvents: [],
  deteriorationSubmission: null,
  clinicalResponses: [],
  responseTrackingRecords: [],
  responseTrackingSummary: null,
  responseSubmission: null,
  clinicalOutcomes: [],
  outcomeSummary: null,
  outcomeSubmission: null,
  patientSubmission: null,
  researchDatasetRows: [],
  researchDatasetQuality: null,
  researchExportFilters: {},
  researchAnalyticsSummary: null,
  studies: [],
  staffUsers: [],
  selectedStudyId: null,
  selectedPatientId: null,
  patientProfileSearch: "",
  studyReadiness: null,
  studyCenter: null,
  studySubmission: null,
  staffSubmission: null,
  currentUser: null,
  isAuthenticated: false,
  allowDevRole: false,
  loginError: null,
  currentRole: null,
  currentRoleLabel: "مدير النظام",
  permissions: [],
  permissionMatrix: null,
  navCollapsed: localStorage.getItem("news2NavCollapsed") === "true",
  expandedNavGroups: new Set(JSON.parse(localStorage.getItem("news2ExpandedNavGroups") || "[]")),
  loading: {},
  errors: {}
};

const api = {
  async request(path, options = {}) {
    try {
      const headers = { Accept: "application/json", ...(options.headers || {}) };
      if (appState.allowDevRole && appState.currentRole) headers["X-Dev-Role"] = appState.currentRole;
      const response = await fetch(path, { credentials: "include", ...options, headers });
      if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try {
          const payload = await response.json();
          detail = Array.isArray(payload.detail) ? "تأكد من صحة البيانات المدخلة" : payload.detail || detail;
        } catch (error) {
          detail = `HTTP ${response.status}`;
        }
        if (response.status === 401 && !path.startsWith("/api/auth/login") && !path.startsWith("/api/auth/me")) {
          clearAuthState();
          if (currentRoute() !== "login") setRoute("login");
        }
        throw new Error(detail);
      }
      return await response.json();
    } catch (error) {
      throw new Error(error.message || "network_error");
    }
  },
  getHealth() {
    return this.request("/health").then(normalizeHealth);
  },
  getCurrentPermissionContext() {
    return this.request("/api/rbac/me").then(normalizePermissionContext);
  },
  getCurrentUser() {
    return this.request("/api/auth/me").then(normalizePermissionContext);
  },
  login(payload) {
    return this.request("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(normalizePermissionContext);
  },
  logout() {
    return this.request("/api/auth/logout", { method: "POST" });
  },
  getPermissionMatrix() {
    return this.request("/api/rbac/permissions").then(normalizePermissionMatrix);
  },
  getStaffUsers(filters = {}) {
    return this.request(`/api/users${queryString(filters)}`).then((rows) => rows.map(normalizeStaffUser));
  },
  createStaffUser(payload) {
    return this.request("/api/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  updateStaffUserStatus(userId, payload) {
    return this.request(`/api/users/${userId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(normalizeStaffUser);
  },
  getPatients() {
    return this.request("/api/patients").then((rows) => rows.map(normalizePatient));
  },
  createPatient(payload) {
    return this.request("/api/patients", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getDialysisSessions() {
    return this.request("/api/dialysis-sessions").then((rows) => rows.map(normalizeSession));
  },
  getAlerts() {
    return this.request("/api/alerts").then((rows) => rows.map(normalizeAlert));
  },
  getResearchSummary() {
    return this.request("/api/research/summary").then(normalizeResearchSummary);
  },
  calculateNews2(payload) {
    return this.request("/api/news2/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  createMonitoringMeasurement(payload) {
    return this.request("/api/monitoring/measurements", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getMonitoringMeasurements(filters = {}) {
    return this.request(`/api/monitoring/measurements${queryString(filters)}`).then((rows) => rows.map(normalizeMeasurement));
  },
  getNews2Assessments(filters = {}) {
    return this.request(`/api/news2/assessments${queryString(filters)}`).then((rows) => rows.map(normalizeNews2Assessment));
  },
  getDeteriorationEvents(filters = {}) {
    return this.request(`/api/deterioration/events${queryString(filters)}`).then((rows) => rows.map(normalizeDeteriorationEvent));
  },
  createDeteriorationEvent(payload) {
    return this.request("/api/deterioration/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getClinicalResponses(filters = {}) {
    return this.request(`/api/responses${queryString(filters)}`).then((rows) => rows.map(normalizeClinicalResponse));
  },
  getResponseTrackingRecords(filters = {}) {
    return this.request(`/api/response-tracking${queryString(filters)}`).then((rows) => rows.map(normalizeResponseTracking));
  },
  getResponseTrackingSummary(filters = {}) {
    return this.request(`/api/response-tracking/summary${queryString(filters)}`).then(normalizeResponseTrackingSummary);
  },
  createClinicalResponse(payload) {
    return this.request("/api/responses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getClinicalOutcomes(filters = {}) {
    return this.request(`/api/outcomes${queryString(filters)}`).then((rows) => rows.map(normalizeClinicalOutcome));
  },
  getOutcomeSummary() {
    return this.request("/api/outcomes/summary").then(normalizeOutcomeSummary);
  },
  createClinicalOutcome(payload) {
    return this.request("/api/outcomes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  },
  getResearchDataset(filters = {}) {
    return this.request(`/api/research/dataset${queryString({ limit: 25, ...filters })}`).then((rows) => rows.map(normalizeResearchDatasetRow));
  },
  getResearchDatasetQuality(filters = {}) {
    return this.request(`/api/research/dataset/quality${queryString(filters)}`).then(normalizeResearchDatasetQuality);
  },
  getResearchAnalyticsSummary() {
    return this.request("/api/research/analytics/summary").then(normalizeResearchAnalyticsSummary);
  },
  getStudies() {
    return this.request("/api/studies").then((rows) => rows.map(normalizeStudy));
  },
  getStudyReadiness(studyId) {
    return this.request(`/api/studies/${studyId}/readiness`).then(normalizeStudyReadiness);
  },
  createStudy(payload) {
    return this.request("/api/studies", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(normalizeStudy);
  },
  updateStudy(studyId, payload) {
    return this.request(`/api/studies/${studyId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(normalizeStudy);
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

function normalizePermissionContext(data) {
  return {
    id: data?.id || null,
    fullName: data?.full_name || null,
    username: data?.username || null,
    email: data?.email || null,
    role: data?.role || "admin",
    roleLabel: data?.role_label || "مدير النظام",
    permissions: data?.permissions || [],
    isDevContext: data?.is_dev_context === true,
    allowDevRole: data?.allow_dev_role === true
  };
}

function normalizePermissionMatrix(data) {
  return {
    roles: data?.roles || [],
    permissions: data?.permissions || [],
    isDevContext: data?.is_dev_context === true
  };
}

function normalizeStaffUser(row) {
  return {
    id: row.id,
    fullName: row.full_name || "",
    username: row.username || "",
    email: row.email || "",
    phone: row.phone || "",
    department: row.department || "",
    jobTitle: row.job_title || "",
    role: row.role || "",
    isActive: row.is_active === true,
    status: row.status || (row.is_active ? "active" : "inactive"),
    createdAt: row.created_at || null,
    updatedAt: row.updated_at || null
  };
}

function normalizePatient(row) {
  return {
    id: row.id,
    patientCode: row.patient_code || `P-${row.id}`,
    fullName: row.full_name || "",
    age: row.age ?? "-",
    gender: row.gender || "unknown",
    studyPhase: row.study_phase || "unknown",
    studyGroup: row.study_group || "unknown",
    dialysisVintageMonths: row.dialysis_vintage_months ?? "-",
    weeklySessionsCount: row.weekly_sessions_count ?? "-",
    isAnonymized: row.is_anonymized === true
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

function priorityLabel(value) {
  return label({ normal: "عادي", urgent: "عاجل", immediate: "فوري" }, value);
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
    acuteHypotensionCount: row?.acute_hypotension_count ?? 0,
    suspectedSepsisOrFeverCount: row?.suspected_sepsis_or_fever_count ?? 0,
    arrhythmiaCount: row?.arrhythmia_count ?? 0,
    seizuresCount: row?.seizures_count ?? 0,
    reducedConsciousnessCount: row?.reduced_consciousness_count ?? 0,
    responsesCount: row?.responses_count ?? 0,
    clinicalResponsesCount: row?.clinical_responses_count ?? row?.responses_count ?? 0,
    averageResponseDelayMinutes: row?.average_response_delay_minutes ?? null,
    fastestResponseDelayMinutes: row?.fastest_response_delay_minutes ?? null,
    slowestResponseDelayMinutes: row?.slowest_response_delay_minutes ?? null,
    averageTimeToAlertMinutes: row?.average_time_to_alert_minutes ?? null,
    averageTimeToResponseMinutes: row?.average_time_to_response_minutes ?? null,
    fastestResponseMinutes: row?.fastest_response_minutes ?? null,
    slowestResponseMinutes: row?.slowest_response_minutes ?? null,
    alertsWithoutResponseCount: row?.alerts_without_response_count ?? 0,
    outcomesCount: row?.outcomes_count ?? 0,
    totalOutcomes: row?.total_outcomes ?? row?.outcomes_count ?? 0,
    stableCompletedSessionCount: row?.stable_completed_session_count ?? 0,
    sessionStoppedEarlyCount: row?.session_stopped_early_count ?? 0,
    hospitalAdmissionCount: row?.hospital_admission_count ?? 0,
    emergencyDepartmentTransferCount: row?.emergency_department_transfer_count ?? 0,
    icuAdmissionCount: row?.icu_admission_count ?? 0,
    deathCount: row?.death_count ?? 0,
    researchDatasetRows: row?.research_dataset_rows ?? 0,
    datasetQualityScore: row?.dataset_quality_score ?? 0,
    missingOutcomesCount: row?.missing_outcomes_count ?? 0,
    exportReadiness: row?.export_readiness ?? "not_ready",
    averageNews2: row?.average_news2 ?? null
  };
}

function normalizeStudy(row) {
  return {
    id: row.id,
    studyCode: row.study_code || `STUDY-${row.id}`,
    studyTitle: row.study_title || row.title || "-",
    studyDescription: row.study_description || row.description || "",
    principalInvestigator: row.principal_investigator || "-",
    studyDesign: row.study_design || "observational",
    studyPhase: row.study_phase || "-",
    studyStatus: row.study_status || row.status || "draft",
    studyGroupAName: row.study_group_a_name || "-",
    studyGroupBName: row.study_group_b_name || "-",
    baselinePeriodStart: row.baseline_period_start || null,
    baselinePeriodEnd: row.baseline_period_end || null,
    interventionPeriodStart: row.intervention_period_start || null,
    interventionPeriodEnd: row.intervention_period_end || null,
    studyStartDate: row.study_start_date || null,
    studyEndDate: row.study_end_date || null,
    targetSampleSize: row.target_sample_size ?? null,
    inclusionNotes: row.inclusion_notes || "",
    exclusionNotes: row.exclusion_notes || "",
    notes: row.notes || "",
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function normalizeStudyReadiness(row) {
  return {
    studyId: row.study_id,
    readinessScore: row.readiness_score ?? 0,
    missingRequirements: row.missing_requirements || [],
    warnings: row.warnings || [],
    recommendations: row.recommendations || [],
    checks: row.checks || {},
    dashboard: row.dashboard || {},
    protocol: row.protocol || {},
    timeline: row.timeline || {}
  };
}

function normalizeMeasurement(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    dialysisSessionId: row.dialysis_session_id,
    measurementTime: row.measurement_time,
    measurementIntervalMinutes: row.measurement_interval_minutes,
    respiratoryRate: row.respiratory_rate,
    spo2: row.spo2,
    oxygenTherapy: row.oxygen_therapy,
    systolicBp: row.systolic_bp,
    diastolicBp: row.diastolic_bp,
    pulseRate: row.pulse_rate,
    temperature: row.temperature,
    consciousnessLevel: row.consciousness_level,
    confusionStatus: row.confusion_status,
    recordedByUserId: row.recorded_by_user_id,
    createdAt: row.created_at
  };
}

function normalizeNews2Assessment(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    dialysisSessionId: row.dialysis_session_id,
    measurementId: row.intradialytic_measurement_id,
    respiratoryScore: row.respiratory_score,
    spo2Score: row.spo2_score,
    oxygenScore: row.oxygen_score,
    systolicBpScore: row.systolic_bp_score,
    pulseScore: row.pulse_score,
    temperatureScore: row.temperature_score,
    consciousnessScore: row.consciousness_score,
    totalScore: row.total_score,
    riskLevel: row.risk_level,
    alertRequired: row.alert_required,
    singleParameterTrigger: row.single_parameter_trigger,
    triggerReason: row.trigger_reason,
    createdAt: row.created_at
  };
}

function normalizeDeteriorationEvent(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    dialysisSessionId: row.dialysis_session_id,
    sessionDate: row.session_date,
    news2AssessmentId: row.news2_assessment_id,
    news2TotalScore: row.news2_total_score,
    alertId: row.alert_id,
    alertStatus: row.alert_status,
    riskLevel: row.risk_level,
    deteriorationTime: row.deterioration_time,
    timeFromSessionStartMinutes: row.time_from_session_start_minutes,
    deteriorationType: row.deterioration_type,
    triggeringNews2Score: row.triggering_news2_score,
    description: row.description,
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function normalizeClinicalResponse(row) {
  return {
    id: row.id,
    clinicalDeteriorationEventId: row.clinical_deterioration_event_id,
    alertId: row.alert_id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    dialysisSessionId: row.dialysis_session_id,
    sessionDate: row.session_date,
    news2TotalScore: row.news2_total_score,
    deteriorationType: row.deterioration_type,
    digitalAlertTime: row.digital_alert_time,
    actualResponseStartTime: row.actual_response_start_time,
    responseDelayMinutes: row.response_delay_minutes,
    patientActions: row.patient_actions || [],
    vascularAccessActions: row.vascular_access_actions || [],
    respondedByUserId: row.responded_by_user_id,
    notes: row.notes,
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function normalizeResponseTracking(row) {
  return {
    id: row.id,
    alertId: row.alert_id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    dialysisSessionId: row.dialysis_session_id,
    sessionDate: row.session_date,
    news2AssessmentId: row.news2_assessment_id,
    news2TotalScore: row.news2_total_score,
    riskLevel: row.risk_level,
    clinicalDeteriorationEventId: row.clinical_deterioration_event_id,
    deteriorationType: row.deterioration_type,
    deteriorationEventCreatedAt: row.deterioration_event_created_at,
    vitalSignsRecordedAt: row.vital_signs_recorded_at,
    alertCreatedAt: row.alert_created_at,
    alertViewedAt: row.alert_viewed_at,
    actualResponseStartTime: row.actual_response_start_time,
    clinicalActionAt: row.clinical_action_at,
    alertClosedAt: row.alert_closed_at,
    timeToAlertMinutes: row.time_to_alert_minutes,
    timeToViewMinutes: row.time_to_view_minutes,
    timeToResponseMinutes: row.time_to_response_minutes,
    timeToActionMinutes: row.time_to_action_minutes,
    totalResponseTimeMinutes: row.total_response_time_minutes,
    warnings: row.warnings || [],
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function normalizeResponseTrackingSummary(row) {
  return {
    recordsCount: row?.records_count ?? 0,
    averageTimeToAlertMinutes: row?.average_time_to_alert_minutes ?? null,
    averageTimeToViewMinutes: row?.average_time_to_view_minutes ?? null,
    averageTimeToResponseMinutes: row?.average_time_to_response_minutes ?? null,
    averageTimeToActionMinutes: row?.average_time_to_action_minutes ?? null,
    averageTotalResponseTimeMinutes: row?.average_total_response_time_minutes ?? null,
    fastestResponseMinutes: row?.fastest_response_minutes ?? null,
    slowestResponseMinutes: row?.slowest_response_minutes ?? null,
    alertsWithoutResponseCount: row?.alerts_without_response_count ?? 0
  };
}

function normalizeClinicalOutcome(row) {
  return {
    id: row.id,
    patientId: row.patient_id,
    patientCode: row.patient_code || `ID ${row.patient_id}`,
    dialysisSessionId: row.dialysis_session_id,
    sessionDate: row.session_date,
    clinicalDeteriorationEventId: row.clinical_deterioration_event_id,
    alertId: row.alert_id,
    news2AssessmentId: row.news2_assessment_id,
    news2TotalScore: row.news2_total_score,
    deteriorationType: row.deterioration_type,
    outcomeType: row.outcome_type,
    outcomeRecordedAt: row.outcome_recorded_at,
    outcomeWindowHours: row.outcome_window_hours,
    description: row.description,
    recordedByUserId: row.recorded_by_user_id,
    createdAt: row.created_at
  };
}

function normalizeOutcomeSummary(row) {
  return {
    totalOutcomes: row?.total_outcomes ?? 0,
    stableCompletedSessionCount: row?.stable_completed_session_count ?? 0,
    sessionStoppedEarlyCount: row?.session_stopped_early_count ?? 0,
    hospitalAdmissionCount: row?.hospital_admission_count ?? 0,
    emergencyDepartmentTransferCount: row?.emergency_department_transfer_count ?? 0,
    icuAdmissionCount: row?.icu_admission_count ?? 0,
    deathCount: row?.death_count ?? 0
  };
}

function normalizeResearchDatasetRow(row) {
  return {
    patientCode: row.patient_code || "-",
    sessionDate: row.session_date || "-",
    measurementTime: row.measurement_time || null,
    news2TotalScore: row.news2_total_score ?? "-",
    riskLevel: row.risk_level || "-",
    alertCreated: Boolean(row.alert_created),
    deteriorationType: row.deterioration_type || "-",
    responseDelayMinutes: row.response_delay_minutes ?? null,
    outcomeType: row.outcome_type || "-",
    studyPhase: row.study_phase || "-",
    studyGroup: row.study_group || "-"
  };
}

function normalizeResearchDatasetQuality(row) {
  return {
    qualityScore: row?.quality_score ?? 0,
    totalRows: row?.total_rows ?? 0,
    issuesCount: row?.issues_count ?? 0,
    issuesByType: row?.issues_by_type || {},
    warnings: row?.warnings || [],
    statistics: row?.statistics || {}
  };
}

function normalizeResearchAnalyticsSummary(row) {
  return {
    kpis: row?.kpis || {},
    news2Distribution: row?.news2_distribution || [],
    riskLevelDistribution: row?.risk_level_distribution || [],
    outcomeAnalysis: row?.outcome_analysis || {},
    responseTimeAnalysis: row?.response_time_analysis || {},
    deteriorationAnalysis: row?.deterioration_analysis || [],
    groupComparison: row?.group_comparison || {}
  };
}

function queryString(filters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") params.set(key, value);
  });
  const value = params.toString();
  return value ? `?${value}` : "";
}

const labels = {
  risk: { low: "منخفض", medium: "متوسط", high: "مرتفع", critical: "حرج" },
  studyPhase: { pre_implementation: "قبل التطبيق", post_implementation: "بعد التطبيق" },
  studyGroup: { control: "ضابطة", intervention: "تدخل" },
  gender: { male: "ذكر", female: "أنثى" },
  status: { new: "جديد", viewed: "تمت المشاهدة", acknowledged: "تم التأكيد", in_progress: "قيد المعالجة", closed: "مغلق", cancelled: "ملغى" },
  sessionStatus: { scheduled: "مجدولة", active: "نشطة", completed: "مكتملة", cancelled: "ملغاة" },
  consciousness: { alert: "يقظ", voice: "يستجيب للصوت", pain: "يستجيب للألم", unresponsive: "لا يستجيب", new_confusion: "ارتباك حديث" },
  trigger: {
    "NEWS2 total score below alert threshold": "درجة NEWS2 أقل من عتبة التنبيه",
    "NEWS2 total score requires clinical alert": "درجة NEWS2 تتطلب تنبيها سريريا",
    "Single parameter scored 3": "مؤشر واحد سجل 3 نقاط"
  },
  deteriorationType: {
    acute_hypotension: "هبوط ضغط حاد",
    suspected_sepsis_or_fever: "اشتباه إنتان / حرارة",
    arrhythmia: "اضطراب نظم القلب",
    seizures: "تشنجات",
    reduced_consciousness: "انخفاض الوعي",
    other: "أخرى"
  },
  patientAction: {
    stop_ultrafiltration: "إيقاف سحب السوائل",
    give_fluids: "إعطاء محاليل",
    give_oxygen: "إعطاء أوكسجين",
    position_adjustment: "تعديل وضعية المريض",
    medication_given: "إعطاء دواء",
    doctor_called: "استدعاء الطبيب",
    transfer_prepared: "تجهيز النقل",
    other: "أخرى"
  },
  vascularAction: {
    check_flow: "فحص التدفق",
    inspect_access_site: "فحص موضع الوصلة",
    blood_culture_from_catheter: "سحب مزرعة دم من القسطرة",
    catheter_evaluation: "تقييم القسطرة",
    other: "أخرى"
  },
  outcomeType: {
    stable_completed_session: "استقرار واستكمال الجلسة",
    session_stopped_early: "إيقاف الجلسة مبكرا",
    hospital_admission: "إدخال إلى المستشفى",
    emergency_department_transfer: "تحويل إلى الطوارئ",
    icu_admission: "دخول العناية المركزة",
    death: "وفاة"
  },
  role: {
    admin: "مدير النظام",
    technical_admin: "تقني النظام",
    doctor: "طبيب",
    on_call_doctor: "طبيب مناوب",
    nurse: "ممرض/ممرضة",
    researcher: "باحث"
  }
};

const PERMISSION_RESOURCE_LABELS = {
  patients: "المرضى",
  sessions: "جلسات الغسيل",
  measurements: "العلامات الحيوية",
  news2: "تقييم NEWS2",
  alerts: "التنبيهات",
  deterioration: "أحداث التدهور",
  responses: "الاستجابات",
  outcomes: "المآلات السريرية",
  research: "البحث",
  studies: "الدراسة",
  users: "المستخدمون",
  staff: "الموظفون",
  rbac: "الأدوار والصلاحيات",
  audit: "سجلات التدقيق",
  settings: "الإعدادات"
};

const PERMISSION_ACTION_LABELS = {
  view: "عرض",
  create: "إضافة",
  update: "تعديل",
  manage: "إدارة",
  disable: "إيقاف",
  analytics: "تحليلات",
  export: "تصدير"
};

labels.studyStatus = {
  draft: "مسودة",
  active: "نشطة",
  paused: "متوقفة مؤقتا",
  completed: "مكتملة",
  archived: "مؤرشفة"
};

labels.studyDesign = {
  observational: "رصدية",
  prospective: "استباقية",
  retrospective: "استرجاعية",
  before_after: "قبل وبعد",
  cohort: "أترابية",
  pilot: "تجريبية أولية"
};

labels.readinessCheck = {
  study_defined: "تعريف الدراسة",
  dataset_available: "Dataset جاهز",
  analytics_available: "التحليلات جاهزة",
  exports_available: "التصدير جاهز",
  outcomes_available: "المآلات جاهزة",
  response_tracking_available: "تتبع الاستجابة جاهز"
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

function hasPermission(permission) {
  return (appState.permissions || []).includes(permission);
}

function routeById(routeId) {
  return routes.find((item) => item.id === routeId);
}

function navItemVisible(item) {
  if (!item.permission) return true;
  return hasPermission(item.permission);
}

function visibleNavGroups() {
  return NAV_GROUPS.map((group) => {
    const children = (group.children || []).filter(navItemVisible).map((child) => ({ ...child, routeMeta: routeById(child.route) })).filter((child) => child.routeMeta);
    return { ...group, children, routeMeta: group.route ? routeById(group.route) : null };
  }).filter((group) => {
    if (group.route) return navItemVisible(group) && group.routeMeta;
    return group.children.length > 0;
  });
}

function activeNavGroup(routeId) {
  return NAV_GROUPS.find((group) => group.route === routeId || (group.children || []).some((child) => child.route === routeId));
}

function groupExpanded(group, routeId) {
  if (appState.navCollapsed) return false;
  if (group.route === routeId || (group.children || []).some((child) => child.route === routeId)) return true;
  return appState.expandedNavGroups.has(group.label);
}

function toggleNavGroup(label) {
  if (appState.expandedNavGroups.has(label)) appState.expandedNavGroups.delete(label);
  else appState.expandedNavGroups.add(label);
  localStorage.setItem("news2ExpandedNavGroups", JSON.stringify([...appState.expandedNavGroups]));
  render();
}

const MOBILE_NAV_QUERY = "(max-width: 1120px)";

function isMobileNavMode() {
  return window.matchMedia(MOBILE_NAV_QUERY).matches;
}

function applySidebarState() {
  document.body.classList.toggle("nav-collapsed", appState.navCollapsed);
  const menuButton = document.querySelector(".menu-toggle");
  if (menuButton) {
    const expanded = isMobileNavMode() ? document.body.classList.contains("nav-open") : !appState.navCollapsed;
    menuButton.setAttribute("aria-expanded", String(expanded));
  }
}

function openSidebar() {
  if (isMobileNavMode()) {
    document.body.classList.add("nav-open");
    applySidebarState();
    return;
  }
  if (!appState.navCollapsed) {
    applySidebarState();
    return;
  }
  appState.navCollapsed = false;
  localStorage.setItem("news2NavCollapsed", String(appState.navCollapsed));
  render();
}

function closeSidebar() {
  if (isMobileNavMode()) {
    document.body.classList.remove("nav-open");
    applySidebarState();
    return;
  }
  if (appState.navCollapsed) {
    applySidebarState();
    return;
  }
  appState.navCollapsed = true;
  localStorage.setItem("news2NavCollapsed", String(appState.navCollapsed));
  render();
}

function toggleSidebar() {
  if (isMobileNavMode()) {
    if (document.body.classList.contains("nav-open")) closeSidebar();
    else openSidebar();
    return;
  }
  appState.navCollapsed = !appState.navCollapsed;
  localStorage.setItem("news2NavCollapsed", String(appState.navCollapsed));
  render();
}

function closeMobileNav() {
  document.body.classList.remove("nav-open");
  applySidebarState();
}

function parseCurrentRoute() {
  const rawRoute = location.hash.replace(/^#\/?/, "") || "login";
  const [pathPart, queryPart = ""] = rawRoute.split("?");
  const pathSegments = pathPart.split("/").filter(Boolean);
  const params = new URLSearchParams(queryPart);
  if (pathSegments[0] === "patient-profile" && pathSegments[1] && !params.has("patient_id")) {
    params.set("patient_id", pathSegments[1]);
  }
  return { id: pathSegments[0] || "login", params };
}

function currentRoute() {
  return parseCurrentRoute().id;
}

function selectedPatientIdFromRoute(params = parseCurrentRoute().params) {
  const patientId = Number(params.get("patient_id"));
  return Number.isInteger(patientId) && patientId > 0 ? patientId : null;
}

function setRoute(routeId) {
  location.hash = `/${routeId}`;
  closeMobileNav();
}

function handleActionKey(event, routeId) {
  if (event.key !== "Enter" && event.key !== " ") return;
  event.preventDefault();
  setRoute(routeId);
}

function selectPatientProfile(patientId) {
  const normalizedId = Number(patientId);
  if (!Number.isInteger(normalizedId) || normalizedId <= 0) return;
  appState.selectedPatientId = normalizedId;
  setRoute(`patient-profile?patient_id=${normalizedId}`);
}

function showPatientProfileSelector() {
  appState.selectedPatientId = null;
  appState.patientProfileSearch = "";
  setRoute("patient-profile");
}

function changePatientProfileSearch(value) {
  appState.patientProfileSearch = String(value || "");
  render();
}

function filterPatientProfileSelector(value) {
  appState.patientProfileSearch = String(value || "");
  const query = appState.patientProfileSearch.trim().toLowerCase();
  const rows = document.querySelectorAll("[data-patient-search-row]");
  let visibleRows = 0;
  rows.forEach((row) => {
    const visible = !query || String(row.dataset.search || "").includes(query);
    row.style.display = visible ? "" : "none";
    if (visible) visibleRows += 1;
  });
  const emptyState = document.getElementById("patientSelectorEmpty");
  if (emptyState) emptyState.style.display = visibleRows ? "none" : "";
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

function renderDevRoleSwitcher() {
  if (!appState.allowDevRole) return "";
  const roles = [
    ["admin", "مدير"],
    ["technical_admin", "تقني النظام"],
    ["doctor", "طبيب"],
    ["on_call_doctor", "مناوب"],
    ["nurse", "تمريض"],
    ["researcher", "باحث"]
  ];
  return `<label class="dev-role-switcher" title="وضع الدور التجريبي مؤقت حتى مرحلة المصادقة"><span>الدور</span><select onchange="changeDevRole(this.value)">${roles.map(([value, text]) => `<option value="${value}" ${appState.currentRole === value ? "selected" : ""}>${text}</option>`).join("")}</select></label>`;
}

function setLoading(key, value) {
  appState.loading[key] = value;
}

function renderCurrentUserBadge() {
  const user = appState.currentUser || {};
  const name = user.fullName || user.username || user.email || "Authenticated user";
  return `<div class="current-user-badge"><span>${escapeHtml(name)}</span><strong>${escapeHtml(appState.currentRoleLabel || "")}</strong></div>`;
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

function clearAuthState() {
  appState.currentUser = null;
  appState.isAuthenticated = false;
  appState.allowDevRole = false;
  appState.currentRole = null;
  appState.currentRoleLabel = "ظ…ط¯ظٹط± ط§ظ„ظ†ط¸ط§ظ…";
  appState.permissions = [];
  appState.permissionMatrix = null;
}

async function loadAuthContext() {
  try {
    const context = await api.getCurrentUser();
    appState.currentUser = context;
    appState.isAuthenticated = true;
    appState.allowDevRole = context.allowDevRole === true;
    appState.currentRole = context.role;
    appState.currentRoleLabel = context.roleLabel;
    appState.permissions = context.permissions;
    appState.errors.rbac = null;
  } catch (error) {
    clearAuthState();
    appState.errors.rbac = error.message;
    render();
    return;
  }
  if (hasPermission("rbac:view")) {
    try {
      appState.permissionMatrix = await api.getPermissionMatrix();
    } catch (error) {
      appState.errors.permissionMatrix = error.message;
    }
  }
  render();
}

async function loadStudyCenter() {
  const studies = await api.getStudies();
  appState.studies = studies;
  const selected = studies.find((study) => study.id === appState.selectedStudyId) || studies[0];
  appState.selectedStudyId = selected?.id || null;
  appState.studyReadiness = selected ? await api.getStudyReadiness(selected.id) : null;
  return { loaded: true, studiesCount: studies.length, selectedStudyId: appState.selectedStudyId };
}

function patientErrorMessage(message) {
  if (String(message || "").includes("patient_code already exists")) return "رقم الملف مستخدم مسبقا";
  if (String(message || "").includes("Permission denied")) return "ليست لديك صلاحية إضافة مريض";
  return message || "تعذر حفظ المريض";
}

function patientPayloadFromForm(form) {
  const data = new FormData(form);
  const ageValue = data.get("age") || ageFromBirthDate(data.get("birth_date"));
  return compactObject({
    patient_code: data.get("patient_code"),
    full_name: data.get("full_name"),
    age: ageValue !== "" && ageValue !== null ? Number(ageValue) : null,
    gender: data.get("gender"),
    target_dry_weight: data.get("target_dry_weight") ? Number(data.get("target_dry_weight")) : null,
    dialysis_start_date: data.get("dialysis_start_date") || null,
    weekly_sessions_count: data.get("weekly_sessions_count") ? Number(data.get("weekly_sessions_count")) : 3,
    comorbidities: data.get("comorbidities") || null,
    baseline_functional_status: data.get("baseline_functional_status") || null,
    study_phase: data.get("study_phase") || "post_implementation",
    study_group: data.get("study_group") || "intervention",
    is_anonymized: true
  });
}

function ageFromBirthDate(value) {
  if (!value) return "";
  const birthDate = new Date(value);
  if (Number.isNaN(birthDate.getTime())) return "";
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDelta = today.getMonth() - birthDate.getMonth();
  if (monthDelta < 0 || (monthDelta === 0 && today.getDate() < birthDate.getDate())) age -= 1;
  return age >= 0 ? age : "";
}

function compactObject(value) {
  return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== "" && item !== null && item !== undefined));
}

function ensureDataForRoute(route) {
  if (route.id === "dashboard") {
    if (!appState.researchSummary && !appState.loading.researchSummary) loadResource("researchSummary", api.getResearchSummary.bind(api));
    if (!appState.alerts.length && !appState.loading.alerts) loadResource("alerts", api.getAlerts.bind(api));
    if (!appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
    if (!appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
  }
  if (route.type === "patients" && !appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
  if (route.id === "users" && !appState.staffUsers.length && !appState.loading.staffUsers) loadResource("staffUsers", api.getStaffUsers.bind(api));
  if (route.type === "profile") {
    if (!appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
    if (!appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
    if (!appState.news2Assessments.length && !appState.loading.news2Assessments) loadResource("news2Assessments", api.getNews2Assessments.bind(api));
    if (!appState.alerts.length && !appState.loading.alerts) loadResource("alerts", api.getAlerts.bind(api));
    if (!appState.deteriorationEvents.length && !appState.loading.deteriorationEvents) loadResource("deteriorationEvents", api.getDeteriorationEvents.bind(api));
    if (!appState.clinicalOutcomes.length && !appState.loading.clinicalOutcomes) loadResource("clinicalOutcomes", api.getClinicalOutcomes.bind(api));
  }
  if (route.type === "sessions" && !appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
  if (route.type === "alerts" && !appState.alerts.length && !appState.loading.alerts) loadResource("alerts", api.getAlerts.bind(api));
  if (route.type === "research" && !appState.researchSummary && !appState.loading.researchSummary) loadResource("researchSummary", api.getResearchSummary.bind(api));
  if (route.id === "vital-signs-entry") {
    if (!appState.patients.length && !appState.loading.patients) loadResource("patients", api.getPatients.bind(api));
    if (!appState.dialysisSessions.length && !appState.loading.dialysisSessions) loadResource("dialysisSessions", api.getDialysisSessions.bind(api));
  }
  if (route.id === "intradialytic-monitoring" && !appState.monitoringMeasurements.length && !appState.loading.monitoringMeasurements) loadResource("monitoringMeasurements", api.getMonitoringMeasurements.bind(api));
  if (route.id === "news2-history" && !appState.news2Assessments.length && !appState.loading.news2Assessments) loadResource("news2Assessments", api.getNews2Assessments.bind(api));
  if (["deterioration-events", "event-details", "event-timeline"].includes(route.id) && !appState.deteriorationEvents.length && !appState.loading.deteriorationEvents) loadResource("deteriorationEvents", api.getDeteriorationEvents.bind(api));
  if (["medical-response-log", "nursing-response-log", "response-workflow"].includes(route.id) && !appState.clinicalResponses.length && !appState.loading.clinicalResponses) loadResource("clinicalResponses", api.getClinicalResponses.bind(api));
  if (["response-time-dashboard", "response-analytics", "response-workflow"].includes(route.id)) {
    if (!appState.responseTrackingRecords.length && !appState.loading.responseTrackingRecords) loadResource("responseTrackingRecords", api.getResponseTrackingRecords.bind(api));
    if (!appState.responseTrackingSummary && !appState.loading.responseTrackingSummary) loadResource("responseTrackingSummary", api.getResponseTrackingSummary.bind(api));
  }
  if (["clinical-outcomes", "outcome-tracking", "outcome-analytics"].includes(route.id)) {
    if (!appState.clinicalOutcomes.length && !appState.loading.clinicalOutcomes) loadResource("clinicalOutcomes", api.getClinicalOutcomes.bind(api));
    if (!appState.outcomeSummary && !appState.loading.outcomeSummary) loadResource("outcomeSummary", api.getOutcomeSummary.bind(api));
    if (!appState.deteriorationEvents.length && !appState.loading.deteriorationEvents) loadResource("deteriorationEvents", api.getDeteriorationEvents.bind(api));
  }
  if (["export-center", "dataset-statistics"].includes(route.id)) {
    if (!appState.researchDatasetRows.length && !appState.loading.researchDatasetRows) loadResource("researchDatasetRows", () => api.getResearchDataset(appState.researchExportFilters));
    if (!appState.researchDatasetQuality && !appState.loading.researchDatasetQuality) loadResource("researchDatasetQuality", () => api.getResearchDatasetQuality(appState.researchExportFilters));
  }
  if (route.id === "study-metrics" && !appState.researchAnalyticsSummary && !appState.loading.researchAnalyticsSummary) {
    loadResource("researchAnalyticsSummary", api.getResearchAnalyticsSummary.bind(api));
  }
  if (route.type === "study" && !appState.studyCenter && !appState.loading.studyCenter) {
    loadResource("studyCenter", loadStudyCenter);
  }
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
        <p class="subtitle">أدخل اسم المستخدم أو البريد الإلكتروني وكلمة المرور للوصول إلى المنصة.</p>
        <form onsubmit="submitLogin(event)">
          <div class="field"><label>اسم المستخدم أو البريد الإلكتروني</label><input name="username_or_email" autocomplete="username" required></div>
          <div class="field" style="margin-top:14px"><label>كلمة المرور</label><input name="password" type="password" autocomplete="current-password" required minlength="8"></div>
          ${appState.loginError ? `<div class="state-message error" role="alert"><strong>${escapeHtml(appState.loginError)}</strong></div>` : ""}
          <div class="footer-actions">
            <button class="btn primary" type="submit">دخول المنصة</button>
          </div>
        </form>
      </section>
    </main>`;
  return;
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
  const navGroups = visibleNavGroups();
  const activeGroup = activeNavGroup(route.id);
  if (activeGroup && !appState.expandedNavGroups.has(activeGroup.label)) {
    appState.expandedNavGroups.add(activeGroup.label);
    localStorage.setItem("news2ExpandedNavGroups", JSON.stringify([...appState.expandedNavGroups]));
  }
  applySidebarState();
  app.innerHTML = `
    <div class="shell" id="app-shell">
      <div class="nav-scrim" onclick="closeSidebar()" aria-hidden="true"></div>
      <aside class="sidebar" id="app-sidebar" aria-label="القائمة الرئيسية">
        <div class="brand">
          <h2 class="brand-title"><span class="brand-mark">N2</span><span class="brand-text">منصة NEWS2</span></h2>
          <p class="brand-subtitle">Karamix Labs Clinical Research</p>
          <button class="icon-btn sidebar-close" id="sidebarCloseButton" aria-label="إغلاق القائمة" onclick="closeSidebar()">×</button>
        </div>
        <nav class="nav-list" aria-label="التنقل الرئيسي">
          ${navGroups.map((group) => renderNavGroup(group, route.id)).join("")}
        </nav>
      </aside>
      <main class="main">
        <header class="topbar">
          <button class="icon-btn menu-toggle" aria-label="فتح أو طي القائمة الجانبية" aria-controls="app-sidebar" aria-expanded="${!appState.navCollapsed}" onclick="toggleSidebar()">☰</button>
          <div>
            <h1>${route.label}</h1>
            <p>${subtitles[route.id] || subtitles.default}</p>
          </div>
          <div class="top-actions">
            ${healthBadge()}
            ${renderCurrentUserBadge()}${renderDevRoleSwitcher()}
            ${badge("RTL", "info")}
            <button class="icon-btn" aria-label="عرض التنبيهات" title="التنبيهات" onclick="setRoute('active-alerts')">!</button>
            <button class="btn" onclick="logout()">خروج</button>
          </div>
        </header>
        <section class="content">${renderScreen(route)}</section>
      </main>
    </div>`;
  applySidebarState();
}

function renderNavGroup(group, routeId) {
  const isDirect = Boolean(group.route);
  const active = group.route === routeId || (group.children || []).some((child) => child.route === routeId);
  if (isDirect) {
    const meta = group.routeMeta || routeById(group.route);
    return `<button class="nav-link nav-parent ${active ? "active" : ""}" title="${escapeHtml(group.label)}" onclick="setRoute('${group.route}')"><span class="nav-icon">${escapeHtml(group.icon)}</span><span class="nav-label">${escapeHtml(group.label)}</span></button>`;
  }
  const expanded = groupExpanded(group, routeId);
  return `<div class="nav-section ${active ? "active" : ""} ${expanded ? "expanded" : ""}">
    <button class="nav-link nav-parent ${active ? "active" : ""}" aria-expanded="${expanded}" title="${escapeHtml(group.label)}" onclick="toggleNavGroup('${escapeHtml(group.label)}')">
      <span class="nav-icon">${escapeHtml(group.icon)}</span><span class="nav-label">${escapeHtml(group.label)}</span><span class="nav-caret">▾</span>
    </button>
    <div class="nav-children">
      ${(group.children || []).map((child) => renderNavChild(child, routeId)).join("")}
    </div>
  </div>`;
}

function renderNavChild(child, routeId) {
  const meta = child.routeMeta || routeById(child.route);
  if (!meta) return "";
  const labelText = child.label || NAV_ROUTE_LABELS[child.route] || meta.label;
  return `<button class="nav-link nav-child ${child.route === routeId ? "active" : ""}" onclick="setRoute('${child.route}')"><span class="nav-icon">${escapeHtml(meta.icon)}</span><span class="nav-label">${escapeHtml(labelText)}</span></button>`;
}

function renderShellLegacy(route) {
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
            ${renderCurrentUserBadge()}${renderDevRoleSwitcher()}
            ${badge("RTL", "info")}
            <button class="icon-btn" aria-label="عرض التنبيهات" title="التنبيهات" onclick="setRoute('active-alerts')">!</button>
            <button class="btn" onclick="logout()">خروج</button>
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
    study: () => renderStudyCenter(route),
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
  const activeAlerts = alerts.filter((item) => !["closed", "cancelled"].includes(item.status)).length;
  const highRiskAlerts = applyAlertRouteFilter(alerts, { highRisk: true }).length;
  const mediumRiskAlerts = alerts.filter((item) => item.riskLevel === "medium" || item.severityLevel === "medium").length;
  const closedAlerts = alerts.filter((item) => item.status === "closed").length;
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
        ${renderActionKpi(["تنبيهات عالية الخطورة", String(highRiskAlerts), "من بيانات التنبيهات", highRiskAlerts > 0 ? "danger" : "success"], "active-alerts?risk_level=high", "عرض التنبيهات عالية الخطورة", highRiskAlerts > 0)}
      </div>
    </div>
    <div class="grid cols-4">
      ${renderActionKpi(["إجمالي المرضى", summary.patientsCount ?? appState.patients.length, "من /api/patients", "info"], "patients", "عرض قائمة المرضى")}
      ${renderActionKpi(["التنبيهات النشطة", activeAlerts, "من /api/alerts", activeAlerts ? "warning" : "success"], "active-alerts", "عرض التنبيهات النشطة")}
      ${renderKpi(["تنبيهات متوسطة", mediumRiskAlerts, "فرز سريري", mediumRiskAlerts ? "warning" : "success"])}
      ${renderKpi(["تنبيهات مغلقة", closedAlerts, "مكتملة", "success"])}
      ${renderActionKpi(["أحداث التدهور", summary.deteriorationEventsCount ?? 0, "من /api/deterioration/events", (summary.deteriorationEventsCount || 0) ? "warning" : "success"], "deterioration-events", "عرض أحداث التدهور")}
      ${renderActionKpi(["الاستجابات المسجلة", summary.clinicalResponsesCount ?? 0, `متوسط البدء ${summary.averageResponseDelayMinutes ?? "-"} د`, "info"], "medical-response-log", "عرض الاستجابات المسجلة")}
      ${renderActionKpi(["المآلات", summary.outcomesCount ?? 0, "من /api/outcomes", (summary.outcomesCount || 0) ? "info" : "success"], "clinical-outcomes", "عرض المآلات السريرية")}
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
  return `
    <div class="grid cols-3">
      ${renderKpi(["إجمالي المرضى", appState.patients.length, "بيانات قاعدة محلية", "info"])}
      ${renderKpi(["مرحلة التدخل", appState.patients.filter((p) => p.studyGroup === "intervention").length, "مجموعة الدراسة", "success"])}
      ${renderKpi(["متوسط الجلسات", "3/أسبوع", "من بيانات التهيئة", "info"])}
    </div>
    <div style="margin-top:16px">${card("قائمة المرضى", renderPatientSelectionTable(appState.patients, { includeName: false, includeVintage: true }))}</div>`;
}

function patientSearchText(patient) {
  return `${patient.patientCode || ""} ${patient.fullName || ""}`.toLowerCase();
}

function filteredProfilePatients() {
  const query = appState.patientProfileSearch.trim().toLowerCase();
  if (!query) return appState.patients;
  return appState.patients.filter((patient) => patientSearchText(patient).includes(query));
}

function renderPatientSelectionTable(patients, options = {}) {
  if (!patients.length) return emptyBlock("لا توجد بيانات مرضى حتى الآن");
  const includeName = options.includeName === true;
  const includeVintage = options.includeVintage === true;
  const headers = [
    "رمز المريض",
    ...(includeName ? ["الاسم"] : []),
    "العمر",
    "الجنس",
    "مرحلة الدراسة",
    "مجموعة الدراسة",
    ...(includeVintage ? ["مدة الغسيل بالشهور"] : []),
    "جلسات أسبوعية"
  ];
  const rows = patients.map((patient) => `
    <tr class="clickable-row" data-patient-search-row data-search="${escapeHtml(patientSearchText(patient))}" onclick="selectPatientProfile(${patient.id})">
      <td><button class="table-link" type="button" onclick="event.stopPropagation(); selectPatientProfile(${patient.id})">${escapeHtml(patient.patientCode)}</button></td>
      ${includeName ? `<td>${escapeHtml(patient.fullName || "-")}</td>` : ""}
      <td>${escapeHtml(patient.age)}</td>
      <td>${escapeHtml(label(labels.gender, patient.gender))}</td>
      <td>${escapeHtml(label(labels.studyPhase, patient.studyPhase))}</td>
      <td>${escapeHtml(label(labels.studyGroup, patient.studyGroup))}</td>
      ${includeVintage ? `<td>${escapeHtml(patient.dialysisVintageMonths)}</td>` : ""}
      <td>${escapeHtml(patient.weeklySessionsCount)}</td>
    </tr>`).join("");
  return `<div class="table-wrap patient-selector-table"><table><thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>`;
}

function renderPatientProfileSelector() {
  if (appState.loading.patients) return tableSkeleton("جاري تحميل قائمة المرضى...");
  if (appState.errors.patients) return `<div class="state-message error" role="alert"><strong>تعذر تحميل قائمة المرضى</strong><span>${escapeHtml(appState.errors.patients)}</span></div>`;
  if (!appState.patients.length) return emptyBlock("لا توجد بيانات مرضى حتى الآن");
  const patients = filteredProfilePatients();
  return card("اختر مريضاً لعرض الملف", `
    <div class="patient-selector-toolbar">
      <input type="search" value="${escapeHtml(appState.patientProfileSearch)}" placeholder="ابحث برمز المريض أو الاسم..." oninput="filterPatientProfileSelector(this.value)">
    </div>
    <div id="patientSelectorEmpty" class="state-message empty" style="${patients.length ? "display:none" : ""}"><strong>لا توجد نتائج مطابقة</strong></div>
    ${patients.length ? renderPatientSelectionTable(patients, { includeName: true }) : ""}
  `);
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
  const alertFilter = currentAlertFilter();
  const visibleAlerts = applyAlertRouteFilter(appState.alerts, alertFilter);
  const high = applyAlertRouteFilter(appState.alerts, { highRisk: true }).length;
  const medium = appState.alerts.filter((item) => item.riskLevel === "medium" || item.severityLevel === "medium").length;
  const filterPanel = alertFilter.highRisk ? `<div class="filter-bar"><span class="badge danger">عرض التنبيهات عالية الخطورة</span><button class="btn" type="button" onclick="setRoute('active-alerts')">عرض كل التنبيهات</button></div>` : "";
  const alertsTable = visibleAlerts.length
    ? renderTable(["المعرف", "رمز المريض", "مستوى الخطر", "الشدة", "الأولوية", "الحالة", "وقت الإنشاء", "سبب التنبيه"], visibleAlerts.map(alertFullRow))
    : emptyBlock(alertFilter.highRisk ? "لا توجد تنبيهات عالية الخطورة حالياً" : "لا توجد تنبيهات نشطة");
  return `
    ${filterPanel}
    <div class="grid cols-3">
      ${renderKpi(["عالية الخطورة", high, "تحتاج تصعيد", high ? "danger" : "success"], high > 0)}
      ${renderKpi(["إجمالي التنبيهات", appState.alerts.length, "من قاعدة البيانات", "info"])}
      ${renderKpi(["متوسطة", medium, "مراقبة سريرية", medium ? "warning" : "success"])}
    </div>
    <div class="grid cols-2" style="margin-top:16px">
      ${card("فتح سجل تدهور سريري", renderDeteriorationEventForm())}
      ${card("نتيجة فتح السجل", renderDeteriorationSubmission())}
    </div>
    <div style="margin-top:16px">${card(alertFilter.highRisk ? "التنبيهات عالية الخطورة" : "التنبيهات النشطة", alertsTable)}</div>`;
}

function currentAlertFilter() {
  const params = parseCurrentRoute().params;
  const highRisk = params.get("risk_level") === "high" || params.get("severity_level") === "high" || ["urgent", "immediate"].includes(params.get("priority"));
  return { highRisk };
}

function applyAlertRouteFilter(alerts, filter) {
  if (!filter.highRisk) return alerts;
  const activeStatuses = new Set(["new", "viewed", "acknowledged", "in_progress"]);
  return alerts.filter((alert) => {
    const active = activeStatuses.has(alert.status);
    const risky = ["high", "critical"].includes(alert.riskLevel) || ["high", "critical"].includes(alert.severityLevel);
    const urgent = ["urgent", "immediate"].includes(alert.priority);
    return active && (risky || urgent);
  });
}

function renderDeteriorationEventForm() {
  const activeAlerts = appState.alerts.filter((alert) => !["closed", "cancelled"].includes(alert.status));
  if (!activeAlerts.length) return `<p class="kpi-meta">لا توجد تنبيهات نشطة متاحة لفتح سجل تدهور سريري.</p>`;
  const alertOptions = activeAlerts.map((alert) => `<option value="${alert.id}">#${alert.id} - ${escapeHtml(alert.patientCode)} - ${escapeHtml(riskLevelLabel(alert.riskLevel))}</option>`).join("");
  return `<form class="form-grid" onsubmit="submitDeteriorationEvent(event)">
    <div class="field"><label>التنبيه المرتبط</label><select name="alert_id" required>${alertOptions}</select></div>
    <div class="field"><label>وقت التدهور</label><input name="deterioration_time" type="datetime-local" value="${defaultMeasurementTime()}" required></div>
    <div class="field full"><label>نوع التدهور</label><select name="deterioration_type">${Object.entries(labels.deteriorationType).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
    <div class="field full"><label>وصف الحالة</label><textarea name="description" placeholder="وصف سريري مختصر للحالة"></textarea></div>
    <input name="created_by_user_id" type="hidden" value="2">
    <div class="footer-actions full"><button class="btn primary" type="submit" ${appState.loading.deteriorationSubmission ? "disabled" : ""}>${appState.loading.deteriorationSubmission ? "جاري الحفظ..." : "حفظ حدث التدهور"}</button></div>
  </form>`;
}

function renderDeteriorationSubmission() {
  if (appState.errors.deteriorationSubmission) {
    return `<div class="state-message error" role="alert"><strong>تعذر إنشاء حدث التدهور</strong><span>${escapeHtml(appState.errors.deteriorationSubmission)}</span></div>`;
  }
  const result = appState.deteriorationSubmission;
  if (!result) return `<p class="kpi-meta">اختر تنبيها نشطا وافتح سجل تدهور سريري عند الحاجة. لا يتم إنشاء سجل استجابة في هذه المرحلة.</p>`;
  const event = normalizeDeteriorationEvent(result.event);
  return `<div class="state-message empty"><strong>${result.event_created ? "تم إنشاء حدث التدهور السريري بنجاح" : "يوجد حدث تدهور مسجل مسبقا لهذا التنبيه"}</strong><span>حدث #${event.id} - ${escapeHtml(label(labels.deteriorationType, event.deteriorationType))}</span></div>`;
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
      ${renderKpi(["سجلات Dataset البحثية", s.researchDatasetRows ?? 0, "جاهزة للتصدير", "info"])}
      ${renderKpi(["درجة جودة البيانات", `${s.datasetQualityScore ?? 0}%`, s.exportReadiness || "needs_review", (s.datasetQualityScore || 0) >= 80 ? "success" : "warning"])}
      ${renderKpi(["مآلات مفقودة", s.missingOutcomesCount ?? 0, "فحص الجودة", (s.missingOutcomesCount || 0) ? "warning" : "success"])}
      ${renderKpi(["جاهزية التصدير", s.exportReadiness || "not_ready", "Phase 11", s.exportReadiness === "ready" ? "success" : "warning"])}
    </div>
    <div class="grid cols-2" style="margin-top:16px">
      ${card("توزيع البيانات", renderBarChart([s.patientsCount, s.sessionsCount, s.measurementsCount, s.news2AssessmentsCount, s.alertsCount, s.outcomesCount]))}
      ${card("مؤشرات البحث", renderTable(["المؤشر", "القيمة", "المصدر"], [["المرضى", s.patientsCount, "patients"], ["الجلسات", s.sessionsCount, "dialysis_sessions"], ["أحداث التدهور", s.deteriorationEventsCount, "clinical_deterioration_events"], ["المخرجات", s.outcomesCount, "clinical_outcomes"]]))}
    </div>`;
}

function alertRow(alert) {
  return [alert.id, alert.patientCode, badge(riskLevelLabel(alert.riskLevel), riskTone(alert.riskLevel), alert.riskLevel === "critical" || alert.riskLevel === "high"), label(labels.status, alert.status), formatDateTime(alert.createdAt)];
}

function alertFullRow(alert) {
  return [alert.id, alert.patientCode, badge(riskLevelLabel(alert.riskLevel), riskTone(alert.riskLevel), alert.riskLevel === "critical" || alert.riskLevel === "high"), badge(riskLevelLabel(alert.severityLevel), riskTone(alert.severityLevel), alert.severityLevel === "critical" || alert.severityLevel === "high"), priorityLabel(alert.priority), label(labels.status, alert.status), formatDateTime(alert.createdAt), alert.triggerReason];
}

function renderKpi(item, critical = false) {
  const [labelText, value, meta, tone] = item;
  return `<div class="card kpi ${critical ? "critical" : ""}"><div class="card-body"><div class="kpi-label">${escapeHtml(labelText)}</div><div class="kpi-value">${escapeHtml(value)}</div><div class="kpi-meta">${badge(meta, tone, critical)}</div></div></div>`;
}

function renderActionKpi(item, routeId, ariaLabel, critical = false) {
  const [labelText, value, meta, tone] = item;
  return `<div class="card kpi kpi-action ${critical ? "critical" : ""}" role="button" tabindex="0" aria-label="${escapeHtml(ariaLabel || labelText)}" onclick="setRoute('${escapeHtml(routeId)}')" onkeydown="handleActionKey(event, '${escapeHtml(routeId)}')"><div class="card-body"><div class="kpi-label">${escapeHtml(labelText)}</div><div class="kpi-value">${escapeHtml(value)}</div><div class="kpi-meta">${badge(meta, tone, critical)}</div></div></div>`;
}

function renderStaticTable(route) {
  if (route.entity === "users") {
    return renderStaffUsers();
  }
  if (route.entity === "roles") {
    return renderRolesMatrix();
  }
  if (route.entity === "medical" || route.entity === "nursing") {
    return renderClinicalResponseLog(route.entity);
  }
  if (route.entity === "events") {
    return renderDeteriorationEvents();
  }
  if (route.entity === "outcomes") {
    return renderClinicalOutcomes();
  }
  if (route.entity === "news2") {
    if (appState.loading.news2Assessments) return tableSkeleton("جاري تحميل سجل NEWS2...");
    if (appState.errors.news2Assessments) return errorBlock("news2Assessments");
    if (appState.news2Assessments.length) {
      const rows = appState.news2Assessments.map((item) => [
        item.id,
        item.patientId,
        item.dialysisSessionId,
        item.totalScore,
        badge(riskLevelLabel(item.riskLevel), riskTone(item.riskLevel), item.alertRequired),
        item.alertRequired ? "يتطلب تنبيها" : "دون عتبة التنبيه",
        formatDateTime(item.createdAt)
      ]);
      return card("سجل NEWS2", renderTable(["المعرف", "المريض", "الجلسة", "الدرجة", "الخطورة", "الحالة", "وقت الإنشاء"], rows));
    }
  }
  const rows = fallbackRows[route.entity] || fallbackRows.events;
  return `<div class="grid cols-3">${renderKpi(["إجمالي السجلات", rows.length, "بيانات مؤقتة حتى إضافة endpoint", "info"])}${renderKpi(["جاهزية التكامل", "جزئية", "سيتم ربطها لاحقا", "warning"])}${renderKpi(["حالة الشاشة", "تعمل", "hash routing محفوظ", "success"])}</div><div style="margin-top:16px">${card(route.label, renderTable(["المعرف", "المرجع", "الوقت", "الحالة", "المؤشر"], rows))}</div>`;
}

function renderDeteriorationEvents() {
  if (appState.loading.deteriorationEvents) return tableSkeleton("جاري تحميل سجل التدهور السريري...");
  if (appState.errors.deteriorationEvents) return errorBlock("deteriorationEvents");
  if (!appState.deteriorationEvents.length) return emptyBlock("لا توجد أحداث تدهور سريري مسجلة");
  const rows = appState.deteriorationEvents.map((event) => [
    event.id,
    event.patientCode,
    event.alertId,
    event.news2TotalScore,
    badge(riskLevelLabel(event.riskLevel), riskTone(event.riskLevel), event.riskLevel === "high" || event.riskLevel === "critical"),
    label(labels.deteriorationType, event.deteriorationType),
    formatDateTime(event.deteriorationTime),
    event.timeFromSessionStartMinutes ?? "-"
  ]);
  return `<div class="grid cols-3">${renderKpi(["إجمالي الأحداث", appState.deteriorationEvents.length, "من /api/deterioration/events", "info"])}${renderKpi(["هبوط ضغط", appState.deteriorationEvents.filter((event) => event.deteriorationType === "acute_hypotension").length, "تصنيف سريري", "warning"])}${renderKpi(["قيد المتابعة", appState.deteriorationEvents.filter((event) => event.alertStatus !== "closed").length, "حسب حالة التنبيه", "warning"])}</div><div style="margin-top:16px">${card("سجل التدهور السريري", renderTable(["المعرف", "المريض", "التنبيه", "NEWS2", "الخطورة", "نوع التدهور", "وقت التدهور", "من بداية الجلسة"], rows))}</div>`;
}

function renderClinicalOutcomes() {
  if (appState.loading.clinicalOutcomes || appState.loading.outcomeSummary) return tableSkeleton("جاري تحميل المآلات السريرية...");
  if (appState.errors.clinicalOutcomes) return errorBlock("clinicalOutcomes");
  const summary = appState.outcomeSummary || {};
  const rows = appState.clinicalOutcomes.map(outcomeRow);
  return `<div class="grid cols-3">
    ${renderKpi(["إجمالي المآلات", summary.totalOutcomes ?? appState.clinicalOutcomes.length, "من /api/outcomes", "info"])}
    ${renderKpi(["استقرار واستكمال الجلسة", summary.stableCompletedSessionCount ?? 0, "24-72 ساعة", "success"])}
    ${renderKpi(["إدخال إلى المستشفى", summary.hospitalAdmissionCount ?? 0, "مؤشر بحثي", (summary.hospitalAdmissionCount || 0) ? "warning" : "success"])}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("تسجيل المآل السريري", renderOutcomeForm())}
    ${card("نتيجة التسجيل", renderOutcomeSubmission())}
  </div>
  <div style="margin-top:16px">${card("متابعة المآلات", rows.length ? renderTable(["المعرف", "المريض", "تاريخ الجلسة", "التنبيه", "NEWS2", "نوع التدهور", "نوع المآل", "الفترة", "المسجل", "وقت التسجيل"], rows) : emptyBlock("لا توجد مآلات سريرية مسجلة حتى الآن"))}</div>`;
}

function outcomeRow(outcome) {
  return [
    outcome.id,
    outcome.patientCode,
    outcome.sessionDate || "-",
    outcome.alertId ? `#${outcome.alertId}` : "-",
    outcome.news2TotalScore ?? "-",
    label(labels.deteriorationType, outcome.deteriorationType),
    label(labels.outcomeType, outcome.outcomeType),
    `${outcome.outcomeWindowHours} ساعة`,
    outcome.recordedByUserId ?? "-",
    formatDateTime(outcome.createdAt)
  ];
}

function renderOutcomeForm() {
  const events = appState.deteriorationEvents || [];
  if (appState.loading.deteriorationEvents) return loadingBlock("جاري تحميل أحداث التدهور المرتبطة...");
  if (!events.length) return `<p class="kpi-meta">لا توجد أحداث تدهور متاحة لتسجيل مآل سريري.</p>`;
  const eventOptions = events.map((event) => `<option value="${event.id}">#${event.id} - ${escapeHtml(event.patientCode)} - NEWS2 ${escapeHtml(event.news2TotalScore ?? "-")}</option>`).join("");
  return `<form class="form-grid" onsubmit="submitClinicalOutcome(event)">
    <div class="field full"><label>حدث التدهور المرتبط</label><select name="clinical_deterioration_event_id" required>${eventOptions}</select></div>
    <div class="field"><label>نوع المآل</label><select name="outcome_type" required>${Object.entries(labels.outcomeType).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
    <div class="field"><label>الفترة الزمنية</label><select name="outcome_window_hours" required><option value="24">24 ساعة</option><option value="48">48 ساعة</option><option value="72">72 ساعة</option></select></div>
    <div class="field full"><label>وصف المآل</label><textarea name="description" placeholder="وصف سريري مختصر للمآل خلال 24-72 ساعة"></textarea></div>
    <input name="recorded_by_user_id" type="hidden" value="2">
    <div class="footer-actions full"><button class="btn primary" type="submit" ${appState.loading.outcomeSubmission ? "disabled" : ""}>${appState.loading.outcomeSubmission ? "جاري الحفظ..." : "حفظ المآل"}</button></div>
  </form>`;
}

function renderOutcomeSubmission() {
  if (appState.errors.outcomeSubmission) {
    return `<div class="state-message error" role="alert"><strong>تعذر تسجيل المآل</strong><span>${escapeHtml(appState.errors.outcomeSubmission)}</span></div>`;
  }
  const result = appState.outcomeSubmission;
  if (!result) return `<p class="kpi-meta">اختر حدث التدهور، نوع المآل، والفترة الزمنية ثم احفظ السجل.</p>`;
  const outcome = normalizeClinicalOutcome(result.outcome);
  return `<div class="state-message empty"><strong>${result.outcome_created ? "تم تسجيل المآل بنجاح" : "يوجد مآل مسجل مسبقا لهذه الفترة"}</strong><span>مآل #${outcome.id} - ${escapeHtml(label(labels.outcomeType, outcome.outcomeType))} - ${outcome.outcomeWindowHours} ساعة</span></div>`;
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

function roleOptions(selected = "") {
  const order = ["admin", "technical_admin", "doctor", "on_call_doctor", "nurse", "researcher"];
  return order.map((role) => `<option value="${role}" ${selected === role ? "selected" : ""}>${escapeHtml(label(labels.role, role))}</option>`).join("");
}

function renderStaffUsers() {
  if (appState.loading.staffUsers) return tableSkeleton("جاري تحميل المستخدمين...");
  if (appState.errors.staffUsers) return errorBlock("staffUsers");
  const canCreate = hasPermission("users:create");
  const rows = appState.staffUsers.map((user) => [
    user.fullName,
    user.username || "-",
    user.email,
    user.department || "-",
    user.jobTitle || "-",
    label(labels.role, user.role),
    badge(user.isActive ? "نشط" : "موقوف", user.isActive ? "success" : "warning"),
    renderStaffUserActions(user)
  ]);
  return `
    <div class="footer-actions profile-actions">
      ${canCreate ? `<button class="btn primary" type="button" onclick="setRoute('create-user')">إضافة موظف</button>` : ""}
    </div>
    <div class="grid cols-3">
      ${renderKpi(["إجمالي المستخدمين", appState.staffUsers.length, "users", "info"])}
      ${renderKpi(["نشط", appState.staffUsers.filter((user) => user.isActive).length, "حسابات مفعلة", "success"])}
      ${renderKpi(["أدوار", new Set(appState.staffUsers.map((user) => user.role)).size, "RBAC", "info"])}
    </div>
    <div style="margin-top:16px">${card("إدارة المستخدمين", rows.length ? renderTable(["الاسم الكامل", "اسم المستخدم", "البريد الإلكتروني", "القسم", "الوظيفة", "الدور", "الحالة", "إجراءات"], rows) : emptyBlock("لا توجد حسابات مستخدمين حتى الآن"))}</div>`;
}

function renderStaffUserActions(user) {
  const actions = [];
  if (hasPermission("users:update")) actions.push(`<button class="btn small" type="button" onclick="setRoute('create-user')">تعديل</button>`);
  if (hasPermission("users:disable")) actions.push(`<button class="btn small" type="button" onclick="toggleStaffUserStatus(${user.id}, ${user.isActive ? "false" : "true"})">${user.isActive ? "إيقاف" : "تفعيل"}</button>`);
  return actions.length ? `<div class="table-actions">${actions.join("")}</div>` : "-";
}

function renderStaffCreateForm() {
  const canCreate = hasPermission("users:create");
  return card("إضافة موظف", `
    ${appState.staffSubmission ? `<div class="state-message success"><strong>${escapeHtml(appState.staffSubmission)}</strong></div>` : ""}
    ${appState.errors.staffSubmission ? `<div class="state-message error" role="alert"><strong>تعذر إنشاء الموظف</strong><span>${escapeHtml(staffErrorMessage(appState.errors.staffSubmission))}</span></div>` : ""}
    <form class="form-grid" onsubmit="submitStaffUser(event)">
      <div class="field"><label>الاسم الكامل</label><input name="full_name" required></div>
      <div class="field"><label>اسم المستخدم</label><input name="username" required></div>
      <div class="field"><label>البريد الإلكتروني</label><input name="email" type="email"></div>
      <div class="field"><label>رقم الهاتف</label><input name="phone"></div>
      <div class="field"><label>القسم</label><input name="department" list="departmentOptions"></div>
      <div class="field"><label>الوظيفة / المهمة</label><input name="job_title" list="jobTitleOptions"></div>
      <div class="field"><label>الدور</label><select name="role" required>${roleOptions("doctor")}</select></div>
      <div class="field"><label>كلمة مرور مؤقتة</label><input name="temporary_password" type="password" minlength="8" required></div>
      <div class="field"><label>الحالة</label><select name="is_active"><option value="true">نشط</option><option value="false">موقوف</option></select></div>
      <datalist id="jobTitleOptions"><option value="طبيب كلى"></option><option value="طبيب مناوب"></option><option value="ممرض غسيل"></option><option value="باحث سريري"></option><option value="تقني نظام"></option><option value="مدير منصة"></option></datalist>
      <datalist id="departmentOptions"><option value="Nephrology"></option><option value="Dialysis Unit"></option><option value="Clinical Research"></option><option value="Information Technology"></option><option value="Administration"></option></datalist>
      <div class="footer-actions full"><button class="btn primary" type="submit" ${canCreate && !appState.loading.staffSubmission ? "" : "disabled"}>${appState.loading.staffSubmission ? "جاري الحفظ..." : "حفظ الموظف"}</button><button class="btn" type="button" onclick="setRoute('users')">إلغاء</button></div>
    </form>`);
}

function staffErrorMessage(message) {
  if (String(message || "").includes("already exists")) return "اسم المستخدم أو البريد الإلكتروني مستخدم مسبقاً";
  if (String(message || "").includes("invalid role")) return "الدور المحدد غير صالح";
  return message || "تعذر حفظ الموظف";
}

function renderFormScreen(route) {
  if (route.entity === "vitals") return renderVitalSignsEntry();
  if (route.entity === "patient") return renderPatientCreateForm(route);
  if (route.entity === "staff") return renderStaffCreateForm();
  const fields = formFields[route.entity] || formFields.patient;
  return card(route.label, `<div class="form-grid">${fields.map((field, index) => `<div class="field ${index === fields.length - 1 ? "full" : ""}"><label>${field}</label>${index === fields.length - 1 ? `<textarea placeholder="${field}"></textarea>` : `<input placeholder="${field}">`}</div>`).join("")}</div><div class="footer-actions"><button class="btn primary">حفظ</button><button class="btn">حفظ كمسودة</button><button class="btn">إلغاء</button></div>`);
}

function renderPatientCreateForm(route) {
  const canCreate = hasPermission("patients:create");
  return card(route.label, `
    ${appState.patientSubmission ? `<div class="state-message empty"><strong>تم حفظ المريض بنجاح</strong><span>${escapeHtml(appState.patientSubmission.patient?.patient_code || "")}</span></div>` : ""}
    ${appState.errors.patientSubmission ? `<div class="state-message error" role="alert"><strong>تعذر حفظ المريض</strong><span>${escapeHtml(patientErrorMessage(appState.errors.patientSubmission))}</span></div>` : ""}
    ${canCreate ? "" : `<div class="state-message warning"><strong>ليست لديك صلاحية إضافة مريض</strong><span>استخدم دور الطبيب أو المدير في الوضع التجريبي.</span></div>`}
    <form class="form-grid" onsubmit="submitPatientCreate(event)">
      <div class="field"><label>الاسم الكامل</label><input name="full_name" required placeholder="الاسم الكامل"></div>
      <div class="field"><label>رقم الملف</label><input name="patient_code" required placeholder="ANON-P-1004"></div>
      <div class="field"><label>العمر</label><input name="age" type="number" min="0" max="130" required placeholder="58"></div>
      <div class="field"><label>تاريخ الميلاد</label><input name="birth_date" type="date"></div>
      <div class="field"><label>الجنس</label><select name="gender" required><option value="">اختر</option><option value="female">أنثى</option><option value="male">ذكر</option></select></div>
      <div class="field"><label>نوع الوصول الوعائي</label><input name="vascular_access_type" placeholder="لا يحفظ ضمن جدول المرضى حاليا"></div>
      <div class="field full"><label>الأمراض المصاحبة</label><textarea name="comorbidities" placeholder="الأمراض المصاحبة"></textarea></div>
      <div class="field"><label>عدد جلسات الغسيل أسبوعيا</label><input name="weekly_sessions_count" type="number" min="1" max="14" value="3"></div>
      <div class="field"><label>وزن الجفاف المستهدف</label><input name="target_dry_weight" type="number" min="1" max="500" step="0.1"></div>
      <div class="field"><label>تاريخ بداية الغسيل</label><input name="dialysis_start_date" type="date"></div>
      <div class="field"><label>مرحلة الدراسة</label><select name="study_phase"><option value="post_implementation">بعد التطبيق</option><option value="pre_implementation">قبل التطبيق</option></select></div>
      <div class="field"><label>مجموعة الدراسة</label><select name="study_group"><option value="intervention">تدخل</option><option value="control">ضابطة</option></select></div>
      <div class="field full"><label>ملاحظات سريرية</label><textarea name="baseline_functional_status" placeholder="ملاحظات سريرية"></textarea></div>
      <div class="footer-actions full"><button class="btn primary" type="submit" ${appState.loading.patientSubmission || !canCreate ? "disabled" : ""}>${appState.loading.patientSubmission ? "جاري الحفظ..." : "حفظ"}</button><button class="btn" type="button" onclick="setRoute('patients')">إلغاء</button></div>
    </form>
  `);
}

function renderVitalSignsEntry() {
  const patientOptions = appState.patients.map((patient) => `<option value="${patient.id}">${escapeHtml(patient.patientCode)}</option>`).join("");
  const sessionOptions = appState.dialysisSessions.map((session) => `<option value="${session.id}" data-patient-id="${session.patientId}">${escapeHtml(session.patientCode)} - ${escapeHtml(session.sessionDate)} - ${escapeHtml(label(labels.sessionStatus, session.sessionStatus))}</option>`).join("");
  const result = appState.monitoringSubmission?.news2_assessment;
  const success = appState.monitoringSubmission ? `<div class="state-message empty"><strong>تم حفظ القياس وحساب NEWS2 بنجاح</strong><span>تم إنشاء سجل قياس وسجل تقييم NEWS2 دون إنشاء تنبيه آلي في هذه المرحلة.</span></div>` : "";
  const resultPanel = result ? renderMonitoringResult(result, appState.monitoringSubmission?.alert) : `<p class="kpi-meta">سيظهر مجموع NEWS2 ومكونات الدرجة بعد حفظ القياس.</p>`;
  return `<div class="grid cols-2">
    ${card("إدخال العلامات الحيوية", `
      ${appState.errors.monitoringSubmission ? `<div class="state-message error" role="alert"><strong>تعذر حفظ القياس</strong><span>${escapeHtml(appState.errors.monitoringSubmission)}</span><span>تأكد من صحة البيانات المدخلة ومن ارتباط الجلسة بالمريض.</span></div>` : ""}
      <form class="form-grid" onsubmit="submitMonitoringMeasurement(event)">
        <div class="field"><label>المريض</label><select name="patient_id" required>${patientOptions}</select></div>
        <div class="field"><label>جلسة الغسيل</label><select name="dialysis_session_id" required>${sessionOptions}</select></div>
        <div class="field"><label>وقت القياس</label><input name="measurement_time" type="datetime-local" value="${defaultMeasurementTime()}" required></div>
        <div class="field"><label>الفاصل الزمني بالدقائق</label><input name="measurement_interval_minutes" type="number" min="1" value="30" required></div>
        <div class="field"><label>معدل التنفس</label><input name="respiratory_rate" type="number" min="1" value="18" required></div>
        <div class="field"><label>تشبع الأوكسجين SpO2</label><input name="spo2" type="number" min="0" max="100" value="95" required></div>
        <div class="field"><label>هل يتلقى أوكسجين؟</label><select name="oxygen_therapy"><option value="false">لا</option><option value="true">نعم</option></select></div>
        <div class="field"><label>ضغط الدم الانقباضي</label><input name="systolic_bp" type="number" min="1" value="125" required></div>
        <div class="field"><label>ضغط الدم الانبساطي</label><input name="diastolic_bp" type="number" min="1" value="75" required></div>
        <div class="field"><label>معدل النبض</label><input name="pulse_rate" type="number" min="1" value="88" required></div>
        <div class="field"><label>درجة الحرارة</label><input name="temperature" type="number" min="25" max="45" step="0.1" value="37.2" required></div>
        <div class="field"><label>مستوى الوعي</label><select name="consciousness_level">${Object.entries(labels.consciousness).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
        <div class="field"><label>وجود ارتباك حديث</label><select name="confusion_status"><option value="false">لا</option><option value="true">نعم</option></select></div>
        <div class="field"><label>مقياس SpO2</label><select name="spo2_scale"><option value="scale_1">Scale 1</option><option value="scale_2">Scale 2 - مراجعة سريرية</option></select></div>
        <input name="recorded_by_user_id" type="hidden" value="3">
        <div class="footer-actions full"><button class="btn primary" type="submit" ${appState.loading.monitoringSubmission ? "disabled" : ""}>${appState.loading.monitoringSubmission ? "جاري الحفظ..." : "حفظ القياس وحساب NEWS2"}</button></div>
      </form>
    `)}
    ${card("نتيجة NEWS2", `${success}${resultPanel}`)}
  </div>`;
}

function renderProfile() {
  if (!appState.selectedPatientId) return renderPatientProfileSelector();
  if (appState.loading.patients && !appState.patients.length) return tableSkeleton("جاري تحميل قائمة المرضى...");
  if (appState.errors.patients) return `<div class="state-message error" role="alert"><strong>تعذر تحميل قائمة المرضى</strong><span>${escapeHtml(appState.errors.patients)}</span></div>`;
  const patient = appState.patients.find((item) => item.id === appState.selectedPatientId);
  if (!patient) return `<div class="state-message warning"><strong>لم يتم العثور على المريض المحدد</strong><button class="btn" type="button" onclick="showPatientProfileSelector()">اختيار مريض آخر</button></div>`;

  const patientSessions = appState.dialysisSessions.filter((session) => session.patientId === patient.id).slice(0, 5);
  const patientAssessments = appState.news2Assessments.filter((assessment) => assessment.patientId === patient.id);
  const patientAlerts = appState.alerts.filter((alert) => alert.patientId === patient.id).slice(0, 5);
  const patientEvents = appState.deteriorationEvents.filter((event) => event.patientId === patient.id).slice(0, 5);
  const patientOutcomes = appState.clinicalOutcomes.filter((outcome) => outcome.patientId === patient.id).slice(0, 5);
  const news2Scores = patientAssessments.slice(-8).map((assessment) => assessment.totalScore ?? 0);

  return `
    <div class="footer-actions profile-actions">
      <button class="btn" type="button" onclick="showPatientProfileSelector()">اختيار مريض آخر</button>
    </div>
    ${card("ملف المريض", `<div class="patient-summary">${[
      ["رمز المريض", patient.patientCode],
      ["الاسم", patient.fullName || "-"],
      ["العمر", patient.age],
      ["الجنس", label(labels.gender, patient.gender)],
      ["مرحلة الدراسة", label(labels.studyPhase, patient.studyPhase)],
      ["مجموعة الدراسة", label(labels.studyGroup, patient.studyGroup)],
      ["مدة الغسيل بالشهور", patient.dialysisVintageMonths],
      ["جلسات أسبوعية", patient.weeklySessionsCount]
    ].map(([a, b]) => `<div class="summary-cell"><span>${escapeHtml(a)}</span><strong>${escapeHtml(b)}</strong></div>`).join("")}</div>`)}
    <div class="grid cols-2" style="margin-top:16px">
      ${card("اتجاه NEWS2", news2Scores.length ? renderBarChart(news2Scores) : emptyBlock("لا توجد قراءات NEWS2 لهذا المريض حتى الآن"))}
      ${card("آخر الجلسات", patientSessions.length ? renderTable(["المعرف", "التاريخ", "الحالة"], patientSessions.map((session) => [session.id, session.sessionDate, label(labels.sessionStatus, session.sessionStatus)])) : emptyBlock("لا توجد جلسات غسيل لهذا المريض حتى الآن"))}
    </div>
    <div class="grid cols-3" style="margin-top:16px">
      ${card("التنبيهات", patientAlerts.length ? renderTable(["المعرف", "الخطورة", "الحالة", "وقت الإنشاء"], patientAlerts.map((alert) => [alert.id, badge(riskLevelLabel(alert.riskLevel), riskTone(alert.riskLevel), alert.riskLevel === "high" || alert.riskLevel === "critical"), label(labels.status, alert.status), formatDateTime(alert.createdAt)])) : emptyBlock("لا توجد تنبيهات لهذا المريض حتى الآن"))}
      ${card("أحداث التدهور", patientEvents.length ? renderTable(["المعرف", "NEWS2", "النوع", "الوقت"], patientEvents.map((event) => [event.id, event.news2TotalScore ?? event.triggeringNews2Score ?? "-", label(labels.deteriorationType, event.deteriorationType), formatDateTime(event.deteriorationTime)])) : emptyBlock("لا توجد أحداث تدهور لهذا المريض حتى الآن"))}
      ${card("المآلات", patientOutcomes.length ? renderTable(["المعرف", "النوع", "الفترة", "وقت التسجيل"], patientOutcomes.map((outcome) => [outcome.id, label(labels.outcomeType, outcome.outcomeType), `${outcome.outcomeWindowHours} ساعة`, formatDateTime(outcome.outcomeRecordedAt || outcome.createdAt)])) : emptyBlock("لا توجد مآلات لهذا المريض حتى الآن"))}
    </div>`;
}

function renderBaseline() {
  return `<div class="grid cols-2">${card("القيم المرجعية", renderTable(["المؤشر", "القيمة المرجعية", "آخر قراءة", "التقييم"], [["ضغط الدم", "135/82", "118/70", "انخفاض"], ["النبض", "78", "96", "ارتفاع"], ["تشبع الأكسجين", "96%", "91%", "متابعة"]]))}${card("سياق سريري", renderFormText(["الأمراض المصاحبة", "الأدوية المؤثرة", "ملاحظات خط الأساس"]))}</div>`;
}

function renderVascular() {
  return `<div class="grid cols-3">${renderKpi(["نوع الوصول", "CVC", "قسطرة وريدية مركزية", "warning"])}${renderKpi(["تقييم العدوى", "متوسط", "يحتاج متابعة", "warning"])}${renderKpi(["كفاءة التدفق", "82%", "مقبول", "success"])}</div><div style="margin-top:16px">${card("توثيق الوصول الوعائي", renderFormText(["موقع الوصول", "حالة الجلد", "معدل التدفق", "ملاحظات التمريض"]))}</div>`;
}

function renderDetails(route) {
  if (route.entity === "event") return renderEventDetails();
  const title = route.entity === "alert" ? "تنبيه NEWS2 عالي الخطورة" : route.entity === "event" ? "حدث تدهور سريري" : "جلسة غسيل نشطة";
  return `<div class="split"><div>${card(title, `<div class="patient-summary">${[["المريض", "ANON-P-1002"], ["NEWS2", "16"], ["الوقت", "08:42"], ["الحالة", "مفتوح"]].map(([a, b]) => `<div class="summary-cell"><span>${a}</span><strong>${b}</strong></div>`).join("")}</div><div style="margin-top:18px">${renderLineChart("تفاصيل الاتجاه السريري")}</div>`)}</div><aside>${card("إجراءات مطلوبة", renderActions())}</aside></div>`;
}

function renderEventDetails() {
  if (appState.loading.deteriorationEvents) return loadingBlock("جاري تحميل تفاصيل حدث التدهور...");
  const event = appState.deteriorationEvents[0];
  if (!event) return emptyBlock("لا يوجد حدث تدهور سريري لعرض تفاصيله");
  return `<div class="split"><div>${card("تفاصيل حدث التدهور", `<div class="patient-summary">${[
    ["رمز المريض", event.patientCode],
    ["جلسة الغسيل", event.sessionDate || event.dialysisSessionId],
    ["التنبيه", `#${event.alertId}`],
    ["NEWS2", event.news2TotalScore],
    ["مستوى الخطورة", riskLevelLabel(event.riskLevel)],
    ["نوع التدهور", label(labels.deteriorationType, event.deteriorationType)],
    ["وقت التدهور", formatDateTime(event.deteriorationTime)],
    ["من بداية الجلسة", event.timeFromSessionStartMinutes ?? "-"],
    ["حالة التنبيه", label(labels.status, event.alertStatus)]
  ].map(([a, b]) => `<div class="summary-cell"><span>${escapeHtml(a)}</span><strong>${escapeHtml(b)}</strong></div>`).join("")}</div><div style="margin-top:16px"><p class="kpi-meta">${escapeHtml(event.description || "لا يوجد وصف مسجل.")}</p></div>`)}</div><aside>${card("تسجيل الاستجابة الطبية والتمريضية", renderClinicalResponseForm(event))}</aside></div><div style="margin-top:16px">${card("نتيجة تسجيل الاستجابة", renderResponseSubmission())}</div>`;
}

function renderClinicalResponseForm(event) {
  return `<form class="form-grid" onsubmit="submitClinicalResponse(event)">
    <input name="clinical_deterioration_event_id" type="hidden" value="${event.id}">
    <div class="field full"><label>حدث التدهور المرتبط</label><input value="#${event.id} - ${escapeHtml(event.patientCode)}" disabled></div>
    <div class="field full"><label>وقت بدء الاستجابة الفعلي</label><input name="actual_response_start_time" type="datetime-local" value="${defaultMeasurementTime()}" required></div>
    <div class="field full"><label>إجراءات المريض</label><select name="patient_actions" multiple>${Object.entries(labels.patientAction).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
    <div class="field full"><label>إجراءات الوصلة الوعائية</label><select name="vascular_access_actions" multiple>${Object.entries(labels.vascularAction).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
    <div class="field full"><label>المستخدم المستجيب</label><input name="responded_by_user_id" type="number" min="1" value="2"></div>
    <div class="field full"><label>ملاحظات الاستجابة</label><textarea name="notes" placeholder="ملاحظات سريرية موجزة"></textarea></div>
    <div class="footer-actions full"><button class="btn primary" type="submit" ${appState.loading.responseSubmission ? "disabled" : ""}>${appState.loading.responseSubmission ? "جاري الحفظ..." : "حفظ الاستجابة"}</button></div>
  </form>`;
}

function renderResponseSubmission() {
  if (appState.errors.responseSubmission) {
    return `<div class="state-message error" role="alert"><strong>تعذر تسجيل الاستجابة</strong><span>${escapeHtml(appState.errors.responseSubmission)}</span></div>`;
  }
  const result = appState.responseSubmission;
  if (!result) return `<p class="kpi-meta">سيظهر سجل الاستجابة هنا بعد الحفظ. لا يتم إنشاء مخرجات سريرية في هذه المرحلة.</p>`;
  const response = normalizeClinicalResponse(result.response);
  return `<div class="state-message empty"><strong>${result.response_created ? "تم تسجيل الاستجابة بنجاح" : "يوجد سجل استجابة مسجل مسبقا لهذا الحدث"}</strong><span>استجابة #${response.id} - زمن البدء: ${formatDateTime(response.actualResponseStartTime)} - التأخير: ${response.responseDelayMinutes ?? "-"} دقيقة</span></div>`;
}

function renderClinicalResponseLog(entity) {
  if (appState.loading.clinicalResponses) return tableSkeleton("جاري تحميل سجل الاستجابة...");
  if (appState.errors.clinicalResponses) return errorBlock("clinicalResponses");
  if (!appState.clinicalResponses.length) return emptyBlock("لا توجد استجابات مسجلة حتى الآن");
  const rows = appState.clinicalResponses.map((response) => [
    response.id,
    response.patientCode,
    response.alertId,
    label(labels.deteriorationType, response.deteriorationType),
    response.news2TotalScore ?? "-",
    delayBadge(response.responseDelayMinutes),
    entity === "nursing" ? response.vascularAccessActions.map((item) => label(labels.vascularAction, item)).join(", ") : response.patientActions.map((item) => label(labels.patientAction, item)).join(", "),
    formatDateTime(response.actualResponseStartTime)
  ]);
  const title = entity === "nursing" ? "الاستجابة التمريضية" : "الاستجابة الطبية";
  return `<div class="grid cols-3">${renderKpi(["الاستجابات", appState.clinicalResponses.length, "من /api/responses", "info"])}${renderKpi(["متوسط التأخير", averageDelayText(), "دقيقة", "warning"])}${renderKpi(["الأسرع", fastestDelayText(), "دقيقة", "success"])}</div><div style="margin-top:16px">${card(title, renderTable(["المعرف", "المريض", "التنبيه", "نوع التدهور", "NEWS2", "زمن البدء", "الإجراءات", "وقت الاستجابة"], rows))}</div>`;
}

function delayBadge(value) {
  if (value === null || value === undefined) return badge("-", "neutral");
  if (value <= 5) return badge(`${value} د`, "success");
  if (value <= 15) return badge(`${value} د`, "warning");
  return badge(`${value} د`, "danger", true);
}

function averageDelayText() {
  const values = appState.clinicalResponses.map((response) => response.responseDelayMinutes).filter((value) => Number.isFinite(value));
  if (!values.length) return "-";
  return Math.round(values.reduce((sum, value) => sum + value, 0) / values.length);
}

function fastestDelayText() {
  const values = appState.clinicalResponses.map((response) => response.responseDelayMinutes).filter((value) => Number.isFinite(value));
  return values.length ? Math.min(...values) : "-";
}

function renderMonitoring() {
  if (appState.loading.monitoringMeasurements) return tableSkeleton("جاري تحميل قياسات الجلسات...");
  if (appState.errors.monitoringMeasurements) return errorBlock("monitoringMeasurements");
  const latest = appState.monitoringMeasurements[0];
  const rows = appState.monitoringMeasurements.map((item) => [
    item.id,
    item.patientId,
    item.dialysisSessionId,
    formatDateTime(item.measurementTime),
    `${item.systolicBp}/${item.diastolicBp}`,
    item.pulseRate,
    `${item.spo2}%`,
    label(labels.consciousness, item.consciousnessLevel)
  ]);
  return `<div class="grid cols-4">${[
    ["ضغط الدم", latest ? `${latest.systolicBp}/${latest.diastolicBp}` : "-", "آخر قياس محفوظ", "info"],
    ["النبض", latest?.pulseRate ?? "-", "آخر قياس محفوظ", "info"],
    ["SpO2", latest ? `${latest.spo2}%` : "-", "آخر قياس محفوظ", "info"],
    ["القياسات", appState.monitoringMeasurements.length, "من /api/monitoring/measurements", "success"]
  ].map((x) => renderKpi(x)).join("")}</div><div style="margin-top:16px">${card("القياسات الحديثة", rows.length ? renderTable(["المعرف", "المريض", "الجلسة", "وقت القياس", "الضغط", "النبض", "SpO2", "الوعي"], rows) : emptyBlock("لا توجد قياسات محفوظة حتى الآن"))}</div>`;
}

function renderMonitoringResult(result, alert) {
  const alertSummary = alert
    ? `<div class="state-message empty"><strong>${alert.alert_created ? "تم إنشاء تنبيه سريري" : "تم استخدام تنبيه نشط قائم"}</strong><span>المعرف: ${escapeHtml(alert.alert_id || "-")} - الأولوية: ${escapeHtml(priorityLabel(alert.priority))} - الحالة: ${escapeHtml(label(labels.status, alert.status))}</span></div>`
    : `<div class="state-message empty"><strong>لا يوجد تنبيه آلي</strong><span>درجة NEWS2 لا تحقق قواعد إنشاء التنبيه في هذه المرحلة.</span></div>`;
  return `${renderKpi(["الدرجة الكلية", result.total_score, riskLevelLabel(result.risk_level), riskTone(result.risk_level)], result.alert_required)}
    ${alertSummary}
    <div class="patient-summary">
      <div class="summary-cell"><span>مستوى الخطورة</span><strong>${riskLevelLabel(result.risk_level)}</strong></div>
      <div class="summary-cell"><span>يتطلب تنبيها سريريا</span><strong>${result.alert_required ? "نعم" : "لا"}</strong></div>
      <div class="summary-cell"><span>سبب التفعيل</span><strong>${label(labels.trigger, result.trigger_reason)}</strong></div>
      <div class="summary-cell"><span>مؤشر منفرد بدرجة 3</span><strong>${result.single_parameter_trigger ? "نعم" : "لا"}</strong></div>
    </div>
    <div style="margin-top:16px">${renderTable(["المكون", "النقاط"], [
      ["التنفس", result.respiratory_score],
      ["تشبع الأوكسجين", result.spo2_score],
      ["الأوكسجين الإضافي", result.oxygen_score],
      ["ضغط الدم الانقباضي", result.systolic_bp_score],
      ["النبض", result.pulse_score],
      ["درجة الحرارة", result.temperature_score],
      ["الوعي", result.consciousness_score]
    ])}</div>`;
}

function defaultMeasurementTime() {
  const date = new Date();
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return date.toISOString().slice(0, 16);
}

async function submitMonitoringMeasurement(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  appState.loading.monitoringSubmission = true;
  appState.errors.monitoringSubmission = null;
  render();
  try {
    appState.monitoringSubmission = await api.createMonitoringMeasurement({
      patient_id: Number(data.get("patient_id")),
      dialysis_session_id: Number(data.get("dialysis_session_id")),
      measurement_time: new Date(data.get("measurement_time")).toISOString(),
      measurement_interval_minutes: Number(data.get("measurement_interval_minutes")),
      respiratory_rate: Number(data.get("respiratory_rate")),
      spo2: Number(data.get("spo2")),
      oxygen_therapy: data.get("oxygen_therapy") === "true",
      systolic_bp: Number(data.get("systolic_bp")),
      diastolic_bp: Number(data.get("diastolic_bp")),
      pulse_rate: Number(data.get("pulse_rate")),
      temperature: Number(data.get("temperature")),
      consciousness_level: data.get("consciousness_level"),
      confusion_status: data.get("confusion_status") === "true",
      spo2_scale: data.get("spo2_scale"),
      recorded_by_user_id: Number(data.get("recorded_by_user_id"))
    });
    appState.monitoringMeasurements = await api.getMonitoringMeasurements();
    appState.news2Assessments = await api.getNews2Assessments();
    appState.alerts = await api.getAlerts();
    appState.researchSummary = await api.getResearchSummary();
  } catch (error) {
    appState.errors.monitoringSubmission = error.message || "تعذر حفظ القياس";
  } finally {
    appState.loading.monitoringSubmission = false;
    render();
  }
}

async function submitPatientCreate(event) {
  event.preventDefault();
  appState.loading.patientSubmission = true;
  appState.errors.patientSubmission = null;
  appState.patientSubmission = null;
  render();
  try {
    const payload = patientPayloadFromForm(event.currentTarget);
    appState.patientSubmission = await api.createPatient(payload);
    appState.patients = await api.getPatients();
    appState.researchSummary = await api.getResearchSummary();
    setRoute("patients");
  } catch (error) {
    appState.errors.patientSubmission = error.message || "تعذر حفظ المريض";
  } finally {
    appState.loading.patientSubmission = false;
    render();
  }
}

async function submitStaffUser(event) {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  appState.loading.staffSubmission = true;
  appState.errors.staffSubmission = null;
  appState.staffSubmission = null;
  render();
  try {
    await api.createStaffUser({
      full_name: data.get("full_name"),
      username: data.get("username"),
      email: data.get("email") || null,
      phone: data.get("phone") || null,
      department: data.get("department") || null,
      job_title: data.get("job_title") || null,
      role: data.get("role"),
      temporary_password: data.get("temporary_password"),
      is_active: data.get("is_active") === "true"
    });
    appState.staffUsers = await api.getStaffUsers();
    appState.staffSubmission = "تم إنشاء الموظف بنجاح";
    setRoute("users");
  } catch (error) {
    appState.errors.staffSubmission = error.message || "تعذر حفظ الموظف";
  } finally {
    appState.loading.staffSubmission = false;
    render();
  }
}

async function toggleStaffUserStatus(userId, isActive) {
  appState.errors.staffUsers = null;
  try {
    const updated = await api.updateStaffUserStatus(userId, { is_active: isActive });
    appState.staffUsers = appState.staffUsers.map((user) => (user.id === updated.id ? updated : user));
  } catch (error) {
    appState.errors.staffUsers = error.message || "تعذر تحديث حالة المستخدم";
  }
  render();
}

async function submitDeteriorationEvent(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  appState.loading.deteriorationSubmission = true;
  appState.errors.deteriorationSubmission = null;
  render();
  try {
    appState.deteriorationSubmission = await api.createDeteriorationEvent({
      alert_id: Number(data.get("alert_id")),
      deterioration_time: new Date(data.get("deterioration_time")).toISOString(),
      deterioration_type: data.get("deterioration_type"),
      description: data.get("description") || null,
      created_by_user_id: Number(data.get("created_by_user_id"))
    });
    appState.deteriorationEvents = await api.getDeteriorationEvents();
    appState.responseTrackingRecords = await api.getResponseTrackingRecords();
    appState.responseTrackingSummary = await api.getResponseTrackingSummary();
    appState.alerts = await api.getAlerts();
    appState.researchSummary = await api.getResearchSummary();
  } catch (error) {
    appState.errors.deteriorationSubmission = error.message || "تعذر إنشاء حدث التدهور";
  } finally {
    appState.loading.deteriorationSubmission = false;
    render();
  }
}

async function submitClinicalResponse(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  appState.loading.responseSubmission = true;
  appState.errors.responseSubmission = null;
  render();
  try {
    appState.responseSubmission = await api.createClinicalResponse({
      clinical_deterioration_event_id: Number(data.get("clinical_deterioration_event_id")),
      actual_response_start_time: new Date(data.get("actual_response_start_time")).toISOString(),
      patient_actions: data.getAll("patient_actions"),
      vascular_access_actions: data.getAll("vascular_access_actions"),
      responded_by_user_id: Number(data.get("responded_by_user_id")),
      notes: data.get("notes") || null
    });
    appState.clinicalResponses = await api.getClinicalResponses();
    appState.responseTrackingRecords = await api.getResponseTrackingRecords();
    appState.responseTrackingSummary = await api.getResponseTrackingSummary();
    appState.alerts = await api.getAlerts();
    appState.researchSummary = await api.getResearchSummary();
  } catch (error) {
    appState.errors.responseSubmission = error.message || "تعذر تسجيل الاستجابة";
  } finally {
    appState.loading.responseSubmission = false;
    render();
  }
}

async function submitClinicalOutcome(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  appState.loading.outcomeSubmission = true;
  appState.errors.outcomeSubmission = null;
  render();
  try {
    appState.outcomeSubmission = await api.createClinicalOutcome({
      clinical_deterioration_event_id: Number(data.get("clinical_deterioration_event_id")),
      outcome_type: data.get("outcome_type"),
      outcome_window_hours: Number(data.get("outcome_window_hours")),
      description: data.get("description") || null,
      recorded_by_user_id: Number(data.get("recorded_by_user_id"))
    });
    appState.clinicalOutcomes = await api.getClinicalOutcomes();
    appState.outcomeSummary = await api.getOutcomeSummary();
    appState.researchSummary = await api.getResearchSummary();
  } catch (error) {
    appState.errors.outcomeSubmission = error.message || "تعذر تسجيل المآل";
  } finally {
    appState.loading.outcomeSubmission = false;
    render();
  }
}

function renderAssessment() {
  const result = appState.news2Demo;
  const resultPanel = result
    ? `${renderKpi(["NEWS2", result.total_score, riskLevelLabel(result.risk_level), riskTone(result.risk_level)], result.alert_required)}
      ${renderTable(["المكون", "النقاط"], [
        ["التنفس", result.respiratory_score],
        ["SpO2", result.spo2_score],
        ["الأكسجين الإضافي", result.oxygen_score],
        ["الضغط الانقباضي", result.systolic_bp_score],
        ["النبض", result.pulse_score],
        ["الحرارة", result.temperature_score],
        ["الوعي", result.consciousness_score]
      ])}
      <p class="kpi-meta">${label(labels.trigger, result.trigger_reason)}</p>
      <p class="kpi-meta">${result.alert_required ? "يتطلب تنبيها سريريا" : "لا يتطلب تنبيها حسب العتبة الرقمية"}</p>`
    : `${appState.errors.news2Demo ? errorBlock("news2Demo") : ""}<p class="kpi-meta">أدخل العلامات الحيوية لحساب NEWS2 عبر الخادم دون حفظ السجل في قاعدة البيانات.</p>`;
  return `<div class="grid cols-2">${card("حاسبة NEWS2", renderNews2CalculatorForm())}${card("نتيجة الحساب", resultPanel)}</div><div style="margin-top:16px">${card("ملاحظة السلامة الطبية", `<p class="kpi-meta">NEWS2 أداة دعم قرار للكشف المبكر عن التدهور ولا تستبدل الحكم السريري. يجب مراجعة التطبيق سريريا قبل الاستخدام الفعلي.</p>`)}</div>`;
}

function renderNews2CalculatorForm() {
  return `<form class="form-grid" onsubmit="calculateNews2Demo(event)">
    <div class="field"><label>معدل التنفس</label><input name="respiratory_rate" type="number" min="1" value="18" required></div>
    <div class="field"><label>SpO2</label><input name="spo2" type="number" min="0" max="100" value="95" required></div>
    <div class="field"><label>الضغط الانقباضي</label><input name="systolic_bp" type="number" min="1" value="125" required></div>
    <div class="field"><label>النبض</label><input name="pulse_rate" type="number" min="1" value="88" required></div>
    <div class="field"><label>الحرارة</label><input name="temperature" type="number" min="25" max="45" step="0.1" value="37.2" required></div>
    <div class="field"><label>مقياس SpO2</label><select name="spo2_scale"><option value="scale_1">Scale 1</option><option value="scale_2">Scale 2 - مراجعة سريرية</option></select></div>
    <div class="field"><label>مستوى الوعي</label><select name="consciousness_level">${Object.entries(labels.consciousness).map(([value, text]) => `<option value="${value}">${text}</option>`).join("")}</select></div>
    <div class="field"><label>أكسجين إضافي</label><select name="oxygen_therapy"><option value="false">لا</option><option value="true">نعم</option></select></div>
    <div class="footer-actions full"><button class="btn primary" type="submit">احسب NEWS2</button></div>
  </form>`;
}

async function calculateNews2Demo(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  try {
    appState.news2Demo = await api.calculateNews2({
      respiratory_rate: Number(data.get("respiratory_rate")),
      spo2: Number(data.get("spo2")),
      oxygen_therapy: data.get("oxygen_therapy") === "true",
      systolic_bp: Number(data.get("systolic_bp")),
      pulse_rate: Number(data.get("pulse_rate")),
      temperature: Number(data.get("temperature")),
      consciousness_level: data.get("consciousness_level"),
      spo2_scale: data.get("spo2_scale")
    });
    appState.errors.news2Demo = null;
  } catch (error) {
    appState.errors.news2Demo = error.message;
  }
  render();
}

function renderTrend() {
  return `<div class="grid cols-3">${renderKpi(["آخر قراءة", "16", "عالية الخطورة", "danger"], true)}${renderKpi(["أعلى قراءة", "16", "من بيانات التهيئة", "warning"])}${renderKpi(["متوسط النظام", appState.researchSummary?.averageNews2 ?? "-", "من API", "info"])}</div><div style="margin-top:16px">${card("اتجاه NEWS2", renderLineChart("اتجاه NEWS2"))}</div>`;
}

function renderTimeline(route) {
  if (route.entity === "event") return renderEventTimeline();
  return `<div class="split"><div>${card(route.label, renderTimelineItems())}</div><aside>${card("مؤشرات زمنية", `${renderKpi(["زمن الاكتشاف", "0 د", "آلي", "success"])}${renderKpi(["زمن التصعيد", "9 د", "ضمن الهدف", "success"])}${renderKpi(["زمن الإغلاق", "قيد المتابعة", "لم يغلق بعد", "warning"])}`)}</aside></div>`;
}

function renderEventTimeline() {
  if (appState.loading.deteriorationEvents) return loadingBlock("جاري تحميل الخط الزمني للتدهور...");
  const event = appState.deteriorationEvents[0];
  if (!event) return emptyBlock("لا يوجد حدث تدهور سريري لبناء خط زمني");
  const items = [
    [formatDateTime(event.deteriorationTime), "تم تسجيل العلامات الحيوية", `المريض ${event.patientCode}`],
    [formatDateTime(event.createdAt), "تم حساب NEWS2", `الدرجة ${event.news2TotalScore}`],
    [formatDateTime(event.createdAt), "تم إنشاء التنبيه", `تنبيه #${event.alertId}`],
    [formatDateTime(event.createdAt), "تم فتح سجل التدهور", label(labels.deteriorationType, event.deteriorationType)],
    ["قيد الانتظار", "توثيق الاستجابة", "سيتم في مرحلة الاستجابة الطبية والتمريضية"]
  ];
  return `<div class="split"><div>${card("الخط الزمني للتدهور السريري", `<div class="timeline">${items.map(([time, title, text]) => `<div class="timeline-item"><strong>${escapeHtml(time)} - ${escapeHtml(title)}</strong><span>${escapeHtml(text)}</span></div>`).join("")}</div>`)}</div><aside>${card("مؤشرات زمنية", `${renderKpi(["من بداية الجلسة", event.timeFromSessionStartMinutes ?? "-", "دقيقة", "info"])}${renderKpi(["NEWS2", event.news2TotalScore, riskLevelLabel(event.riskLevel), riskTone(event.riskLevel)], event.riskLevel === "high")}`)}</aside></div>`;
}

function renderWorkflow(route) {
  if (route.id === "response-workflow") return renderResponseWorkflow();
  if (route.id === "outcome-tracking") return renderOutcomeTracking();
  return `<div class="grid cols-4">${["اكتشاف", "تأكيد", "تصعيد", "إغلاق"].map((step, index) => renderKpi([step, index < 3 ? "تم" : "نشط", index < 3 ? "موثق" : "بانتظار المخرج", index < 3 ? "success" : "warning"])).join("")}</div><div style="margin-top:16px">${card(route.label, renderTimelineItems())}</div>`;
}

function renderOutcomeTracking() {
  if (appState.loading.clinicalOutcomes || appState.loading.deteriorationEvents) return loadingBlock("جاري تحميل متابعة المآلات...");
  if (appState.errors.clinicalOutcomes) return errorBlock("clinicalOutcomes");
  const outcome = appState.clinicalOutcomes[0];
  if (!outcome) return `<div class="grid cols-2">${card("تسجيل المآل السريري", renderOutcomeForm())}${card("نتيجة التسجيل", renderOutcomeSubmission())}</div>`;
  const items = [
    [outcome.createdAt, "تم فتح سجل التدهور", label(labels.deteriorationType, outcome.deteriorationType)],
    [outcome.outcomeRecordedAt, "تم تسجيل المآل السريري", `${label(labels.outcomeType, outcome.outcomeType)} - ${outcome.outcomeWindowHours} ساعة`],
    [outcome.createdAt, "تم تحديث تحليلات المآلات", `مآل #${outcome.id}`]
  ];
  return `<div class="split">
    <div>${card("متابعة المآلات", `<div class="timeline">${items.map(([time, title, text]) => `<div class="timeline-item"><strong>${escapeHtml(formatDateTime(time))} - ${escapeHtml(title)}</strong><span>${escapeHtml(text)}</span></div>`).join("")}</div>`)}</div>
    <aside>${card("تفاصيل المآل", renderOutcomeDetails(outcome))}</aside>
  </div>`;
}

function renderOutcomeDetails(outcome) {
  return renderTable(["الحقل", "القيمة"], [
    ["رمز المريض", outcome.patientCode],
    ["تاريخ الجلسة", outcome.sessionDate || "-"],
    ["معرف التنبيه", outcome.alertId ? `#${outcome.alertId}` : "-"],
    ["درجة NEWS2", outcome.news2TotalScore ?? "-"],
    ["نوع التدهور", label(labels.deteriorationType, outcome.deteriorationType)],
    ["نوع المآل", label(labels.outcomeType, outcome.outcomeType)],
    ["فترة المآل", `${outcome.outcomeWindowHours} ساعة`],
    ["المستخدم المسجل", outcome.recordedByUserId ?? "-"],
    ["الوصف", outcome.description || "-"],
    ["وقت الإنشاء", formatDateTime(outcome.createdAt)]
  ]);
}

function renderResponseWorkflow() {
  if (appState.loading.responseTrackingRecords || appState.loading.clinicalResponses) return loadingBlock("جاري تحميل مسار الاستجابة...");
  const tracking = appState.responseTrackingRecords[0];
  if (tracking) return renderResponseTrackingWorkflow(tracking);
  if (appState.errors.responseTrackingRecords) return errorBlock("responseTrackingRecords");
  if (appState.loading.clinicalResponses) return loadingBlock("جاري تحميل مسار الاستجابة...");
  const response = appState.clinicalResponses[0];
  if (!response) return emptyBlock("لا توجد استجابة مسجلة لبناء مسار الاستجابة");
  const items = [
    [formatDateTime(response.digitalAlertTime), "تم إنشاء التنبيه", `تنبيه #${response.alertId}`],
    [formatDateTime(response.createdAt), "تم فتح سجل التدهور", label(labels.deteriorationType, response.deteriorationType)],
    [formatDateTime(response.actualResponseStartTime), "بدأت الاستجابة الفعلية", `تأخير ${response.responseDelayMinutes ?? "-"} دقيقة`],
    [formatDateTime(response.createdAt), "تم توثيق الإجراءات الطبية والتمريضية", response.patientActions.map((item) => label(labels.patientAction, item)).join(", ") || "موثق"]
  ];
  return `<div class="split"><div>${card("مسار الاستجابة", `<div class="timeline">${items.map(([time, title, text]) => `<div class="timeline-item"><strong>${escapeHtml(time)} - ${escapeHtml(title)}</strong><span>${escapeHtml(text)}</span></div>`).join("")}</div>`)}</div><aside>${card("زمن الاستجابة", `${renderKpi(["زمن بدء الاستجابة", response.responseDelayMinutes ?? "-", "دقيقة", response.responseDelayMinutes > 15 ? "danger" : response.responseDelayMinutes > 5 ? "warning" : "success"], response.responseDelayMinutes > 15)}${renderKpi(["NEWS2", response.news2TotalScore ?? "-", "عند التدهور", "info"])}`)}</aside></div>`;
}

function renderResponseTrackingWorkflow(tracking) {
  const items = [
    [tracking.vitalSignsRecordedAt, "تم تسجيل العلامات الحيوية", `المريض ${tracking.patientCode}`],
    [tracking.alertCreatedAt, "تم إنشاء التنبيه", `تنبيه #${tracking.alertId}`],
    [tracking.alertViewedAt, "تمت مشاهدة التنبيه", tracking.alertViewedAt ? `${tracking.timeToViewMinutes ?? "-"} دقيقة` : "قيد الانتظار"],
    [tracking.deteriorationEventCreatedAt, "تم فتح سجل التدهور", label(labels.deteriorationType, tracking.deteriorationType)],
    [tracking.actualResponseStartTime, "بدأت الاستجابة", tracking.timeToResponseMinutes !== null && tracking.timeToResponseMinutes !== undefined ? `${tracking.timeToResponseMinutes} دقيقة` : "قيد الانتظار"],
    [tracking.alertClosedAt, "تم إغلاق التنبيه", tracking.alertClosedAt ? `${tracking.totalResponseTimeMinutes ?? "-"} دقيقة إجمالا` : "قيد المتابعة"]
  ];
  const timeline = items.map(([time, title, text]) => {
    const displayTime = time ? formatDateTime(time) : "قيد الانتظار";
    const tone = time ? "" : " pending";
    return `<div class="timeline-item${tone}"><strong>${escapeHtml(displayTime)} - ${escapeHtml(title)}</strong><span>${escapeHtml(text)}</span></div>`;
  }).join("");
  return `<div class="split"><div>${card("مسار الاستجابة", `<div class="timeline">${timeline}</div>`)}</div><aside>${card("زمن الاستجابة", `${renderKpi(["زمن إنشاء التنبيه", minuteText(tracking.timeToAlertMinutes), "من تسجيل العلامات", "info"])}${renderKpi(["زمن بدء الاستجابة", minuteText(tracking.timeToResponseMinutes), "من إنشاء التنبيه", responseTone(tracking.timeToResponseMinutes)], (tracking.timeToResponseMinutes || 0) > 15)}${renderKpi(["NEWS2", tracking.news2TotalScore ?? "-", riskLevelLabel(tracking.riskLevel), riskTone(tracking.riskLevel)])}`)}</aside></div>`;
}

function renderResponseTimeDashboard() {
  if (appState.loading.responseTrackingRecords || appState.loading.responseTrackingSummary) return loadingBlock("جاري تحميل مؤشرات زمن الاستجابة...");
  if (appState.errors.responseTrackingRecords) return errorBlock("responseTrackingRecords");
  const s = appState.responseTrackingSummary || {};
  const rows = responseTrackingRows();
  return `<div class="grid cols-3">
    ${renderKpi(["متوسط زمن إنشاء التنبيه", minuteText(s.averageTimeToAlertMinutes), "من تسجيل العلامات", "info"])}
    ${renderKpi(["متوسط زمن مشاهدة التنبيه", minuteText(s.averageTimeToViewMinutes), "من إنشاء التنبيه", "info"])}
    ${renderKpi(["متوسط زمن بدء الاستجابة", minuteText(s.averageTimeToResponseMinutes), "من إنشاء التنبيه", "warning"])}
    ${renderKpi(["أسرع استجابة", minuteText(s.fastestResponseMinutes), "دقيقة", "success"])}
    ${renderKpi(["أبطأ استجابة", minuteText(s.slowestResponseMinutes), "دقيقة", responseTone(s.slowestResponseMinutes)], (s.slowestResponseMinutes || 0) > 15)}
    ${renderKpi(["تنبيهات بدون استجابة", s.alertsWithoutResponseCount ?? 0, "قيد المتابعة", (s.alertsWithoutResponseCount || 0) ? "warning" : "success"])}
  </div><div style="margin-top:16px">${card("سجل تتبع زمن الاستجابة", rows.length ? renderTable(["رمز المريض", "تاريخ الجلسة", "NEWS2", "مستوى الخطورة", "نوع التدهور", "زمن التنبيه", "زمن المشاهدة", "زمن الاستجابة", "الزمن الإجمالي"], rows) : emptyBlock("لا توجد سجلات تتبع زمن الاستجابة حتى الآن"))}</div>`;
}

function renderResponseAnalytics() {
  if (appState.loading.responseTrackingRecords || appState.loading.responseTrackingSummary) return loadingBlock("جاري تحميل تحليلات الاستجابة...");
  const s = appState.responseTrackingSummary || {};
  const records = appState.responseTrackingRecords || [];
  const averages = [s.averageTimeToAlertMinutes || 0, s.averageTimeToViewMinutes || 0, s.averageTimeToResponseMinutes || 0, s.averageTimeToActionMinutes || 0, s.averageTotalResponseTimeMinutes || 0];
  const withResponse = records.filter((record) => record.timeToResponseMinutes !== null && record.timeToResponseMinutes !== undefined).length;
  const withoutResponse = s.alertsWithoutResponseCount || 0;
  return `<div class="grid cols-4">
    ${renderKpi(["السجلات", s.recordsCount ?? records.length, "response_tracking", "info"])}
    ${renderKpi(["متوسط الاستجابة", minuteText(s.averageTimeToResponseMinutes), "دقيقة", "warning"])}
    ${renderKpi(["مكتملة الاستجابة", withResponse, "لها وقت بدء", "success"])}
    ${renderKpi(["بدون استجابة", withoutResponse, "قيد المتابعة", withoutResponse ? "warning" : "success"])}
  </div><div class="grid cols-2" style="margin-top:16px">${card("متوسطات زمن الاستجابة", renderBarChart(averages))}${card("الاستجابة حسب الحالة", renderBarChart([withResponse, withoutResponse || 1]))}</div><div style="margin-top:16px">${card("تحليل الخطورة والزمن", renderRiskTimingTable(records))}</div>`;
}

function responseTrackingRows() {
  return (appState.responseTrackingRecords || []).map((record) => [
    record.patientCode,
    record.sessionDate || "-",
    record.news2TotalScore ?? "-",
    badge(riskLevelLabel(record.riskLevel), riskTone(record.riskLevel), record.riskLevel === "high" || record.riskLevel === "critical"),
    label(labels.deteriorationType, record.deteriorationType),
    minuteText(record.timeToAlertMinutes),
    minuteText(record.timeToViewMinutes),
    delayBadge(record.timeToResponseMinutes),
    minuteText(record.totalResponseTimeMinutes)
  ]);
}

function renderRiskTimingTable(records) {
  const groups = records.reduce((acc, record) => {
    const key = record.riskLevel || "unknown";
    acc[key] = acc[key] || [];
    if (Number.isFinite(record.timeToResponseMinutes)) acc[key].push(record.timeToResponseMinutes);
    return acc;
  }, {});
  const rows = Object.entries(groups).map(([risk, values]) => [
    riskLevelLabel(risk),
    values.length,
    values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length) : "-",
    values.length ? Math.min(...values) : "-"
  ]);
  return rows.length ? renderTable(["مستوى الخطورة", "عدد الاستجابات", "متوسط الزمن", "الأسرع"], rows) : emptyBlock("لا توجد بيانات كافية للتحليل حسب الخطورة");
}

function minuteText(value) {
  return value === null || value === undefined ? "-" : `${value} د`;
}

function responseTone(value) {
  if (value === null || value === undefined) return "neutral";
  if (value <= 5) return "success";
  if (value <= 15) return "warning";
  return "danger";
}

function renderAnalytics(route) {
  if (route.id === "study-metrics") return renderResearchAnalyticsDashboard();
  if (route.id === "response-time-dashboard") return renderResponseTimeDashboard();
  if (route.id === "response-analytics") return renderResponseAnalytics();
  if (route.id === "outcome-analytics") return renderOutcomeAnalytics();
  if (route.id === "dataset-statistics") return renderDatasetStatistics();
  return `<div class="grid cols-4">${[
    ["المرضى", appState.researchSummary?.patientsCount ?? "-", "API عند التوفر", "info"],
    ["الجلسات", appState.researchSummary?.sessionsCount ?? "-", "API عند التوفر", "info"],
    ["التنبيهات", appState.researchSummary?.alertsCount ?? "-", "API عند التوفر", "warning"],
    ["المخرجات", appState.researchSummary?.outcomesCount ?? "-", "API عند التوفر", "success"]
  ].map((item) => renderKpi(item)).join("")}</div><div class="grid cols-2" style="margin-top:16px">${card("تحليل الاتجاهات", renderLineChart("تحليل الاتجاهات"))}${card("توزيع المؤشرات", renderBarChart([30, 48, 24, 16, 10]))}</div><div style="margin-top:16px">${card(route.label, renderTable(["المؤشر", "قبل", "بعد", "التحسن"], [["زمن الاستجابة", "18 د", "9 د", "50%"], ["اكتمال التوثيق", "82%", "97%", "15%"], ["التنبيهات المغلقة", "70%", "91%", "21%"]]))}</div>`;
}

function renderDatasetStatistics() {
  if (appState.loading.researchDatasetQuality || appState.loading.researchDatasetRows) return loadingBlock("جاري تحميل إحصاءات البيانات البحثية...");
  if (appState.errors.researchDatasetQuality) return errorBlock("researchDatasetQuality");
  const quality = appState.researchDatasetQuality || {};
  const stats = quality.statistics || {};
  return `<div class="grid cols-4">
    ${renderKpi(["عدد سجلات البحث", stats.dataset_rows ?? quality.totalRows ?? 0, "measurement + NEWS2", "info"])}
    ${renderKpi(["عدد القياسات", stats.measurements_count ?? 0, "intradialytic_measurements", "info"])}
    ${renderKpi(["عدد تنبيهات NEWS2", stats.news2_alerts_count ?? 0, "alerts", (stats.news2_alerts_count || 0) ? "warning" : "success"])}
    ${renderKpi(["عدد أحداث التدهور", stats.deterioration_events_count ?? 0, "events", (stats.deterioration_events_count || 0) ? "warning" : "success"])}
    ${renderKpi(["عدد الاستجابات", stats.responses_count ?? 0, "clinical_responses", "info"])}
    ${renderKpi(["عدد المآلات", stats.outcomes_count ?? 0, "clinical_outcomes", "success"])}
    ${renderKpi(["نسبة اكتمال البيانات", `${stats.completion_rate ?? quality.qualityScore ?? 0}%`, "quality score", (stats.completion_rate || quality.qualityScore || 0) >= 80 ? "success" : "warning"])}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("المشاكل حسب النوع", renderQualityIssuesTable(quality.issuesByType || {}))}
    ${card("توزيع الجاهزية", renderBarChart([stats.dataset_rows || 0, stats.news2_alerts_count || 0, stats.deterioration_events_count || 0, stats.responses_count || 0, stats.outcomes_count || 0]))}
  </div>`;
}

function renderOutcomeAnalytics() {
  if (appState.loading.outcomeSummary || appState.loading.clinicalOutcomes) return loadingBlock("جاري تحميل تحليلات المآلات...");
  const s = appState.outcomeSummary || {};
  const outcomes = appState.clinicalOutcomes || [];
  const values = [
    s.stableCompletedSessionCount || 0,
    s.sessionStoppedEarlyCount || 0,
    s.hospitalAdmissionCount || 0,
    s.emergencyDepartmentTransferCount || 0,
    s.icuAdmissionCount || 0,
    s.deathCount || 0
  ];
  return `<div class="grid cols-4">
    ${renderKpi(["إجمالي المآلات", s.totalOutcomes ?? outcomes.length, "clinical_outcomes", "info"])}
    ${renderKpi(["استقرار واستكمال الجلسة", s.stableCompletedSessionCount ?? 0, "مآل مستقر", "success"])}
    ${renderKpi(["إدخال إلى المستشفى", s.hospitalAdmissionCount ?? 0, "مؤشر بحثي", (s.hospitalAdmissionCount || 0) ? "warning" : "success"])}
    ${renderKpi(["تحويل إلى الطوارئ", s.emergencyDepartmentTransferCount ?? 0, "مؤشر تصعيد", (s.emergencyDepartmentTransferCount || 0) ? "warning" : "success"])}
    ${renderKpi(["العناية المركزة", s.icuAdmissionCount ?? 0, "مآل حرج", (s.icuAdmissionCount || 0) ? "danger" : "success"], (s.icuAdmissionCount || 0) > 0)}
    ${renderKpi(["الوفيات", s.deathCount ?? 0, "مآل نهائي", (s.deathCount || 0) ? "danger" : "success"], (s.deathCount || 0) > 0)}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("توزيع المآلات", renderBarChart(values))}
    ${card("المآلات حسب الفترة", renderOutcomeWindowTable(outcomes))}
  </div>
  <div style="margin-top:16px">${card("آخر المآلات المسجلة", outcomes.length ? renderTable(["المريض", "NEWS2", "نوع التدهور", "نوع المآل", "الفترة", "وقت التسجيل"], outcomes.slice(0, 8).map((outcome) => [outcome.patientCode, outcome.news2TotalScore ?? "-", label(labels.deteriorationType, outcome.deteriorationType), label(labels.outcomeType, outcome.outcomeType), `${outcome.outcomeWindowHours} ساعة`, formatDateTime(outcome.createdAt)])) : emptyBlock("لا توجد مآلات لتحليلها حتى الآن"))}</div>`;
}

function renderOutcomeWindowTable(outcomes) {
  const windows = [24, 48, 72].map((windowHours) => {
    const rows = outcomes.filter((outcome) => outcome.outcomeWindowHours === windowHours);
    return [`${windowHours} ساعة`, rows.length, rows.filter((outcome) => outcome.outcomeType === "stable_completed_session").length, rows.filter((outcome) => ["hospital_admission", "emergency_department_transfer", "icu_admission", "death"].includes(outcome.outcomeType)).length];
  });
  return renderTable(["الفترة", "الإجمالي", "مستقر", "تصعيد / مآل حرج"], windows);
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

function renderExport() {
  if (appState.loading.researchDatasetRows || appState.loading.researchDatasetQuality) return loadingBlock("جاري تحميل مركز التصدير البحثي...");
  const rows = appState.researchDatasetRows || [];
  const quality = appState.researchDatasetQuality || {};
  return `<div class="dashboard-hero">
    <div class="hero-band">
      <h2>مركز التصدير البحثي</h2>
      <p>تجهيز Dataset بحثية محمية الخصوصية بصيغ CSV و Excel مع Codebook و Variable Labels جاهزة للتحضير في SPSS.</p>
    </div>
    <div class="status-panel">
      ${renderKpi(["درجة جودة البيانات", `${quality.qualityScore ?? 0}%`, "جاهزية البيانات البحثية", (quality.qualityScore || 0) >= 80 ? "success" : "warning"])}
      ${renderKpi(["عدد السجلات", quality.totalRows ?? rows.length, "سجلات Dataset", "info"])}
    </div>
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("فلاتر Dataset", renderExportFilters())}
    ${card("تنزيل ملفات التصدير", renderExportButtons())}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("جاهزية البيانات البحثية", renderQualityPanel(quality))}
    ${card("تنبيهات قبل التصدير", renderQualityWarnings(quality.warnings || []))}
  </div>
  <div style="margin-top:16px">${card("Dataset Preview", rows.length ? renderTable(["patient_code", "session_date", "measurement_time", "news2_total_score", "risk_level", "alert_created", "deterioration_type", "response_delay_minutes", "outcome_type", "study_phase", "study_group"], rows.map(datasetPreviewRow)) : emptyBlock("لا توجد سجلات مطابقة للفلاتر المحددة"))}</div>`;
}

function renderExportFilters() {
  const filters = appState.researchExportFilters || {};
  return `<form class="form-grid" onsubmit="submitResearchExportFilters(event)">
    <div class="field"><label>من تاريخ</label><input name="start_date" type="date" value="${escapeHtml(filters.start_date || "")}"></div>
    <div class="field"><label>إلى تاريخ</label><input name="end_date" type="date" value="${escapeHtml(filters.end_date || "")}"></div>
    <div class="field"><label>مرحلة الدراسة</label><select name="study_phase"><option value="">الكل</option><option value="pre_implementation" ${filters.study_phase === "pre_implementation" ? "selected" : ""}>قبل التطبيق</option><option value="post_implementation" ${filters.study_phase === "post_implementation" ? "selected" : ""}>بعد التطبيق</option></select></div>
    <div class="field"><label>مجموعة الدراسة</label><select name="study_group"><option value="">الكل</option><option value="control" ${filters.study_group === "control" ? "selected" : ""}>ضابطة</option><option value="intervention" ${filters.study_group === "intervention" ? "selected" : ""}>تدخل</option></select></div>
    <div class="field"><label>مستوى الخطورة</label><select name="risk_level"><option value="">الكل</option><option value="low" ${filters.risk_level === "low" ? "selected" : ""}>منخفض</option><option value="medium" ${filters.risk_level === "medium" ? "selected" : ""}>متوسط</option><option value="high" ${filters.risk_level === "high" ? "selected" : ""}>مرتفع</option></select></div>
    <div class="field"><label>نوع المآل</label><select name="outcome_type"><option value="">الكل</option>${Object.entries(labels.outcomeType).map(([value, text]) => `<option value="${value}" ${filters.outcome_type === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="field full"><label>نوع التدهور</label><select name="deterioration_type"><option value="">الكل</option>${Object.entries(labels.deteriorationType).map(([value, text]) => `<option value="${value}" ${filters.deterioration_type === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="footer-actions full"><button class="btn primary" type="submit">تطبيق الفلاتر</button><button class="btn" type="button" onclick="clearResearchExportFilters()">إلغاء الفلاتر</button></div>
  </form>`;
}

function renderExportButtons() {
  if (!hasPermission("research:export")) {
    return `<div class="state-message warning"><strong>ليست لديك صلاحية تصدير البيانات البحثية</strong><span>استخدم الدور التجريبي Admin أو Researcher لاختبار التصدير قبل مرحلة المصادقة.</span></div>`;
  }
  return `<div class="footer-actions">
    <button class="btn primary" onclick="downloadResearchExport('csv')">تصدير CSV</button>
    <button class="btn primary" onclick="downloadResearchExport('xlsx')">تصدير Excel</button>
    <button class="btn" onclick="downloadResearchExport('spss-codebook')">تحميل Codebook لـ SPSS</button>
    <button class="btn" onclick="downloadResearchExport('spss-variable-labels')">تحميل Variable Labels لـ SPSS</button>
  </div><p class="kpi-meta">تم تجهيز ملف التصدير من API حقيقي مع استبعاد الأسماء ومعلومات الاتصال وكلمات المرور.</p>`;
}

function renderQualityPanel(quality) {
  return `<div class="grid cols-2">
    ${renderKpi(["درجة جودة البيانات", `${quality.qualityScore ?? 0}%`, "قابلة للمراجعة", (quality.qualityScore || 0) >= 80 ? "success" : "warning"])}
    ${renderKpi(["عدد السجلات", quality.totalRows ?? 0, "Dataset rows", "info"])}
    ${renderKpi(["عدد المشاكل", quality.issuesCount ?? 0, "مشاكل البيانات", (quality.issuesCount || 0) ? "warning" : "success"])}
  </div>${renderQualityIssuesTable(quality.issuesByType || {})}`;
}

function renderQualityIssuesTable(issuesByType) {
  const rows = Object.entries(issuesByType).map(([type, count]) => [qualityIssueLabel(type), count]);
  return rows.length ? renderTable(["المشاكل حسب النوع", "العدد"], rows) : emptyBlock("لا توجد مشاكل جودة ظاهرة");
}

function renderQualityWarnings(warnings) {
  if (!warnings.length) return emptyBlock("لا توجد تنبيهات جودة قبل التصدير");
  return `<div class="timeline">${warnings.map((warning) => `<div class="timeline-item"><strong>تنبيه جودة</strong><span>${escapeHtml(warning)}</span></div>`).join("")}</div>`;
}

function datasetPreviewRow(row) {
  return [
    row.patientCode,
    row.sessionDate,
    formatDateTime(row.measurementTime),
    row.news2TotalScore,
    badge(riskLevelLabel(row.riskLevel), riskTone(row.riskLevel), row.riskLevel === "high" || row.riskLevel === "critical"),
    row.alertCreated ? "نعم" : "لا",
    label(labels.deteriorationType, row.deteriorationType),
    minuteText(row.responseDelayMinutes),
    label(labels.outcomeType, row.outcomeType),
    label(labels.studyPhase, row.studyPhase),
    label(labels.studyGroup, row.studyGroup)
  ];
}

function qualityIssueLabel(type) {
  return label({
    missing_patient_code: "رمز المريض مفقود",
    missing_session: "الجلسة مفقودة",
    missing_measurement_time: "وقت القياس مفقود",
    missing_news2_total_score: "درجة NEWS2 مفقودة",
    invalid_timestamp_sequence: "تسلسل زمني غير صالح",
    missing_outcome_for_deterioration: "مآل مفقود بعد التدهور",
    alert_without_response: "تنبيه بدون استجابة",
    response_without_tracking: "استجابة بدون تتبع",
    duplicate_dataset_rows: "سجلات مكررة"
  }, type);
}

async function submitResearchExportFilters(event) {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  appState.researchExportFilters = Object.fromEntries([...data.entries()].filter(([, value]) => value !== ""));
  appState.loading.researchDatasetRows = true;
  appState.loading.researchDatasetQuality = true;
  appState.errors.researchDatasetRows = null;
  appState.errors.researchDatasetQuality = null;
  render();
  try {
    appState.researchDatasetRows = await api.getResearchDataset(appState.researchExportFilters);
    appState.researchDatasetQuality = await api.getResearchDatasetQuality(appState.researchExportFilters);
  } catch (error) {
    appState.errors.researchDatasetRows = error.message || "تعذر تحميل البيانات البحثية";
  } finally {
    appState.loading.researchDatasetRows = false;
    appState.loading.researchDatasetQuality = false;
    render();
  }
}

async function clearResearchExportFilters() {
  appState.researchExportFilters = {};
  appState.researchDatasetRows = [];
  appState.researchDatasetQuality = null;
  await Promise.all([
    loadResource("researchDatasetRows", () => api.getResearchDataset({})),
    loadResource("researchDatasetQuality", () => api.getResearchDatasetQuality({}))
  ]);
}

function downloadResearchExport(format) {
  if (!hasPermission("research:export")) {
    appState.errors.researchDatasetRows = "ليست لديك صلاحية تصدير البيانات البحثية";
    render();
    return;
  }
  const endpoints = {
    csv: "/api/research/export/csv",
    xlsx: "/api/research/export/xlsx",
    "spss-codebook": "/api/research/export/spss-codebook",
    "spss-variable-labels": "/api/research/export/spss-variable-labels"
  };
  const endpoint = endpoints[format];
  if (!endpoint) return;
  window.location.href = `${endpoint}${queryString(appState.researchExportFilters || {})}`;
}

function renderResearchAnalyticsDashboard() {
  if (appState.loading.researchAnalyticsSummary) return loadingBlock("جاري تحميل التحليلات البحثية...");
  if (appState.errors.researchAnalyticsSummary) return errorBlock("researchAnalyticsSummary");
  const analytics = appState.researchAnalyticsSummary;
  if (!analytics) return emptyBlock("لا توجد بيانات كافية للتحليل");
  const k = analytics.kpis || {};
  const outcome = analytics.outcomeAnalysis || {};
  const response = analytics.responseTimeAnalysis || {};
  return `<div class="dashboard-hero">
    <div class="hero-band">
      <h2>لوحة التحليلات البحثية</h2>
      <p>تحليلات وصفية مبنية على Dataset البحثية دون اختبارات استدلالية أو تنبؤات.</p>
    </div>
    <div class="status-panel">
      ${renderKpi(["جاهزية البحث", k.export_readiness || "needs_review", "جاهزية التصدير", k.export_readiness === "ready" ? "success" : "warning"])}
      ${renderKpi(["جودة البيانات", `${k.dataset_quality_score ?? 0}%`, "Dataset Quality", (k.dataset_quality_score || 0) >= 80 ? "success" : "warning"])}
    </div>
  </div>
  <div class="grid cols-4">
    ${renderKpi(["عدد المرضى", k.total_patients ?? 0, "patients", "info"])}
    ${renderKpi(["عدد الجلسات", k.total_sessions ?? 0, "sessions", "info"])}
    ${renderKpi(["عدد القياسات", k.total_measurements ?? 0, "measurements", "info"])}
    ${renderKpi(["عدد تقييمات NEWS2", k.total_news2_assessments ?? 0, "NEWS2", "info"])}
    ${renderKpi(["عدد التنبيهات", k.total_alerts ?? 0, "alerts", (k.total_alerts || 0) ? "warning" : "success"])}
    ${renderKpi(["عدد أحداث التدهور", k.total_deterioration_events ?? 0, "events", (k.total_deterioration_events || 0) ? "warning" : "success"])}
    ${renderKpi(["عدد الاستجابات", k.total_responses ?? 0, "responses", "info"])}
    ${renderKpi(["عدد المآلات", k.total_outcomes ?? 0, "outcomes", "success"])}
    ${renderKpi(["متوسط NEWS2", k.average_news2_score ?? "-", "descriptive", (k.average_news2_score || 0) >= 7 ? "danger" : "info"])}
    ${renderKpi(["متوسط زمن الاستجابة", minuteText(k.average_response_time_minutes), "minutes", responseTone(k.average_response_time_minutes)])}
    ${renderKpi(["معدل التدهور", `${k.deterioration_rate ?? 0}%`, "events / sessions", (k.deterioration_rate || 0) ? "warning" : "success"])}
    ${renderKpi(["اكتمال الاستجابات", `${k.response_completion_rate ?? 0}%`, "responses / alerts", (k.response_completion_rate || 0) >= 80 ? "success" : "warning"])}
    ${renderKpi(["اكتمال المآلات", `${k.outcome_completion_rate ?? 0}%`, "outcomes / events", (k.outcome_completion_rate || 0) >= 80 ? "success" : "warning"])}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("تحليل NEWS2", renderDistributionTable(["الفئة", "العدد", "النسبة"], analytics.news2Distribution, "label"))}
    ${card("NEWS2 Score Distribution", renderBarChart((analytics.news2Distribution || []).map((item) => item.count || 0)))}
    ${card("تحليل المآلات", renderOutcomeAnalysisTable(outcome))}
    ${card("Outcome Distribution", renderBarChart((outcome.distribution || []).map((item) => item.count || 0)))}
    ${card("تحليل الاستجابة", renderResponseAnalysisTable(response))}
    ${card("Response Time Metrics", renderBarChart([response.average_time_to_alert || 0, response.average_time_to_view || 0, response.average_time_to_response || 0, response.average_time_to_action || 0, response.average_total_response_time || 0]))}
    ${card("تحليل التدهور السريري", renderDeteriorationAnalyticsTable(analytics.deteriorationAnalysis || []))}
    ${card("Deterioration Type Distribution", renderBarChart((analytics.deteriorationAnalysis || []).map((item) => item.count || 0)))}
    ${card("Risk Analytics", renderRiskAnalyticsTable(analytics.riskLevelDistribution || []))}
    ${card("مقارنة المجموعات", renderGroupComparisonTable(analytics.groupComparison || {}))}
  </div>
  <div style="margin-top:16px">${card("Research Readiness", renderTable(["المؤشر", "القيمة"], [["Dataset Quality", `${k.dataset_quality_score ?? 0}%`], ["Outcome Completion", `${k.outcome_completion_rate ?? 0}%`], ["Response Completion", `${k.response_completion_rate ?? 0}%`], ["Export Readiness", k.export_readiness || "needs_review"], ["Alerts per 100 sessions", k.alerts_per_100_sessions ?? 0]]))}</div>`;
}

function renderDistributionTable(headers, items, labelKey) {
  const rows = (items || []).map((item) => [item[labelKey] || item.bucket || item.risk_level || "-", item.count ?? 0, `${item.percentage ?? 0}%`]);
  return rows.length ? renderTable(headers, rows) : emptyBlock("لا توجد بيانات كافية للتحليل");
}

function renderOutcomeAnalysisTable(outcome) {
  const rows = (outcome.distribution || []).map((item) => [label(labels.outcomeType, item.outcome_type), item.count ?? 0, `${item.percentage ?? 0}%`]);
  rows.push(["Good outcome rate", `${outcome.good_outcome_rate ?? 0}%`, "stable_completed_session"]);
  rows.push(["Adverse outcome rate", `${outcome.adverse_outcome_rate ?? 0}%`, "admission / transfer / ICU / death"]);
  return rows.length ? renderTable(["المآل", "القيمة", "النسبة / الملاحظة"], rows) : emptyBlock("لا توجد مآلات للتحليل");
}

function renderResponseAnalysisTable(response) {
  return renderTable(["المؤشر", "الدقائق"], [
    ["average_time_to_alert", minuteText(response.average_time_to_alert)],
    ["average_time_to_view", minuteText(response.average_time_to_view)],
    ["average_time_to_response", minuteText(response.average_time_to_response)],
    ["average_time_to_action", minuteText(response.average_time_to_action)],
    ["average_total_response_time", minuteText(response.average_total_response_time)],
    ["fastest_response", minuteText(response.fastest_response)],
    ["slowest_response", minuteText(response.slowest_response)],
    ["median_response", minuteText(response.median_response)]
  ]);
}

function renderDeteriorationAnalyticsTable(items) {
  const rows = items.map((item) => [label(labels.deteriorationType, item.deterioration_type), item.count ?? 0, `${item.percentage ?? 0}%`, Object.entries(item.associated_outcomes || {}).filter(([, count]) => count).map(([key, count]) => `${label(labels.outcomeType, key)}: ${count}`).join(", ") || "-"]);
  return rows.length ? renderTable(["نوع التدهور", "العدد", "النسبة", "المآلات المرتبطة"], rows) : emptyBlock("لا توجد أحداث تدهور للتحليل");
}

function renderRiskAnalyticsTable(items) {
  const rows = items.map((item) => [riskLevelLabel(item.risk_level), item.count ?? 0, `${item.percentage ?? 0}%`, minuteText(item.average_response_time)]);
  return rows.length ? renderTable(["مستوى الخطورة", "العدد", "النسبة", "متوسط الاستجابة"], rows) : emptyBlock("لا توجد بيانات خطورة للتحليل");
}

function renderGroupComparisonTable(groupComparison) {
  const studyGroup = groupComparison.study_group || {};
  const groupA = studyGroup.group_a || {};
  const groupB = studyGroup.group_b || {};
  return renderTable(["المجموعة", "العدد", "متوسط NEWS2", "متوسط الاستجابة"], [
    [groupA.name || "-", groupA.count ?? 0, groupA.average_news2 ?? "-", minuteText(groupA.average_response_time)],
    [groupB.name || "-", groupB.count ?? 0, groupB.average_news2 ?? "-", minuteText(groupB.average_response_time)]
  ]);
}

function renderStudyCenter(route) {
  if (appState.loading.studyCenter) return loadingBlock("جاري تحميل مركز إدارة الدراسة...");
  if (appState.errors.studyCenter) return errorBlock("studyCenter");
  const study = currentStudy();
  if (route.id === "research-protocol") return renderResearchProtocol(study);
  if (route.id === "study-timeline") return renderStudyTimeline(study);
  if (route.id === "study-readiness") return renderStudyReadiness(study);
  return renderStudyManagement(study);
}

function currentStudy() {
  return appState.studies.find((study) => study.id === appState.selectedStudyId) || appState.studies[0] || null;
}

function renderStudyManagement(study) {
  const readiness = appState.studyReadiness;
  const dashboard = readiness?.dashboard || {};
  return `<div class="dashboard-hero">
    <div class="hero-band"><h2>${escapeHtml(study?.studyTitle || "مركز إدارة الدراسة")}</h2><p>طبقة حوكمة بحثية لتعريف البروتوكول ومراقبة جاهزية Dataset والتحليلات والتصدير والمآلات.</p></div>
    <div class="status-panel">${renderKpi(["درجة الجاهزية", `${readiness?.readinessScore ?? 0}%`, "Study Readiness", readinessTone(readiness?.readinessScore ?? 0)])}${renderKpi(["حالة الدراسة", label(labels.studyStatus, study?.studyStatus), "research_studies", study?.studyStatus === "active" ? "success" : "warning"])}</div>
  </div>
  <div class="grid cols-4">
    ${renderKpi(["عنوان الدراسة", study?.studyTitle || "-", "Study Title", "info"])}
    ${renderKpi(["الباحث الرئيسي", study?.principalInvestigator || "-", "Principal Investigator", "info"])}
    ${renderKpi(["تصميم الدراسة", label(labels.studyDesign, study?.studyDesign), "Study Design", "info"])}
    ${renderKpi(["حجم العينة المستهدف", dashboard.target_sample_size ?? study?.targetSampleSize ?? "-", "Target Sample Size", "info"])}
    ${renderKpi(["المرضى الحاليون", dashboard.current_patients ?? 0, "Current Patients", "info"])}
    ${renderKpi(["صفوف Dataset", dashboard.dataset_rows ?? 0, "Dataset Rows", "info"])}
    ${renderKpi(["حالة التحليلات", readinessStatusLabel(dashboard.analytics_status), "Analytics Status", dashboard.analytics_status === "ready" ? "success" : "warning"])}
    ${renderKpi(["جاهزية التصدير", readinessStatusLabel(dashboard.export_readiness), "Export Readiness", dashboard.export_readiness === "ready" ? "success" : "warning"])}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("إعداد البروتوكول", renderStudyForm(study))}
    ${card("الدراسات المسجلة", renderStudiesTable())}
    ${card("جاهزية البحث", renderReadinessChecks(readiness))}
    ${card("توصيات الجاهزية", renderReadinessList(readiness?.recommendations || [], "لا توجد توصيات تشغيلية حالية"))}
  </div>`;
}

function renderResearchProtocol(study) {
  const protocol = appState.studyReadiness?.protocol || {};
  return `<div class="grid cols-2">
    ${card("هدف الدراسة", renderTable(["البند", "القيمة"], [["Study Objective", protocol.study_objective || study?.studyDescription || "-"], ["Study Design", label(labels.studyDesign, protocol.study_design || study?.studyDesign)], ["Baseline Period", periodText(study?.baselinePeriodStart, study?.baselinePeriodEnd)], ["Intervention Period", periodText(study?.interventionPeriodStart, study?.interventionPeriodEnd)]]))}
    ${card("معايير وملاحظات البحث", renderTable(["البند", "القيمة"], [["Inclusion Notes", study?.inclusionNotes || "-"], ["Exclusion Notes", study?.exclusionNotes || "-"], ["Research Notes", study?.notes || "-"]]))}
  </div>`;
}

function renderStudyTimeline(study) {
  const timeline = appState.studyReadiness?.timeline || {};
  const items = [["Study Start", timeline.study_start || study?.studyStartDate], ["Baseline Period", periodText(study?.baselinePeriodStart, study?.baselinePeriodEnd)], ["Intervention Period", periodText(study?.interventionPeriodStart, study?.interventionPeriodEnd)], ["Current Date", timeline.current_date], ["Study End", timeline.study_end || study?.studyEndDate]];
  return card("الخط الزمني للدراسة", `<div class="timeline">${items.map(([title, value]) => `<div class="timeline-item"><strong>${escapeHtml(title)}</strong><span>${escapeHtml(value || "-")}</span></div>`).join("")}</div>`);
}

function renderStudyReadiness(study) {
  const readiness = appState.studyReadiness;
  return `<div class="grid cols-3">
    ${renderKpi(["Dataset Ready", yesNo(readiness?.checks?.dataset_available), "Dataset", readiness?.checks?.dataset_available ? "success" : "warning"])}
    ${renderKpi(["Analytics Ready", yesNo(readiness?.checks?.analytics_available), "Analytics", readiness?.checks?.analytics_available ? "success" : "warning"])}
    ${renderKpi(["Exports Ready", yesNo(readiness?.checks?.exports_available), "Exports", readiness?.checks?.exports_available ? "success" : "warning"])}
    ${renderKpi(["Outcomes Ready", yesNo(readiness?.checks?.outcomes_available), "Outcomes", readiness?.checks?.outcomes_available ? "success" : "warning"])}
    ${renderKpi(["Tracking Ready", yesNo(readiness?.checks?.response_tracking_available), "Tracking", readiness?.checks?.response_tracking_available ? "success" : "warning"])}
    ${renderKpi(["Overall Readiness", `${readiness?.readinessScore ?? 0}%`, study?.studyTitle || "Study", readinessTone(readiness?.readinessScore ?? 0)])}
  </div>
  <div class="grid cols-2" style="margin-top:16px">
    ${card("تفاصيل الجاهزية", renderReadinessChecks(readiness))}
    ${card("المتطلبات الناقصة", renderReadinessList((readiness?.missingRequirements || []).map((item) => label(labels.readinessCheck, item)), "لا توجد متطلبات ناقصة"))}
    ${card("تحذيرات", renderReadinessList(readiness?.warnings || [], "لا توجد تحذيرات جاهزية"))}
    ${card("توصيات", renderReadinessList(readiness?.recommendations || [], "لا توجد توصيات حالية"))}
  </div>`;
}

function renderStudyForm(study) {
  const canManageStudy = study ? hasPermission("studies:update") : hasPermission("studies:create");
  return `<form class="form-grid" onsubmit="submitStudyForm(event)">
    <div class="field"><label>رمز الدراسة</label><input name="study_code" required value="${escapeHtml(study?.studyCode || "NEWS2-HD-001")}"></div>
    <div class="field"><label>عنوان الدراسة</label><input name="study_title" required value="${escapeHtml(study?.studyTitle || "")}"></div>
    <div class="field"><label>الباحث الرئيسي</label><input name="principal_investigator" value="${escapeHtml(study?.principalInvestigator || "")}"></div>
    <div class="field"><label>تصميم الدراسة</label><select name="study_design">${Object.entries(labels.studyDesign).map(([value, text]) => `<option value="${value}" ${study?.studyDesign === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="field"><label>حالة الدراسة</label><select name="study_status">${Object.entries(labels.studyStatus).map(([value, text]) => `<option value="${value}" ${study?.studyStatus === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="field"><label>حجم العينة المستهدف</label><input name="target_sample_size" type="number" min="1" value="${escapeHtml(study?.targetSampleSize || "")}"></div>
    <div class="field"><label>بداية الدراسة</label><input name="study_start_date" type="date" value="${escapeHtml(study?.studyStartDate || "")}"></div>
    <div class="field"><label>نهاية الدراسة</label><input name="study_end_date" type="date" value="${escapeHtml(study?.studyEndDate || "")}"></div>
    <div class="field"><label>بداية خط الأساس</label><input name="baseline_period_start" type="date" value="${escapeHtml(study?.baselinePeriodStart || "")}"></div>
    <div class="field"><label>نهاية خط الأساس</label><input name="baseline_period_end" type="date" value="${escapeHtml(study?.baselinePeriodEnd || "")}"></div>
    <div class="field"><label>بداية التدخل</label><input name="intervention_period_start" type="date" value="${escapeHtml(study?.interventionPeriodStart || "")}"></div>
    <div class="field"><label>نهاية التدخل</label><input name="intervention_period_end" type="date" value="${escapeHtml(study?.interventionPeriodEnd || "")}"></div>
    <div class="field full"><label>وصف الدراسة</label><textarea name="study_description">${escapeHtml(study?.studyDescription || "")}</textarea></div>
    <div class="field full"><label>ملاحظات الاشتمال</label><textarea name="inclusion_notes">${escapeHtml(study?.inclusionNotes || "")}</textarea></div>
    <div class="field full"><label>ملاحظات الاستبعاد</label><textarea name="exclusion_notes">${escapeHtml(study?.exclusionNotes || "")}</textarea></div>
    <div class="field full"><label>ملاحظات البحث</label><textarea name="notes">${escapeHtml(study?.notes || "")}</textarea></div>
    ${appState.studySubmission ? `<div class="state-message success full"><strong>${escapeHtml(appState.studySubmission)}</strong></div>` : ""}
    <div class="footer-actions full"><button class="btn primary" type="submit">${study ? "تحديث الدراسة" : "إنشاء الدراسة"}</button></div>
  </form>`;
}

function renderStudiesTable() {
  const rows = appState.studies.map((study) => [study.studyCode, study.studyTitle, study.principalInvestigator, label(labels.studyDesign, study.studyDesign), badge(label(labels.studyStatus, study.studyStatus), study.studyStatus === "active" ? "success" : "warning")]);
  return rows.length ? renderTable(["الرمز", "العنوان", "الباحث", "التصميم", "الحالة"], rows) : emptyBlock("لا توجد دراسة معرفة حتى الآن");
}

function renderReadinessChecks(readiness) {
  const checks = readiness?.checks || {};
  const rows = Object.entries(labels.readinessCheck).map(([key, text]) => [text, yesNo(checks[key]), badge(checks[key] ? "جاهز" : "غير مكتمل", checks[key] ? "success" : "warning")]);
  return renderTable(["المتطلب", "الحالة", "المؤشر"], rows);
}

function renderReadinessList(items, emptyText) {
  if (!items.length) return emptyBlock(emptyText);
  return `<div class="timeline">${items.map((item) => `<div class="timeline-item"><strong>${escapeHtml(item)}</strong></div>`).join("")}</div>`;
}

function readinessTone(score) {
  if (score >= 80) return "success";
  if (score >= 50) return "warning";
  return "danger";
}

function readinessStatusLabel(value) {
  return label({ ready: "جاهز", needs_review: "يحتاج مراجعة", not_ready: "غير جاهز" }, value);
}

function yesNo(value) {
  return value ? "نعم" : "لا";
}

function periodText(start, end) {
  return `${start || "-"} / ${end || "-"}`;
}

async function submitStudyForm(event) {
  event.preventDefault();
  const study = currentStudy();
  if (study ? !hasPermission("studies:update") : !hasPermission("studies:create")) {
    appState.errors.studyCenter = "ليست لديك صلاحية تعديل إعدادات الدراسة";
    render();
    return;
  }
  const data = new FormData(event.currentTarget);
  const payload = Object.fromEntries([...data.entries()].filter(([, value]) => value !== ""));
  if (payload.target_sample_size) payload.target_sample_size = Number(payload.target_sample_size);
  appState.loading.studyCenter = true;
  appState.errors.studyCenter = null;
  render();
  try {
    const saved = study ? await api.updateStudy(study.id, payload) : await api.createStudy(payload);
    appState.selectedStudyId = saved.id;
    appState.studySubmission = "تم حفظ إعدادات الدراسة";
    appState.studyCenter = await loadStudyCenter();
  } catch (error) {
    appState.errors.studyCenter = error.message || "تعذر حفظ إعدادات الدراسة";
  } finally {
    appState.loading.studyCenter = false;
    render();
  }
}

function renderPermissions() {
  const matrix = appState.permissionMatrix || { roles: [], permissions: [] };
  const roles = matrix.roles || [];
  const headers = ["الصلاحية", ...roles.map((role) => role.role_label || role.role)];
  const rows = (matrix.permissions || []).map((permission) => [
    permissionLabel(permission),
    ...roles.map((role) => (role.permissions || []).includes(permission) ? badge("مسموح", "success") : badge("ممنوع", "warning"))
  ]);
  return `<div class="grid cols-2">${renderKpi(["الدور الحالي", appState.currentRoleLabel, "Session RBAC", "info"])}${renderKpi(["عدد الصلاحيات", appState.permissions.length, "Current permissions", "info"])}</div><div style="margin-top:16px">${card("مصفوفة الصلاحيات", rows.length ? renderTable(headers, rows) : emptyBlock("لم يتم تحميل مصفوفة الصلاحيات"))}</div>`;
}

function renderRolesMatrix() {
  const roles = appState.permissionMatrix?.roles || [];
  const rows = roles.map((role) => [
    role.role_label,
    permissionGroupSummary(role.permissions || []),
    (role.permissions || []).length,
    role.role === appState.currentRole ? badge("الدور الحالي", "info") : "-"
  ]);
  return card("الأدوار", rows.length ? renderTable(["الدور", "مجموعات الصلاحيات", "عدد الصلاحيات", "الحالة"], rows) : emptyBlock("لم يتم تحميل الأدوار بعد"));
}

function permissionGroupSummary(permissions) {
  const groups = permissions.reduce((acc, permission) => {
    const [resource, action = "view"] = String(permission).split(":");
    if (!acc[resource]) acc[resource] = [];
    acc[resource].push(action);
    return acc;
  }, {});
  const rows = Object.entries(groups).map(([resource, actions]) => {
    const actionLabels = [...new Set(actions)].map(permissionActionLabel).join("، ");
    return `<span class="permission-group-line"><strong>${escapeHtml(permissionResourceLabel(resource))}:</strong> ${escapeHtml(actionLabels)}</span>`;
  });
  return rows.length ? `<span class="permission-groups" dir="rtl">${rows.join("")}</span>` : "-";
}

function permissionLabel(permission) {
  const [resource, action = "view"] = String(permission).split(":");
  return `${permissionResourceLabel(resource)}: ${permissionActionLabel(action)}`;
}

function permissionResourceLabel(resource) {
  const value = String(resource || "");
  return PERMISSION_RESOURCE_LABELS[value] || readablePermissionFallback(value);
}

function permissionActionLabel(action) {
  const value = String(action || "");
  return PERMISSION_ACTION_LABELS[value] || readablePermissionFallback(value);
}

function readablePermissionFallback(value) {
  return String(value || "-").replace(/_/g, " ");
}

async function changeDevRole(role) {
  if (!appState.allowDevRole) return;
  appState.currentRole = role;
  localStorage.setItem("news2DevRole", role);
  appState.researchDatasetRows = [];
  appState.researchDatasetQuality = null;
  appState.researchAnalyticsSummary = null;
  appState.studyCenter = null;
  appState.studyReadiness = null;
  await loadAuthContext();
  const route = routes.find((item) => item.id === currentRoute());
  if (route) ensureDataForRoute(route);
}

async function submitLogin(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  appState.loginError = null;
  try {
    const context = await api.login(payload);
    appState.currentUser = context;
    appState.isAuthenticated = true;
    appState.allowDevRole = context.allowDevRole === true;
    appState.currentRole = context.role;
    appState.currentRoleLabel = context.roleLabel;
    appState.permissions = context.permissions;
    if (hasPermission("rbac:view")) {
      try {
        appState.permissionMatrix = await api.getPermissionMatrix();
      } catch (error) {
        appState.errors.permissionMatrix = error.message;
      }
    }
    setRoute("dashboard");
  } catch (error) {
    appState.loginError = error.message || "تعذر تسجيل الدخول";
    clearAuthState();
    renderLogin();
  }
}

async function logout() {
  try {
    await api.logout();
  } catch (error) {
    appState.errors.auth = error.message;
  }
  clearAuthState();
  setRoute("login");
}

function renderStudyForm(study) {
  const canManageStudy = study ? hasPermission("studies:update") : hasPermission("studies:create");
  return `<form class="form-grid" onsubmit="submitStudyForm(event)">
    <div class="field"><label>رمز الدراسة</label><input name="study_code" required value="${escapeHtml(study?.studyCode || "NEWS2-HD-001")}"></div>
    <div class="field"><label>عنوان الدراسة</label><input name="study_title" required value="${escapeHtml(study?.studyTitle || "")}"></div>
    <div class="field"><label>الباحث الرئيسي</label><input name="principal_investigator" value="${escapeHtml(study?.principalInvestigator || "")}"></div>
    <div class="field"><label>تصميم الدراسة</label><select name="study_design">${Object.entries(labels.studyDesign).map(([value, text]) => `<option value="${value}" ${study?.studyDesign === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="field"><label>حالة الدراسة</label><select name="study_status">${Object.entries(labels.studyStatus).map(([value, text]) => `<option value="${value}" ${study?.studyStatus === value ? "selected" : ""}>${text}</option>`).join("")}</select></div>
    <div class="field"><label>حجم العينة المستهدف</label><input name="target_sample_size" type="number" min="1" value="${escapeHtml(study?.targetSampleSize || "")}"></div>
    <div class="field"><label>بداية الدراسة</label><input name="study_start_date" type="date" value="${escapeHtml(study?.studyStartDate || "")}"></div>
    <div class="field"><label>نهاية الدراسة</label><input name="study_end_date" type="date" value="${escapeHtml(study?.studyEndDate || "")}"></div>
    <div class="field"><label>بداية خط الأساس</label><input name="baseline_period_start" type="date" value="${escapeHtml(study?.baselinePeriodStart || "")}"></div>
    <div class="field"><label>نهاية خط الأساس</label><input name="baseline_period_end" type="date" value="${escapeHtml(study?.baselinePeriodEnd || "")}"></div>
    <div class="field"><label>بداية التدخل</label><input name="intervention_period_start" type="date" value="${escapeHtml(study?.interventionPeriodStart || "")}"></div>
    <div class="field"><label>نهاية التدخل</label><input name="intervention_period_end" type="date" value="${escapeHtml(study?.interventionPeriodEnd || "")}"></div>
    <div class="field full"><label>وصف الدراسة</label><textarea name="study_description">${escapeHtml(study?.studyDescription || "")}</textarea></div>
    <div class="field full"><label>ملاحظات الاشتمال</label><textarea name="inclusion_notes">${escapeHtml(study?.inclusionNotes || "")}</textarea></div>
    <div class="field full"><label>ملاحظات الاستبعاد</label><textarea name="exclusion_notes">${escapeHtml(study?.exclusionNotes || "")}</textarea></div>
    <div class="field full"><label>ملاحظات البحث</label><textarea name="notes">${escapeHtml(study?.notes || "")}</textarea></div>
    ${appState.studySubmission ? `<div class="state-message success full"><strong>${escapeHtml(appState.studySubmission)}</strong></div>` : ""}
    ${canManageStudy ? "" : `<div class="state-message warning full"><strong>ليست لديك صلاحية تعديل إعدادات الدراسة</strong></div>`}
    <div class="footer-actions full"><button class="btn primary" type="submit" ${canManageStudy ? "" : "disabled"}>${study ? "تحديث الدراسة" : "إنشاء الدراسة"}</button></div>
  </form>`;
}

function render() {
  applySidebarState();
  const routeState = parseCurrentRoute();
  const id = routeState.id;
  appState.selectedPatientId = id === "patient-profile" ? selectedPatientIdFromRoute(routeState.params) : appState.selectedPatientId;
  if (id === "login") {
    if (appState.isAuthenticated) setRoute("dashboard");
    else renderLogin();
    return;
  }
  if (!appState.isAuthenticated) {
    renderLogin();
    return;
  }
  const route = routes.find((item) => item.id === id) || routes[0];
  ensureDataForRoute(route);
  renderShell(route);
}

window.setRoute = setRoute;
window.calculateNews2Demo = calculateNews2Demo;
window.submitPatientCreate = submitPatientCreate;
window.submitStaffUser = submitStaffUser;
window.toggleStaffUserStatus = toggleStaffUserStatus;
window.submitMonitoringMeasurement = submitMonitoringMeasurement;
window.submitDeteriorationEvent = submitDeteriorationEvent;
window.submitClinicalResponse = submitClinicalResponse;
window.submitResearchExportFilters = submitResearchExportFilters;
window.clearResearchExportFilters = clearResearchExportFilters;
window.downloadResearchExport = downloadResearchExport;
window.submitStudyForm = submitStudyForm;
window.submitLogin = submitLogin;
window.logout = logout;
window.changeDevRole = changeDevRole;
window.handleActionKey = handleActionKey;
window.selectPatientProfile = selectPatientProfile;
window.showPatientProfileSelector = showPatientProfileSelector;
window.filterPatientProfileSelector = filterPatientProfileSelector;
window.openSidebar = openSidebar;
window.closeSidebar = closeSidebar;
window.toggleSidebar = toggleSidebar;
window.toggleNavGroup = toggleNavGroup;
window.closeMobileNav = closeMobileNav;
window.addEventListener("hashchange", render);
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeSidebar();
});
window.addEventListener("resize", () => {
  if (!isMobileNavMode()) document.body.classList.remove("nav-open");
  applySidebarState();
});
loadHealth();
loadAuthContext();
render();
