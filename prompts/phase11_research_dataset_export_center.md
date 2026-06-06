# PHASE 11 — RESEARCH DATASET & EXPORT CENTER

## Objective

Implement the Research Dataset & Export Center for the NEWS2 Hemodialysis Monitoring Platform.

This phase must build a research-grade dataset builder that combines the complete clinical workflow into exportable records for statistical analysis.

The dataset must support Excel and CSV export, SPSS-ready preparation, research data quality checks, privacy rules, and frontend export center UI.

This is a core PhD research phase because it converts operational clinical records into a structured dataset suitable for analysis.

---

# CURRENT PROJECT STATE

The project currently supports:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready configuration
- Patient records
- Dialysis sessions
- Intradialytic measurements
- NEWS2 calculation engine
- Persisted NEWS2 assessments
- Alert creation engine
- Clinical deterioration event workflow
- Medical/nursing response workflow
- Response time tracking engine
- Clinical outcomes 24–72h workflow
- Research summary dashboard
- Audit logs

Current traceability chain:

```text
Patient
↓
Dialysis Session
↓
Measurement
↓
NEWS2 Assessment
↓
Alert
↓
Clinical Deterioration Event
↓
Clinical Response
↓
Response Tracking
↓
Clinical Outcome
```

Phase 11 must build a dataset/export layer over this chain.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.
Do not break existing workflows.
Do not change tables destructively.
Do not implement full authentication yet.
Do not implement role permissions yet.
Do not implement advanced statistical analysis yet.
Do not implement AI/ML.
Do not add unnecessary heavy dependencies.

---

# PHASE BOUNDARY

This phase must do:

```text
Build research dataset rows
↓
Validate dataset quality
↓
Export CSV
↓
Export Excel
↓
Prepare SPSS-ready codebook
↓
Expose API endpoints
↓
Add frontend Export Center
```

This phase must NOT do:

```text
Advanced statistical modeling
Pre/Post inferential analysis
Authentication
Role-based access control
Deployment
```

Those belong to later phases.

---

# DATASET DESIGN

Each dataset row should represent a clinically meaningful research observation.

Recommended primary row unit:

```text
one intradialytic measurement + linked NEWS2 assessment
```

Enrich each row with linked data when available:

```text
patient baseline
dialysis session
vascular access
NEWS2 assessment
alert
deterioration event
clinical response
response tracking
clinical outcome
study phase/group
```

---

# REQUIRED DATASET FIELDS

Build a unified dataset with these fields.

## Patient Fields

```text
patient_code
age
gender
target_dry_weight
dialysis_start_date
dialysis_vintage_months
weekly_sessions_count
comorbidities
charlson_comorbidity_index
baseline_functional_status
study_phase
study_group
```

## Vascular Access Fields

```text
vascular_access_type
vascular_access_location
vascular_access_inserted_at
```

## Dialysis Session Fields

```text
dialysis_session_id
session_date
weekday
actual_start_time
actual_end_time
target_ultrafiltration
blood_flow_rate
dialysate_flow_rate
dialysate_temperature
ultrafiltration_rate
ultrafiltration_volume
session_duration_minutes
session_status
```

## Measurement Fields

```text
measurement_id
measurement_time
measurement_interval_minutes
respiratory_rate
spo2
oxygen_therapy
systolic_bp
diastolic_bp
pulse_rate
temperature
consciousness_level
confusion_status
```

## NEWS2 Fields

```text
news2_assessment_id
respiratory_score
spo2_score
oxygen_score
systolic_bp_score
pulse_score
temperature_score
consciousness_score
news2_total_score
risk_level
alert_required
trigger_reason
```

## Alert Fields

```text
alert_id
alert_created
alert_status
alert_priority
alert_severity_level
alert_trigger_reason
alert_created_at
alert_viewed_at
alert_acknowledged_at
alert_action_taken_at
alert_closed_at
```

## Clinical Deterioration Fields

```text
clinical_deterioration_event_id
deterioration_time
time_from_session_start_minutes
deterioration_type
triggering_news2_score
deterioration_description
```

## Clinical Response Fields

```text
clinical_response_id
digital_alert_time
actual_response_start_time
response_delay_minutes
patient_actions
vascular_access_actions
response_notes
```

## Response Tracking Fields

```text
response_tracking_id
time_to_alert_minutes
time_to_view_minutes
time_to_response_minutes
time_to_action_minutes
total_response_time_minutes
```

## Outcome Fields

```text
clinical_outcome_id
outcome_type
outcome_recorded_at
outcome_window_hours
outcome_description
```

---

# PRIVACY RULES

Research exports must protect privacy.

Default export must:

- Include `patient_code`
- Exclude patient full name
- Exclude direct identifiers where possible

Do not export:

```text
patient full_name
user phone
user email
password_hash
ip_address
user_agent
```

Add clear documentation that exports are research datasets, not full clinical records.

---

# EXPORT FORMATS

Implement:

```text
CSV
Excel XLSX
SPSS-ready CSV + codebook
```

Do not create true `.sav` unless the project already has a safe dependency for it.

Instead, create:

```text
research_dataset.csv
research_dataset.xlsx
spss_codebook.md
spss_variable_labels.csv
```

The SPSS-ready package should include:

- CSV file
- Variable label mapping
- Value label mapping
- Missing-value notes
- Data dictionary

---

# DEPENDENCIES

Allowed lightweight dependencies:

```text
openpyxl
```

For CSV use Python standard library or pandas only if already present.

Prefer avoiding pandas unless already installed.

If adding openpyxl, update:

```text
requirements.txt
```

---

# SERVICE LAYER

Create:

```text
app/services/export_service.py
```

Recommended functions:

```python
build_research_dataset(db, filters)
validate_research_dataset(rows)
export_dataset_csv(rows)
export_dataset_xlsx(rows)
build_spss_codebook()
build_spss_variable_labels()
```

Responsibilities:

- Query related clinical records.
- Build flat research rows.
- Apply privacy rules.
- Apply filters.
- Validate quality.
- Generate export files or streaming responses.
- Avoid leaking private identifiers.

---

# DATA QUALITY VALIDATION

Implement dataset quality checks.

Checks:

```text
missing_patient_code
missing_session
missing_measurement_time
missing_news2_total_score
invalid_timestamp_sequence
missing_outcome_for_deterioration
alert_without_response
response_without_tracking
duplicate_dataset_rows
```

Return:

```text
quality_score
total_rows
issues_count
issues_by_type
warnings
```

Quality score suggestion:

```text
100 - weighted issue penalties
```

Keep simple and explainable.

---

# FILTERS

Dataset builder and export endpoints should support filters:

```text
start_date
end_date
patient_id
patient_code
study_phase
study_group
risk_level
outcome_type
deterioration_type
```

All filters optional.

---

# API ENDPOINTS

Create or update:

```text
app/routers/research_exports.py
```

Required endpoints:

## Dataset Preview

```text
GET /api/research/dataset
```

Returns JSON preview rows.

Support:

```text
limit
filters
```

---

## Dataset Quality

```text
GET /api/research/dataset/quality
```

Returns quality report.

---

## Export CSV

```text
GET /api/research/export/csv
```

Returns downloadable CSV.

---

## Export Excel

```text
GET /api/research/export/xlsx
```

Returns downloadable XLSX.

---

## SPSS Codebook

```text
GET /api/research/export/spss-codebook
```

Returns markdown/text codebook.

---

## SPSS Variable Labels

```text
GET /api/research/export/spss-variable-labels
```

Returns CSV mapping.

---

# FRONTEND INTEGRATION

Update:

```text
app/static/app.js
```

Implement or improve:

```text
Export Center
Dataset Statistics
Research Dashboard
```

Use real export/quality APIs.

---

# EXPORT CENTER UI

Required Arabic UI sections:

## Dataset Preview

Show table with selected fields:

```text
patient_code
session_date
measurement_time
news2_total_score
risk_level
alert_created
deterioration_type
response_delay_minutes
outcome_type
study_phase
study_group
```

## Filters

Arabic labels:

```text
من تاريخ
إلى تاريخ
مرحلة الدراسة
مجموعة الدراسة
مستوى الخطورة
نوع المآل
نوع التدهور
```

## Export Buttons

```text
تصدير CSV
تصدير Excel
تحميل Codebook لـ SPSS
تحميل Variable Labels لـ SPSS
```

## Quality Panel

Show:

```text
درجة جودة البيانات
عدد السجلات
عدد المشاكل
المشاكل حسب النوع
تنبيهات الجودة
```

---

# DATASET STATISTICS UI

Show KPI cards:

```text
عدد سجلات البحث
عدد القياسات
عدد تنبيهات NEWS2
عدد أحداث التدهور
عدد الاستجابات
عدد المآلات
نسبة اكتمال البيانات
```

---

# RESEARCH DASHBOARD UPDATE

Add dataset readiness indicators:

```text
Research Dataset Rows
Dataset Quality Score
Missing Outcomes
Alerts Without Response
Export Readiness
```

---

# ARABIC LABELS

Use professional Arabic labels.

Screen title:

```text
مركز التصدير البحثي
```

Quality labels:

```text
جاهزية البيانات البحثية
درجة جودة البيانات
مشاكل البيانات
تنبيهات قبل التصدير
```

Messages:

```text
تم تجهيز ملف التصدير
تعذر تحميل البيانات البحثية
لا توجد سجلات مطابقة للفلاتر المحددة
```

---

# FILE DOWNLOAD BEHAVIOR

Frontend export buttons should open the API endpoint or trigger download.

Do not fake downloads.

Use real backend responses.

---

# TESTS

Create:

```text
tests/test_research_export_center.py
```

Required tests:

1. Dataset builder returns rows.
2. Dataset rows exclude patient full name.
3. Dataset includes required core fields.
4. Filters work.
5. Quality report returns expected structure.
6. CSV export returns correct content type.
7. XLSX export returns downloadable content.
8. SPSS codebook endpoint works.
9. SPSS variable labels endpoint works.
10. Export does not include password_hash/email/phone.
11. Dataset row count is stable with seeded data.

---

# DOCUMENTATION

Create:

```text
docs/research_export_center.md
```

Must document:

- Dataset row definition.
- Included variables.
- Privacy rules.
- Export formats.
- SPSS preparation approach.
- Data quality checks.
- API endpoints.
- Frontend behavior.
- Research safety note.

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/outcome_workflow.md
```

Mention Phase 11 support.

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

Then verify:

1. Export Center loads.
2. Dataset preview shows rows.
3. Quality score appears.
4. CSV downloads.
5. XLSX downloads.
6. SPSS codebook downloads.
7. No full patient names appear in export.
8. Filters work.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Dataset architecture
4. Export formats implemented
5. Privacy rules implemented
6. API endpoints created
7. Frontend updates
8. Data quality validation
9. Tests added or updated
10. Validation results
11. Research safety notes
12. Risks / next phase recommendation
13. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase, the recommended next phase is:

```text
Phase 12 — Research Analytics Dashboard
```

That phase will add deeper research analytics:

```text
Pre/Post Comparison
Risk-Level Outcome Analysis
Response-Time vs Outcome
NEWS2 Distribution
Deterioration Type Trends
Study Group Comparison
```
