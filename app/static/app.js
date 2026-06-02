const routes = [
  { id: "dashboard", label: "لوحة التحكم", group: "الرصد السريري", icon: "D", type: "dashboard" },
  { id: "patients", label: "قائمة المرضى", group: "المرضى", icon: "P", type: "table", entity: "patients" },
  { id: "create-patient", label: "إضافة مريض", group: "المرضى", icon: "+", type: "form", entity: "patient" },
  { id: "patient-profile", label: "ملف المريض", group: "المرضى", icon: "ID", type: "profile" },
  { id: "patient-baseline", label: "الخط الأساسي", group: "المرضى", icon: "B", type: "baseline" },
  { id: "vascular-access", label: "الوصول الوعائي", group: "المرضى", icon: "V", type: "vascular" },
  { id: "sessions", label: "جلسات الغسيل", group: "الجلسات", icon: "S", type: "table", entity: "sessions" },
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

// Phase 03 integration boundary: replace static mock arrays below with fetch
// calls to read-only API endpoints such as /api/patients, /api/alerts, and
// /api/research/summary without changing the hash-based screen router.

const kpis = [
  ["مرضى تحت الرصد", "128", "زيادة 8 مرضى هذا الأسبوع", "info"],
  ["تنبيهات عالية الخطورة", "7", "تحتاج مراجعة خلال 15 دقيقة", "danger"],
  ["متوسط زمن الاستجابة", "11 د", "أفضل من الهدف التشغيلي", "success"],
  ["جلسات اليوم", "42", "31 مكتملة و 11 نشطة", "warning"]
];

const patients = [
  ["P-1024", "سارة محمود", "56", "ناسور شرياني وريدي", "NEWS2 2", "مستقر"],
  ["P-1088", "خالد يوسف", "64", "قسطرة وريدية مركزية", "NEWS2 6", "مرتفع"],
  ["P-1120", "نورا عادل", "48", "طعوم وعائي", "NEWS2 4", "متوسط"],
  ["P-1182", "محمد سالم", "71", "ناسور شرياني وريدي", "NEWS2 1", "مستقر"]
];

const genericRows = {
  sessions: [["S-2201", "P-1088", "08:00", "نشطة", "NEWS2 6", "مراجعة طبية"], ["S-2202", "P-1024", "10:30", "مكتملة", "NEWS2 2", "متابعة روتينية"], ["S-2203", "P-1182", "12:00", "مجدولة", "NEWS2 -", "قيد الانتظار"]],
  news2: [["N-771", "P-1088", "06:00", "3", "أصفر", "تمت المراجعة"], ["N-772", "P-1088", "08:30", "6", "أحمر", "تصعيد نشط"], ["N-773", "P-1024", "09:00", "2", "أخضر", "مستقر"]],
  events: [["E-310", "هبوط ضغط", "P-1088", "08:42", "عالي", "مفتوح"], ["E-311", "نقص أكسجة", "P-1120", "11:10", "متوسط", "مغلق"], ["E-312", "حمى", "P-1182", "13:20", "منخفض", "متابعة"]],
  medical: [["08:43", "طبيب كلى", "تقييم فوري", "تعديل معدل السحب", "مكتمل"], ["08:50", "استشاري", "مراجعة NEWS2", "خطة مراقبة", "نشط"]],
  nursing: [["08:41", "تمريض الجلسة", "إعادة قياس العلامات", "مكتمل"], ["08:45", "تمريض مسؤول", "إبلاغ الطبيب", "مكتمل"]],
  outcomes: [["O-120", "P-1088", "استقرار خلال الجلسة", "45 دقيقة", "بدون نقل"], ["O-121", "P-1120", "تصعيد متوسط", "70 دقيقة", "مراقبة إضافية"]],
  users: [["U-01", "د. أحمد منصور", "طبيب", "نشط", "آخر دخول اليوم"], ["U-02", "ليلى حسن", "تمريض", "نشط", "آخر دخول أمس"]],
  roles: [["طبيب", "18 صلاحية", "تقييم وتصعيد", "نشط"], ["تمريض", "14 صلاحية", "إدخال ومتابعة", "نشط"], ["باحث", "9 صلاحيات", "تحليلات وتصدير", "نشط"]],
  audit: [["09:10", "U-01", "تحديث تقييم NEWS2", "P-1088", "نجاح"], ["09:18", "U-02", "إدخال علامات حيوية", "P-1024", "نجاح"]]
};

const timelineItems = [
  ["08:30", "ارتفاع NEWS2 إلى 6", "تغير في معدل التنفس وضغط الدم مع إنذار عالي الخطورة."],
  ["08:35", "تأكيد تمريضي", "إعادة قياس العلامات الحيوية وتثبيت حالة الوصول الوعائي."],
  ["08:43", "تصعيد طبي", "تقييم الطبيب وتعديل خطة الجلسة ومعدل السحب."],
  ["09:05", "انخفاض درجة الخطورة", "تحسن تدريجي مع استمرار المراقبة كل 15 دقيقة."]
];

const formFields = {
  patient: ["الاسم الكامل", "رقم الملف", "تاريخ الميلاد", "الجنس", "نوع الوصول الوعائي", "الأمراض المصاحبة", "خطة الغسيل", "ملاحظات سريرية"],
  session: ["المريض", "تاريخ الجلسة", "وقت البدء", "الوزن قبل الجلسة", "معدل السحب", "الضغط الابتدائي", "حالة الوصول", "ملاحظات الفريق"],
  vitals: ["معدل التنفس", "تشبع الأكسجين", "ضغط الدم الانقباضي", "النبض", "درجة الحرارة", "مستوى الوعي", "الأكسجين الإضافي", "ملاحظات القياس"]
};

const subtitles = {
  dashboard: "رصد تشغيلي مباشر للمخاطر والتنبيهات وجودة الاستجابة.",
  patients: "إدارة ملفات مرضى الغسيل الكلوي مع مؤشرات الخطر الحالية.",
  "create-patient": "تسجيل مريض جديد مع بيانات سريرية أولية قابلة للتوسع.",
  "patient-profile": "ملف سريري موحد يربط الخط الأساسي والجلسات والتنبيهات.",
  "patient-baseline": "قيم مرجعية تساعد على تفسير تغير NEWS2 أثناء الجلسات.",
  "vascular-access": "توثيق حالة الوصول الوعائي ومخاطر العدوى والتدفق.",
  sessions: "متابعة الجلسات المجدولة والنشطة والمكتملة.",
  "create-session": "فتح جلسة غسيل جديدة مرتبطة بالمريض وخطة الرصد.",
  "session-details": "تفاصيل تشغيلية وسريرية للجلسة الحالية.",
  "intradialytic-monitoring": "مراقبة مستمرة للعلامات الحيوية ومؤشرات التدهور.",
  "vital-signs-entry": "إدخال العلامات الحيوية المطلوبة لحساب NEWS2.",
  "news2-assessment": "تقييم منظم لمكونات NEWS2 والتصعيد المرتبط بها.",
  "news2-trend": "اتجاهات NEWS2 عبر الجلسة والزيارات السابقة.",
  "news2-history": "سجل قياسات NEWS2 وإجراءات الاستجابة.",
  "active-alerts": "قائمة التنبيهات السريرية المفتوحة حسب الأولوية.",
  "alert-details": "سياق التنبيه والإجراءات المطلوبة ومؤشرات الخطر.",
  "alert-timeline": "تسلسل زمني للتنبيه منذ الاكتشاف حتى الإغلاق.",
  "deterioration-events": "أحداث تدهور موثقة لأغراض السلامة والبحث.",
  "event-details": "تفاصيل الحدث والربط مع الجلسة والمخرجات.",
  "event-timeline": "تسلسل سريري وتشغيلي للحدث.",
  "medical-response-log": "توثيق قرارات وتدخلات الفريق الطبي.",
  "nursing-response-log": "توثيق إجراءات التمريض أثناء التصعيد.",
  "response-workflow": "مسار الاستجابة من الاكتشاف إلى الإغلاق.",
  "response-time-dashboard": "مؤشرات سرعة الاستجابة والالتزام بالأهداف.",
  "response-analytics": "تحليل أنماط التصعيد والأداء التشغيلي.",
  "clinical-outcomes": "مخرجات سريرية مرتبطة بالجلسات والتنبيهات.",
  "outcome-tracking": "متابعة حالة المخرجات حتى الإغلاق.",
  "outcome-analytics": "تحليل أثر الرصد المبكر على النتائج السريرية.",
  "research-dashboard": "رؤية بحثية موحدة للبيانات والمؤشرات.",
  "pre-post-comparison": "مقارنة مؤشرات ما قبل وبعد تطبيق الرصد.",
  "study-metrics": "مؤشرات الدراسة وجودة البيانات والامتثال.",
  "dataset-statistics": "توزيع البيانات وحجم العينات ومعدلات الاكتمال.",
  "export-center": "تصدير آمن ومنظم للبيانات البحثية.",
  users: "إدارة المستخدمين المرتبطين بالمنصة.",
  roles: "إدارة أدوار العمل والصلاحيات المتصلة بها.",
  permissions: "مصفوفة صلاحيات وظيفية قابلة للمراجعة.",
  "audit-logs": "سجل تدقيق للإجراءات الحساسة داخل النظام.",
  "system-settings": "إعدادات تشغيلية عامة للمنصة.",
  "language-settings": "تهيئة اللغة والاتجاه مع دعم التوسع للإنجليزية."
};

const app = document.getElementById("app");

function currentRoute() {
  return location.hash.replace("#/", "") || "login";
}

function setRoute(routeId) {
  location.hash = `/${routeId}`;
}

function badge(text, tone = "neutral", critical = false) {
  return `<span class="badge ${tone} ${critical ? "critical" : ""}">${text}</span>`;
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
        <p class="subtitle">دخول آمن للفريق السريري والبحثي</p>
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
                <span class="nav-icon">${item.icon}</span>
                <span>${item.label}</span>
              </button>`).join("")}
          </nav>`).join("")}
      </aside>
      <main class="main">
        <header class="topbar">
          <button class="icon-btn mobile-toggle" onclick="document.body.classList.toggle('nav-open')" title="القائمة">☰</button>
          <div>
            <h1>${route.label}</h1>
            <p>${subtitles[route.id] || "واجهة سريرية متصلة ضمن نظام NEWS2."}</p>
          </div>
          <div class="top-actions">
            ${badge("RTL", "info")}
            ${badge("بحث سريري", "success")}
            <button class="icon-btn" title="التنبيهات" onclick="setRoute('active-alerts')">!</button>
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
    table: () => renderTableScreen(route),
    form: () => renderFormScreen(route),
    profile: renderProfile,
    baseline: renderBaseline,
    vascular: renderVascular,
    details: () => renderDetails(route),
    monitoring: renderMonitoring,
    assessment: renderAssessment,
    trend: renderTrend,
    alerts: renderAlerts,
    timeline: () => renderTimeline(route),
    workflow: () => renderWorkflow(route),
    analytics: () => renderAnalytics(route),
    research: renderResearch,
    comparison: renderComparison,
    export: renderExport,
    permissions: renderPermissions,
    settings: renderSettings,
    language: renderLanguage
  };
  return (renderers[route.type] || renderDashboard)();
}

function renderDashboard() {
  return `
    <div class="dashboard-hero">
      <div class="hero-band">
        <h2>رصد مبكر للتدهور السريري أثناء جلسات الغسيل الكلوي</h2>
        <p>واجهة موحدة تربط العلامات الحيوية وNEWS2 والتنبيهات والاستجابة السريرية والتحليلات البحثية في سياق تشغيلي واحد.</p>
      </div>
      <div class="status-panel">
        ${renderKpi(["الاستقرار العام", "94%", "التزام مرتفع ببروتوكول الرصد", "success"])}
        ${renderKpi(["تنبيه حرج", "1", "P-1088 يحتاج متابعة الآن", "danger"], true)}
      </div>
    </div>
    <div class="grid cols-4">${kpis.map((item) => renderKpi(item, item[3] === "danger")).join("")}</div>
    <div class="grid cols-2" style="margin-top:16px">
      ${card("منحنى NEWS2 اليوم", renderLineChart())}
      ${card("توزيع المخاطر", renderBarChart([42, 28, 18, 7]))}
    </div>
    <div style="margin-top:16px">${card("أحدث التنبيهات", renderTable(["المعرف", "المريض", "الوقت", "الخطورة", "الحالة"], genericRows.events))}</div>`;
}

function renderKpi(item, critical = false) {
  const [label, value, meta, tone] = item;
  return `<div class="card kpi ${critical ? "critical" : ""}"><div class="card-body"><div class="kpi-label">${label}</div><div class="kpi-value">${value}</div><div class="kpi-meta">${badge(meta, tone, critical)}</div></div></div>`;
}

function renderTableScreen(route) {
  const headers = tableHeaders(route.entity);
  const rows = route.entity === "patients" ? patients : genericRows[route.entity] || genericRows.sessions;
  return `
    <div class="grid cols-3">
      ${renderKpi(["إجمالي السجلات", String(rows.length * 24), "بيانات نشطة", "info"])}
      ${renderKpi(["مراجعات مفتوحة", "12", "تحتاج متابعة", "warning"])}
      ${renderKpi(["امتثال البيانات", "97%", "جودة عالية", "success"])}
    </div>
    <div style="margin-top:16px">${card(route.label, renderTable(headers, rows))}</div>`;
}

function tableHeaders(entity) {
  const map = {
    patients: ["الملف", "المريض", "العمر", "الوصول الوعائي", "NEWS2", "الحالة"],
    roles: ["الدور", "الصلاحيات", "النطاق", "الحالة"],
    audit: ["الوقت", "المستخدم", "الإجراء", "المرجع", "النتيجة"]
  };
  return map[entity] || ["المعرف", "المرجع", "الوقت", "الحالة", "المؤشر", "الإجراء"];
}

function renderTable(headers, rows) {
  return `<div class="table-wrap"><table><thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${formatCell(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function formatCell(cell) {
  const value = String(cell);
  if (value.includes("عالي") || value.includes("مرتفع") || value.includes("أحمر") || value.includes("NEWS2 6")) return badge(value, "danger", value.includes("NEWS2 6"));
  if (value.includes("متوسط") || value.includes("أصفر") || value.includes("متابعة")) return badge(value, "warning");
  if (value.includes("مستقر") || value.includes("مكتمل") || value.includes("نجاح") || value.includes("نشط")) return badge(value, "success");
  return value;
}

function renderFormScreen(route) {
  const fields = formFields[route.entity] || formFields.patient;
  return card(route.label, `
    <div class="form-grid">
      ${fields.map((field, index) => `
        <div class="field ${index === fields.length - 1 ? "full" : ""}">
          <label>${field}</label>
          ${index === fields.length - 1 ? `<textarea placeholder="${field}"></textarea>` : `<input placeholder="${field}">`}
        </div>`).join("")}
    </div>
    <div class="footer-actions">
      <button class="btn primary">حفظ</button>
      <button class="btn">حفظ كمسودة</button>
      <button class="btn">إلغاء</button>
    </div>`);
}

function renderProfile() {
  return `
    ${card("ملخص المريض", `<div class="patient-summary">${["الملف P-1088", "العمر 64", "NEWS2 الحالي 6", "الوصول قسطرة مركزية"].map((x) => `<div class="summary-cell"><span>${x.split(" ")[0]}</span><strong>${x.substring(x.indexOf(" ") + 1)}</strong></div>`).join("")}</div>`)}
    <div class="grid cols-2" style="margin-top:16px">${card("اتجاه NEWS2", renderLineChart())}${card("آخر الجلسات", renderTable(tableHeaders("sessions"), genericRows.sessions))}</div>`;
}

function renderBaseline() {
  return `<div class="grid cols-2">${card("القيم المرجعية", renderTable(["المؤشر", "القيمة المرجعية", "آخر قراءة", "التقييم"], [["ضغط الدم", "135/82", "118/70", "انخفاض"], ["النبض", "78", "96", "ارتفاع"], ["تشبع الأكسجين", "96%", "91%", "مراجعة"]]))}${card("سياق سريري", renderFormText(["الأمراض المصاحبة", "الأدوية المؤثرة", "ملاحظات خط الأساس"]))}</div>`;
}

function renderVascular() {
  return `<div class="grid cols-3">${renderKpi(["نوع الوصول", "CVC", "قسطرة وريدية مركزية", "warning"])}${renderKpi(["تقييم العدوى", "متوسط", "يحتاج متابعة", "warning"])}${renderKpi(["كفاءة التدفق", "82%", "مقبول", "success"])}</div><div style="margin-top:16px">${card("توثيق الوصول الوعائي", renderFormText(["موقع الوصول", "حالة الجلد", "معدل التدفق", "ملاحظات التمريض"]))}</div>`;
}

function renderDetails(route) {
  const title = route.entity === "alert" ? "تنبيه NEWS2 عالي الخطورة" : route.entity === "event" ? "حدث تدهور سريري" : "جلسة غسيل نشطة";
  return `<div class="split"><div>${card(title, `<div class="patient-summary">${["المريض P-1088", "NEWS2 6", "الوقت 08:42", "الحالة مفتوح"].map((x) => `<div class="summary-cell"><span>${x.split(" ")[0]}</span><strong>${x.substring(x.indexOf(" ") + 1)}</strong></div>`).join("")}</div><div style="margin-top:18px">${renderLineChart()}</div>`)}</div><aside>${card("إجراءات مطلوبة", renderActions())}</aside></div>`;
}

function renderMonitoring() {
  return `<div class="grid cols-4">${[["ضغط الدم", "118/70", "انخفاض عن الخط الأساسي", "warning"], ["النبض", "96", "صاعد", "warning"], ["SpO2", "91%", "حرج", "danger"], ["NEWS2", "6", "تصعيد", "danger"]].map((x) => renderKpi(x, x[3] === "danger")).join("")}</div><div class="grid cols-2" style="margin-top:16px">${card("منحنى العلامات الحيوية", renderLineChart())}${card("ملاحظات الجلسة", renderTimelineItems())}</div>`;
}

function renderAssessment() {
  return `<div class="grid cols-2">${card("مكونات NEWS2", renderTable(["المكون", "القراءة", "النقاط", "التقييم"], [["التنفس", "24", "2", "متوسط"], ["الأكسجين", "91%", "3", "أحمر"], ["الضغط", "118", "0", "مستقر"], ["الوعي", "يقظ", "0", "مستقر"], ["الحرارة", "37.8", "1", "متابعة"]]))}${card("قرار التصعيد", `<div class="kpi-value risk-high">NEWS2 6</div><p class="kpi-meta">تصعيد طبي ومراقبة كل 15 دقيقة.</p>${renderActions()}`)}</div>`;
}

function renderTrend() {
  return `<div class="grid cols-3">${renderKpi(["آخر قراءة", "6", "عالية الخطورة", "danger"], true)}${renderKpi(["أعلى قراءة", "7", "خلال 30 يوم", "warning"])}${renderKpi(["متوسط المريض", "3.1", "فوق خط الأساس", "info"])}</div><div style="margin-top:16px">${card("اتجاه NEWS2", renderLineChart())}</div>`;
}

function renderAlerts() {
  return `<div class="grid cols-3">${renderKpi(["حرجة", "1", "تصعيد فوري", "danger"], true)}${renderKpi(["متوسطة", "4", "متابعة خلال ساعة", "warning"])}${renderKpi(["منخفضة", "8", "مراقبة روتينية", "success"])}</div><div style="margin-top:16px">${card("التنبيهات النشطة", renderTable(["المعرف", "المريض", "الوقت", "الخطورة", "الحالة"], genericRows.events))}</div>`;
}

function renderTimeline(route) {
  return `<div class="split"><div>${card(route.label, renderTimelineItems())}</div><aside>${card("مؤشرات زمنية", `${renderKpi(["زمن الاكتشاف", "0 د", "آلي", "success"])}${renderKpi(["زمن التصعيد", "8 د", "ضمن الهدف", "success"])}${renderKpi(["زمن الإغلاق", "65 د", "قيد المتابعة", "warning"])}`)}</aside></div>`;
}

function renderWorkflow(route) {
  return `<div class="grid cols-4">${["اكتشاف", "تأكيد", "تصعيد", "إغلاق"].map((step, index) => renderKpi([step, index < 3 ? "تم" : "نشط", index < 3 ? "موثق" : "بانتظار المخرج", index < 3 ? "success" : "warning"])).join("")}</div><div style="margin-top:16px">${card(route.label, renderTimelineItems())}</div>`;
}

function renderAnalytics(route) {
  return `<div class="grid cols-4">${kpis.map((item) => renderKpi(item, item[3] === "danger")).join("")}</div><div class="grid cols-2" style="margin-top:16px">${card("تحليل الاتجاهات", renderLineChart())}${card("توزيع المؤشرات", renderBarChart([30, 48, 24, 16, 10]))}</div><div style="margin-top:16px">${card(route.label, renderTable(["المؤشر", "قبل", "بعد", "التحسن"], [["زمن الاستجابة", "18 د", "11 د", "39%"], ["اكتمال التوثيق", "82%", "97%", "15%"], ["التنبيهات المغلقة", "70%", "91%", "21%"]]))}</div>`;
}

function renderResearch() {
  return `<div class="dashboard-hero"><div class="hero-band"><h2>لوحة بحثية لقياس أثر الرصد المبكر</h2><p>مؤشرات الدراسة وجودة البيانات والمقارنات قبل وبعد تطبيق NEWS2 في بيئة الغسيل الكلوي.</p></div><div class="status-panel">${renderKpi(["حجم العينة", "1,284", "جلسات موثقة", "info"])}${renderKpi(["اكتمال البيانات", "97%", "جاهز للتحليل", "success"])}</div></div><div class="grid cols-2">${card("اتجاه الدراسة", renderLineChart())}${card("توزيع البيانات", renderBarChart([55, 42, 30, 18]))}</div>`;
}

function renderComparison() {
  return `<div class="grid cols-3">${renderKpi(["قبل التطبيق", "18 د", "متوسط الاستجابة", "warning"])}${renderKpi(["بعد التطبيق", "11 د", "متوسط الاستجابة", "success"])}${renderKpi(["فرق التحسن", "39%", "دلالة تشغيلية", "success"])}</div><div style="margin-top:16px">${card("مقارنة المؤشرات", renderTable(["المؤشر", "قبل", "بعد", "النتيجة"], [["اكتشاف مبكر", "62%", "88%", "تحسن"], ["تصعيد موثق", "71%", "94%", "تحسن"], ["مخرجات مستقرة", "84%", "91%", "تحسن"]]))}</div>`;
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
  return `<div class="timeline">${timelineItems.map(([time, title, text]) => `<div class="timeline-item"><strong>${time} - ${title}</strong><span>${text}</span></div>`).join("")}</div>`;
}

function renderBarChart(values) {
  return `<div class="chart">${values.map((value) => `<div class="bar" style="height:${value + 42}%"></div>`).join("")}</div>`;
}

function renderLineChart() {
  return `<svg class="line-chart" viewBox="0 0 640 230" role="img" aria-label="NEWS2 trend chart">
    <line x1="28" y1="200" x2="615" y2="200" stroke="#e2e8f0" />
    <line x1="28" y1="40" x2="28" y2="200" stroke="#e2e8f0" />
    <polyline points="40,170 120,150 205,162 285,118 365,132 445,80 540,96 610,58"></polyline>
    ${[[40,170], [120,150], [205,162], [285,118], [365,132], [445,80], [540,96], [610,58]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="6"></circle>`).join("")}
  </svg>`;
}

function card(title, body) {
  return `<article class="card"><div class="card-header"><h2 class="card-title">${title}</h2></div><div class="card-body">${body}</div></article>`;
}

function render() {
  document.body.classList.remove("nav-open");
  const id = currentRoute();
  if (id === "login") {
    renderLogin();
    return;
  }
  renderShell(routes.find((route) => route.id === id) || routes[0]);
}

window.setRoute = setRoute;
window.addEventListener("hashchange", render);
render();
