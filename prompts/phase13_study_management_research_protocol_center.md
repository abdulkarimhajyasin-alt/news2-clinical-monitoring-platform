# PHASE 13 — STUDY MANAGEMENT & RESEARCH PROTOCOL CENTER

## Objective

Implement the Study Management & Research Protocol Center for the NEWS2 Hemodialysis Monitoring Platform.

This phase must establish a formal research-governance layer above the existing clinical and analytics workflows.

The goal is to allow investigators to define, manage, document, monitor, and audit the research study configuration directly inside the platform.

This phase creates the bridge between:

Clinical System
↓
Research Dataset
↓
Research Analytics
↓
Research Study Governance

---

# CURRENT PROJECT STATE

The platform currently supports:

- Patient management
- Dialysis sessions
- Measurements
- NEWS2 engine
- Alerts
- Deterioration events
- Clinical responses
- Response tracking
- Clinical outcomes
- Research dataset builder
- Export center
- Research analytics dashboard

Phase 13 adds:

```text
Research Protocol Management
Study Configuration
Study Governance
Research Readiness Monitoring
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI identity.

Do not break exports.

Do not break analytics.

Do not break clinical workflows.

Do not implement authentication yet.

Do not implement RBAC yet.

Do not implement publication generation.

---

# PHASE BOUNDARY

This phase must do:

```text
Study Registry
↓
Protocol Configuration
↓
Study Timeline
↓
Research Governance
↓
Readiness Tracking
```

This phase must NOT do:

```text
User permissions
Authentication
Publication writing
Statistical inference
Multi-center federation
```

---

# STUDY MODEL

Create or use:

```text
research_studies
```

Required fields:

```text
id
study_code
study_title
study_description
principal_investigator
study_design
study_phase
study_status
study_group_a_name
study_group_b_name
baseline_period_start
baseline_period_end
intervention_period_start
intervention_period_end
study_start_date
study_end_date
target_sample_size
notes
created_at
updated_at
```

---

# STUDY STATUS

Support:

```text
draft
active
paused
completed
archived
```

Arabic:

```text
draft      => مسودة
active     => نشطة
paused     => متوقفة مؤقتاً
completed  => مكتملة
archived   => مؤرشفة
```

---

# STUDY DESIGN TYPES

Support:

```text
observational
prospective
retrospective
before_after
cohort
pilot
```

Arabic labels should be displayed in UI.

---

# SERVICE LAYER

Create:

```text
app/services/study_management_service.py
```

Recommended functions:

```python
create_study()
update_study()
get_study()
list_studies()
build_study_readiness_report()
```

---

# READINESS ENGINE

Create a readiness report.

Evaluate:

```text
study_defined
dataset_available
analytics_available
exports_available
outcomes_available
response_tracking_available
```

Return:

```text
readiness_score
missing_requirements
warnings
recommendations
```

Readiness score:

```text
0–100
```

---

# API ENDPOINTS

Create:

```text
app/routers/studies.py
```

Required endpoints:

```text
POST   /api/studies
GET    /api/studies
GET    /api/studies/{id}
PUT    /api/studies/{id}
GET    /api/studies/{id}/readiness
```

---

# FRONTEND

Implement:

```text
Study Management
Research Protocol
Study Timeline
Study Readiness
```

---

# STUDY DASHBOARD

Display:

```text
Study Title
Principal Investigator
Study Status
Study Design
Target Sample Size
Current Patients
Dataset Rows
Analytics Status
Export Readiness
Readiness Score
```

---

# RESEARCH PROTOCOL PAGE

Display:

```text
Study Objective
Study Design
Baseline Period
Intervention Period
Inclusion Notes
Exclusion Notes
Research Notes
```

---

# TIMELINE PAGE

Display:

```text
Study Start
Baseline Period
Intervention Period
Current Date
Study End
```

---

# READINESS PANEL

Display:

```text
Dataset Ready
Analytics Ready
Exports Ready
Outcomes Ready
Tracking Ready
Overall Readiness
```

Arabic labels only.

---

# AUDIT LOG

Create:

```text
study_created
study_updated
study_readiness_viewed
```

---

# TESTS

Create:

```text
tests/test_study_management.py
```

Required tests:

1. Create study.
2. Update study.
3. List studies.
4. Readiness calculation.
5. Missing requirement detection.
6. API endpoint validation.
7. Empty-safe behavior.
8. Dashboard payload stability.
9. Status transitions.
10. Audit log creation.

---

# DOCUMENTATION

Create:

```text
docs/study_management.md
```

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
docs/research_analytics_dashboard.md
```

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Study architecture
4. Readiness engine
5. API endpoints
6. Frontend updates
7. Audit logs
8. Tests
9. Validation results
10. Risks
11. Git commands

---

# NEXT PHASE

After this phase:

```text
Phase 14 — Role Based Access Control (RBAC)
```

Then:

```text
Phase 15 — Authentication & Security
```
