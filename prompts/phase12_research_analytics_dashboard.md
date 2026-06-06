# PHASE 12 — RESEARCH ANALYTICS DASHBOARD

## Objective

Implement the Research Analytics Dashboard for the NEWS2 Hemodialysis Monitoring Platform.

This phase must transform the collected research dataset into actionable research analytics, visual summaries, trend analysis, and study-ready indicators.

The purpose is not advanced statistical inference yet. The purpose is to provide descriptive analytics, cohort comparisons, and outcome visibility directly inside the platform.

This phase is a major PhD milestone because it begins answering research questions rather than only collecting data.

---

# CURRENT PROJECT STATE

The platform currently supports:

- Patient management
- Dialysis sessions
- Intradialytic measurements
- NEWS2 engine
- Alert engine
- Clinical deterioration workflow
- Clinical response workflow
- Response time tracking
- Clinical outcomes workflow
- Research dataset builder
- CSV export
- Excel export
- SPSS-ready export
- Dataset quality validation

Current research chain:

```text
Clinical Data
↓
Research Dataset
↓
Export Center
```

Phase 12 extends this to:

```text
Clinical Data
↓
Research Dataset
↓
Research Analytics
↓
Research Dashboard
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI identity.

Do not break exports.

Do not break dataset builder.

Do not modify tables destructively.

Do not implement inferential statistics yet.

Do not implement machine learning.

Do not implement predictive analytics.

Do not implement publication-ready statistical tests.

---

# PHASE BOUNDARY

This phase must do:

```text
Descriptive analytics
Trend analysis
Distribution analysis
Cohort comparison
Outcome analysis
Response-time analysis
Research KPIs
```

This phase must NOT do:

```text
T-test
ANOVA
Regression
Machine learning
Prediction
Research publication automation
```

Those belong to later phases.

---

# ANALYTICS MODULE

Create:

```text
app/services/research_analytics_service.py
```

Recommended functions:

```python
build_research_kpis()
build_news2_distribution()
build_risk_level_distribution()
build_outcome_distribution()
build_response_time_analysis()
build_deterioration_analysis()
build_group_comparison()
```

All functions must use the research dataset layer rather than duplicating query logic.

---

# KPI DASHBOARD

Create analytics for:

```text
total_patients
total_sessions
total_measurements
total_news2_assessments
total_alerts
total_deterioration_events
total_responses
total_outcomes
```

Additional KPIs:

```text
average_news2_score
average_response_time_minutes
alerts_per_100_sessions
deterioration_rate
response_completion_rate
outcome_completion_rate
dataset_quality_score
```

---

# NEWS2 DISTRIBUTION

Calculate:

```text
0–2
3–4
5–6
7+
```

Return:

```text
count
percentage
```

Arabic labels:

```text
منخفض جداً
منخفض
متوسط
مرتفع
```

---

# RISK LEVEL ANALYSIS

Analyze:

```text
low
medium
high
```

For each level return:

```text
count
percentage
outcome_distribution
average_response_time
```

---

# OUTCOME ANALYSIS

For:

```text
stable_completed_session
session_stopped_early
hospital_admission
emergency_department_transfer
icu_admission
death
```

Return:

```text
count
percentage
```

Calculate:

```text
good_outcome_rate
adverse_outcome_rate
```

Where:

Good:

```text
stable_completed_session
```

Adverse:

```text
hospital_admission
emergency_department_transfer
icu_admission
death
```

---

# RESPONSE TIME ANALYSIS

Calculate:

```text
average_time_to_alert
average_time_to_view
average_time_to_response
average_time_to_action
average_total_response_time
```

Also:

```text
fastest_response
slowest_response
median_response
```

If median calculation is easy, include it.

---

# DETERIORATION ANALYSIS

Analyze:

```text
acute_hypotension
suspected_sepsis_or_fever
arrhythmia
seizures
reduced_consciousness
other
```

Return:

```text
count
percentage
associated_outcomes
```

---

# STUDY GROUP COMPARISON

Prepare support for:

```text
study_group
study_phase
```

If fields exist.

Return:

```text
group_a
group_b
```

Comparison:

```text
average_news2
average_response_time
outcome_distribution
```

If no group data exists:

Return empty-safe structure.

Do not fail.

---

# PRE / POST ANALYSIS PLACEHOLDER

Add architecture support for:

```text
baseline_period
intervention_period
```

For now:

Return descriptive counts only.

Document that inferential analysis is not implemented yet.

---

# API ENDPOINTS

Create:

```text
app/routers/research_analytics.py
```

Required endpoints:

## Analytics Summary

```text
GET /api/research/analytics/summary
```

---

## NEWS2 Distribution

```text
GET /api/research/analytics/news2-distribution
```

---

## Outcome Analysis

```text
GET /api/research/analytics/outcomes
```

---

## Response Analysis

```text
GET /api/research/analytics/response-times
```

---

## Deterioration Analysis

```text
GET /api/research/analytics/deterioration
```

---

## Group Comparison

```text
GET /api/research/analytics/group-comparison
```

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement:

```text
Research Analytics Dashboard
Research KPI Dashboard
Outcome Analytics
Response Analytics
Risk Analytics
```

Use real API data.

---

# DASHBOARD UI

Add KPI cards:

```text
عدد المرضى
عدد الجلسات
عدد القياسات
عدد تقييمات NEWS2
عدد التنبيهات
عدد أحداث التدهور
عدد الاستجابات
عدد المآلات
```

Additional cards:

```text
متوسط NEWS2
متوسط زمن الاستجابة
معدل التدهور
معدل اكتمال الاستجابة
جودة البيانات
```

---

# CHARTS

Use existing chart framework.

Required charts:

## NEWS2 Distribution

```text
NEWS2 Score Distribution
```

---

## Outcome Distribution

```text
Outcome Distribution
```

---

## Response Times

```text
Response Time Metrics
```

---

## Deterioration Types

```text
Deterioration Type Distribution
```

---

# RESEARCH READINESS PANEL

Add:

```text
Dataset Quality
Outcome Completion
Response Completion
Export Readiness
```

Arabic labels:

```text
جاهزية البحث
جاهزية التصدير
اكتمال المآلات
اكتمال الاستجابات
```

---

# ARABIC LABELS

Screen title:

```text
لوحة التحليلات البحثية
```

Sections:

```text
مؤشرات الدراسة
تحليل NEWS2
تحليل المآلات
تحليل الاستجابة
تحليل التدهور السريري
مقارنة المجموعات
```

Messages:

```text
لا توجد بيانات كافية للتحليل
تم تحميل التحليلات
```

---

# AUDIT LOG

Add:

```text
research_analytics_viewed
```

Only if audit infrastructure already supports it.

Otherwise keep lightweight.

---

# TESTS

Create:

```text
tests/test_research_analytics_dashboard.py
```

Required tests:

1. KPI summary returns expected keys.
2. NEWS2 distribution works.
3. Outcome analysis works.
4. Response analysis works.
5. Deterioration analysis works.
6. Empty dataset handled safely.
7. Group comparison safe without groups.
8. API endpoints return valid payloads.
9. Percentages sum correctly.
10. Frontend-facing structures remain stable.

---

# DOCUMENTATION

Create:

```text
docs/research_analytics_dashboard.md
```

Must document:

- KPI definitions
- Distribution calculations
- Outcome calculations
- Response calculations
- Group comparison logic
- Limitations
- Research usage notes

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/research_export_center.md
```

Mention Phase 12 support.

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Manual validation:

```bash
uvicorn app.main:app --reload
```

Verify:

1. Analytics dashboard loads.
2. KPI cards show values.
3. Charts render.
4. Empty-state handling works.
5. Research readiness indicators work.
6. Analytics APIs return data.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Analytics architecture
4. KPI metrics implemented
5. API endpoints created
6. Frontend updates
7. Research readiness features
8. Tests added
9. Validation results
10. Research safety notes
11. Risks / next phase recommendation
12. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase:

```text
Phase 13 — Role Based Access Control (RBAC)
```

and later:

```text
Phase 14 — Authentication & Security
```

because the research layer will then be largely complete.
