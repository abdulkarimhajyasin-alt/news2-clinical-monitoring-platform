# Phase 18C — HD2-mNEWS Risk Color & Nursing Protocol Engine

## Objective
Implement the study-specific HD2-mNEWS risk color and nursing protocol layer exactly according to the doctor’s final digital monitoring form, without expanding the platform beyond the PhD research scope.

The system already has:
- Standard NEWS2 workflow
- HD2-mNEWS scoring engine
- Patient baseline/context alignment
- Dialysis session context alignment
- Alerts, responses, outcomes, research dataset, analytics, RBAC, authentication, patient lifecycle

This phase must convert HD2-mNEWS results into clear operational research outputs:
- Green / Yellow / Red risk color
- Arabic risk labels
- Required nursing protocol
- Required reassessment interval
- Required response urgency
- Protocol guidance shown in the monitoring UI
- Persisted protocol metadata for research/export/analytics

Do not build a broad hospital workflow engine. Keep the implementation focused only on the doctor’s final form.

---

## Source-of-Truth Rules
Use the doctor’s final digital monitoring form as the highest priority.

HD2-mNEWS risk levels:

1. Green — Low Risk
   - Score: 0–4
   - Arabic label: أخضر - آمن
   - Required actions:
     1. Routine follow-up
     2. Measure vital signs every 60 minutes
     3. Record data in the platform
     4. Continue the session as scheduled
   - Reassessment time: 60 minutes

2. Yellow — Moderate Risk
   - Score: 5–6
   - Arabic label: أصفر - مراقبة
   - Required actions:
     1. Repeat vital signs within 15–30 minutes
     2. Review dialysis machine settings, especially fluid removal rate and temperature
     3. Assess associated symptoms
     4. Document nursing notes in the platform
   - Reassessment time: 15–30 minutes

3. Red — High Risk / Emergency
   - Score: >= 7 OR any critical variable score = 3
   - Arabic label: أحمر - طوارئ
   - Required actions:
     1. Call the responsible physician immediately
     2. Assess airway and consciousness
     3. Repeat vital signs within 5 minutes
     4. Prepare emergency equipment: oxygen, fluids, emergency medications
     5. Consider temporary dialysis interruption
     6. Record the event in the platform and medical file
     7. Continue close monitoring every 5–10 minutes
   - Required response time: within 5 minutes
   - Follow-up interval: every 5–10 minutes

Critical automatic red triggers already expected from Phase 18A:
- SpO2 <= 91%
- AVPU = Unresponsive
- Symptomatic SBP <= 90
- Critical potassium range
- Critical vascular access/fistula state

---

## Implementation Requirements

### 1. Backend Protocol Service
Create or extend a service dedicated to HD2-mNEWS protocol guidance.

Suggested file:
- `app/services/hd2_protocol_service.py`

The service should expose a pure function, for example:

```python
build_hd2_nursing_protocol(score: int, risk_color: str, critical_triggers: list | None = None) -> dict
```

Return a structured object with:
- `risk_color`
- `risk_label_ar`
- `risk_label_en`
- `risk_level`
- `required_actions_ar`
- `required_actions_en`
- `reassessment_interval_minutes_min`
- `reassessment_interval_minutes_max`
- `required_response_time_minutes`
- `follow_up_interval_minutes_min`
- `follow_up_interval_minutes_max`
- `requires_physician_call`
- `requires_emergency_preparation`
- `requires_machine_settings_review`
- `requires_symptom_assessment`
- `requires_close_monitoring`
- `protocol_summary_ar`
- `protocol_summary_en`

Keep this function deterministic and fully covered by tests.

---

### 2. Integrate With HD2-mNEWS Calculation
Extend the existing HD2-mNEWS calculation output to include nursing protocol metadata.

Do not break the existing `POST /api/hd2-mnews/calculate` response schema.
Add fields additively.

Expected response additions:
- `nursing_protocol`
- `reassessment_interval_label_ar`
- `required_response_time_label_ar`
- `protocol_actions_ar`

---

### 3. Persist Protocol Metadata With Monitoring Records
When monitoring creation calculates and persists HD2-mNEWS, also persist the protocol metadata needed for research traceability.

Use additive nullable columns or JSON if the project already uses JSON fields safely.

Recommended persisted fields:
- `hd2_risk_color`
- `hd2_risk_label_ar`
- `hd2_protocol_json`
- `hd2_reassessment_interval_min`
- `hd2_reassessment_interval_max`
- `hd2_required_response_time_minutes`
- `hd2_requires_physician_call`
- `hd2_requires_emergency_preparation`
- `hd2_requires_close_monitoring`

If similar HD2 fields already exist, reuse them rather than duplicating.

Add safe startup/runtime schema guards for SQLite/PostgreSQL compatibility.

---

### 4. Frontend UI — Monitoring Result Panel
Update the Arabic RTL monitoring result panel to show a clear protocol card after HD2-mNEWS calculation.

The card must show:
- HD2-mNEWS total score
- Risk color: أخضر / أصفر / أحمر
- Arabic risk label
- Required reassessment time
- Required response time if red
- Required nursing actions as a numbered Arabic list
- Critical trigger reasons if present

Design requirements:
- Preserve the existing Arabic medical UI identity.
- Make green/yellow/red visually clear but professional.
- Do not clutter the page.
- The nurse should immediately understand what to do next.

---

### 5. Frontend UI — Existing Monitoring Records
Where monitoring/measurement records are listed or displayed, add HD2 protocol summary if available:
- Color badge
- Score
- Reassessment interval
- Red emergency marker when applicable

Keep this compact.

---

### 6. Alert Integration
If HD2-mNEWS risk is red:
- Existing high-priority alert creation/upgrade must remain active.
- Ensure the alert details include the HD2 protocol summary if alert details support metadata.
- Do not create duplicate alerts for the same measurement/session if the existing duplicate prevention already handles this.

If HD2-mNEWS risk is yellow:
- Do not create a high emergency alert unless current architecture already creates medium alerts for this severity.
- If medium alert logic exists and fits the architecture, attach protocol metadata.
- If not, only show protocol guidance in the monitoring result and persist it.

---

### 7. Research Dataset / Export Alignment
Add protocol fields to the research dataset and exports:
- HD2 risk color
- HD2 Arabic risk label
- Reassessment interval
- Required response time
- Physician call required
- Emergency preparation required
- Close monitoring required
- Protocol action summary

Deleted patients must remain excluded.

---

### 8. Tests
Add/extend tests for:

1. Pure protocol service:
   - Green score returns 60-minute routine protocol
   - Yellow score returns 15–30 minute reassessment protocol
   - Red score returns emergency protocol and physician call requirement
   - Red triggered by critical variable keeps red protocol even if total score is otherwise lower

2. API response:
   - `POST /api/hd2-mnews/calculate` includes protocol metadata
   - Green/yellow/red responses are stable

3. Monitoring persistence:
   - HD2 protocol metadata is persisted when HD2 fields are present
   - Existing standard NEWS2 workflow remains compatible

4. Research export:
   - Protocol fields appear in dataset/export
   - Deleted patients remain excluded

5. Frontend regression:
   - `node --check app/static/app.js`
   - If existing tests inspect navigation/rendering, update them carefully.

---

## Constraints
- Do not remove or break standard NEWS2.
- Do not change existing authentication/RBAC semantics.
- Do not add broad hospital workflow features.
- Do not add shift management, staff assignment, or multi-center logic.
- Do not physically delete any data.
- Keep schema changes additive and nullable.
- Preserve Arabic-first RTL UI.
- Preserve current visual identity.
- Preserve all existing tests unless they must be updated for the new protocol fields.

---

## Validation Commands
Run all of the following:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

If `pytest` is not on PATH, use:

```bash
python -m pytest
```

---

## Expected Final Response From Codex
After implementation, report:
- Objective completed
- Files changed
- Backend changes
- Frontend changes
- Protocol rules implemented
- Tests added/updated
- Validation results
- Risk analysis
- Final Git commands

---

## Git Commands
When everything passes:

```bash
git add .
git commit -m "Add HD2 nursing protocol guidance"
git push origin main
```
