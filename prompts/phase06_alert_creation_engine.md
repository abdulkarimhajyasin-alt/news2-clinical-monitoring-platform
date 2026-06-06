# PHASE 06 — ALERT CREATION ENGINE

## Objective

Implement the governed clinical alert creation engine for the NEWS2 Hemodialysis Monitoring Platform.

This phase must automatically generate alerts from persisted NEWS2 assessments while preventing duplicate alerts, preserving clinical traceability, and preparing the system for clinical deterioration workflows.

The system must create alerts only after measurements and NEWS2 assessments have been successfully persisted.

---

# CURRENT PROJECT STATE

The project currently supports:

- Patient management
- Dialysis sessions
- Intradialytic measurements
- NEWS2 calculation engine
- Persisted NEWS2 assessments
- Monitoring write workflow
- Research dashboard
- Read APIs
- Monitoring APIs

Current workflow:

```text
Vital Signs
↓
Measurement Saved
↓
NEWS2 Calculated
↓
NEWS2 Assessment Saved
```

Phase 06 extends this workflow.

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.

Do not break monitoring workflow.

Do not remove NEWS2 calculation logic.

Do not modify existing database tables destructively.

Do not implement clinical deterioration workflow yet.

Do not implement response tracking yet.

Do not implement outcome tracking yet.

---

# ALERT CREATION RULES

Alerts must be created automatically when:

```text
NEWS2 >= 5
```

OR

```text
single_parameter_trigger = true
```

---

# ALERT SEVERITY MAPPING

Map NEWS2 results to alert severity.

## Medium Risk

```text
NEWS2 5–6
```

Alert:

```text
risk_level = medium
severity_level = medium
priority = normal
```

---

## High Risk

```text
NEWS2 >= 7
```

Alert:

```text
risk_level = high
severity_level = high
priority = urgent
```

---

## Single Parameter Trigger

If:

```text
single_parameter_trigger = true
```

and total score < 5

Create alert:

```text
risk_level = medium
severity_level = medium
priority = normal
trigger_reason = single_parameter_trigger
```

---

# DUPLICATE ALERT PREVENTION

Very important.

Do not create unlimited alerts.

For the same patient/session:

If an active alert already exists:

```text
new
viewed
acknowledged
in_progress
```

Do not create a duplicate alert for the same assessment state.

Instead:

- Reuse existing alert if appropriate.
- Update timestamps if needed.
- Record event in logs.

The goal is:

```text
One active alert per active clinical deterioration chain
```

not dozens of duplicate alerts.

---

# ALERT STATUS MODEL

Supported statuses:

```text
new
viewed
acknowledged
in_progress
closed
cancelled
```

Default:

```text
new
```

---

# ALERT SERVICE

Create or update:

```text
app/services/alert_service.py
```

Core function:

```python
create_alert_from_news2_assessment(...)
```

Responsibilities:

- Evaluate assessment
- Check thresholds
- Prevent duplicates
- Create alert
- Return structured result

---

# ALERT CREATION WORKFLOW

Workflow:

```text
Measurement Saved
↓
NEWS2 Saved
↓
Evaluate Alert Rules
↓
Alert Needed?
 ├─ No → Finish
 └─ Yes
      ↓
Check Existing Active Alert
      ↓
Create or Reuse Alert
      ↓
Return Alert Result
```

---

# MONITORING INTEGRATION

Update monitoring workflow.

After:

```text
NEWS2 assessment created
```

Call:

```python
create_alert_from_news2_assessment()
```

The monitoring workflow response should now include:

```text
measurement
news2_assessment
alert
message
```

Alert can be:

```text
null
```

if no alert was required.

---

# ALERT RESPONSE SCHEMA

Create schema:

```text
AlertCreationResult
```

Response example:

```json
{
  "alert_created": true,
  "alert_id": 15,
  "status": "new",
  "risk_level": "high",
  "severity_level": "high",
  "priority": "urgent",
  "trigger_reason": "NEWS2 >= 7"
}
```

---

# ALERT READ APIS

Extend existing alerts endpoint.

Required:

```text
GET /api/alerts
GET /api/alerts/{id}
```

Support filters:

```text
status
risk_level
severity_level
patient_id
dialysis_session_id
```

Support ordering:

Newest first.

---

# ALERT ACTION APIS

Create minimal lifecycle endpoints.

## View Alert

```text
POST /api/alerts/{id}/view
```

Sets:

```text
status = viewed
viewed_at
```

---

## Acknowledge Alert

```text
POST /api/alerts/{id}/acknowledge
```

Sets:

```text
status = acknowledged
acknowledged_at
```

---

## Start Action

```text
POST /api/alerts/{id}/start
```

Sets:

```text
status = in_progress
action_taken_at
```

---

## Close Alert

```text
POST /api/alerts/{id}/close
```

Sets:

```text
status = closed
closed_at
```

Do not implement deterioration workflow yet.

---

# FRONTEND UPDATES

Update:

```text
app/static/app.js
```

Active Alerts screen must use real alert data.

Display:

```text
Alert ID
Patient
Risk Level
Severity
Priority
Status
Created Time
Trigger Reason
```

Use Arabic labels.

---

# ALERT COLORS

Low:

Green

Medium:

Orange

High:

Red

Critical:

Dark Red

Maintain existing medical visual identity.

---

# ALERT BADGES

Arabic labels:

```text
new            => جديد
viewed         => تمت المشاهدة
acknowledged   => تم التأكيد
in_progress    => قيد المعالجة
closed         => مغلق
cancelled      => ملغى
```

---

# DASHBOARD INTEGRATION

Dashboard should display:

```text
Active Alerts
High Risk Alerts
Medium Risk Alerts
Closed Alerts
```

Use real data.

---

# AUDIT LOG

When alerts are:

- created
- viewed
- acknowledged
- started
- closed

Create audit log entries if audit infrastructure already exists.

If not, add lightweight support.

---

# TESTS

Create:

```text
tests/test_alert_creation_engine.py
```

Required tests:

1. NEWS2 < 5 creates no alert.
2. NEWS2 5–6 creates medium alert.
3. NEWS2 >= 7 creates high alert.
4. Single parameter trigger creates alert.
5. Duplicate prevention works.
6. View endpoint updates status.
7. Acknowledge endpoint updates status.
8. Start endpoint updates status.
9. Close endpoint updates status.
10. Monitoring workflow now returns alert when required.

---

# DOCUMENTATION

Create:

```text
docs/alert_engine.md
```

Must document:

- Alert thresholds
- Severity mapping
- Duplicate prevention
- Alert lifecycle
- API endpoints
- Clinical safety notes

Update:

```text
README.md
docs/system_architecture.md
docs/research_workflow.md
```

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

Create:

- NEWS2 score < 5
- NEWS2 score 5–6
- NEWS2 score >= 7

Verify alerts are created correctly.

Verify duplicate prevention.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Alert engine architecture
4. Alert creation rules
5. Alert lifecycle APIs
6. Monitoring integration
7. Frontend updates
8. Tests added
9. Validation results
10. Clinical safety notes
11. Risks / next phase recommendation
12. Git commands

---

# NEXT PHASE PREVIEW

After this phase:

```text
Phase 07 — Clinical Deterioration Event Workflow
```

This phase will transform alerts into structured clinical deterioration events and begin the response workflow chain.
