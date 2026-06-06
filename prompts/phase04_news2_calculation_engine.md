# PHASE 04 — NEWS2 CALCULATION ENGINE

## Objective

Implement the official NEWS2 calculation engine for the NEWS2 Hemodialysis Monitoring Platform.

This phase must build the clinical scoring core of the project while preserving the existing FastAPI + SQLAlchemy + Arabic RTL frontend architecture.

The NEWS2 engine must calculate component scores from vital signs, compute the total NEWS2 score, classify clinical risk, and prepare the system for later alert creation workflows.

This phase must be implemented as a clinical decision-support calculation layer, not as a replacement for clinical judgment.

---

# CURRENT PROJECT STATE

The project currently has:

- Arabic-first RTL frontend
- FastAPI backend
- SQLAlchemy models
- SQLite local database
- PostgreSQL-ready configuration
- Seed data
- Read-only API integration
- Dashboard / Patients / Sessions / Alerts / Research Summary using real API data

Existing important files:

```text
app/main.py
app/database.py
app/models.py
app/schemas.py
app/seed.py

app/services/news2_service.py
app/routers/news2.py

app/static/index.html
app/static/styles.css
app/static/app.js

tests/
docs/
```

---

# CRITICAL RULES

## Preserve Existing Work

Do not redesign the UI.
Do not break the existing API integration.
Do not remove existing seed data.
Do not change database tables destructively.
Do not implement authentication in this phase.
Do not implement full alert auto-creation yet.
Do not implement write workflows for all clinical forms yet.

---

# MEDICAL SAFETY PRINCIPLES

NEWS2 must be implemented as decision support only.

Add clear documentation that:

- NEWS2 supports early detection of clinical deterioration.
- It does not replace clinical judgment.
- Final clinical decisions remain the responsibility of qualified healthcare professionals.
- The implementation must be clinically reviewed before real-world deployment.

---

# OFFICIAL NEWS2 PARAMETERS

NEWS2 uses six physiological parameters plus oxygen therapy weighting:

```text
respiratory_rate
spo2
oxygen_therapy
systolic_bp
pulse_rate
temperature
consciousness_level / new confusion
```

The engine must support:

- SpO2 Scale 1
- SpO2 Scale 2 placeholder/support path
- Supplemental oxygen score
- AVPU / new confusion logic

---

# NEWS2 SCORING RULES — SCALE 1

Implement the standard NEWS2 Scale 1 scoring.

## Respiratory Rate

```text
<= 8        => 3
9 - 11      => 1
12 - 20     => 0
21 - 24     => 2
>= 25       => 3
```

## Oxygen Saturation — Scale 1

```text
<= 91       => 3
92 - 93     => 2
94 - 95     => 1
>= 96       => 0
```

## Supplemental Oxygen

```text
oxygen_therapy = true  => 2
oxygen_therapy = false => 0
```

## Systolic Blood Pressure

```text
<= 90       => 3
91 - 100    => 2
101 - 110   => 1
111 - 219   => 0
>= 220      => 3
```

## Pulse Rate

```text
<= 40       => 3
41 - 50     => 1
51 - 90     => 0
91 - 110    => 1
111 - 130   => 2
>= 131      => 3
```

## Temperature

```text
<= 35.0     => 3
35.1 - 36.0 => 1
36.1 - 38.0 => 0
38.1 - 39.0 => 1
>= 39.1     => 2
```

## Consciousness / New Confusion

Support these values:

```text
alert
voice
pain
unresponsive
new_confusion
```

Scoring:

```text
alert         => 0
voice         => 3
pain          => 3
unresponsive  => 3
new_confusion => 3
```

---

# SPO2 SCALE 2 SUPPORT

Implement a clearly separated structure for SpO2 Scale 2.

Scale 2 is used only when clinically selected for patients with hypercapnic respiratory failure risk.

For this phase:

- Add data structures and function path for `spo2_scale = "scale_2"`.
- Implement a conservative placeholder if exact Scale 2 rules are not already documented in the project.
- Mark Scale 2 as requiring clinical review before production use.
- Default must be Scale 1.

Do not silently apply Scale 2 unless explicitly requested in input.

Recommended input field:

```text
spo2_scale
```

Allowed values:

```text
scale_1
scale_2
```

Default:

```text
scale_1
```

---

# RISK CLASSIFICATION

Implement risk classification from total NEWS2 score.

```text
0 - 4  => low
5 - 6  => medium
>= 7   => high
```

Also support clinical alert flag:

```text
alert_required = true if total_score >= 5
```

Add special trigger support:

```text
single_parameter_score_3 = true
```

If any individual parameter scores 3, mark:

```text
single_parameter_trigger = true
```

This should be documented because a single extreme physiological parameter can be clinically important even if the total is below 5.

---

# OUTPUT STRUCTURE

The NEWS2 engine should return a structured result.

Example:

```json
{
  "respiratory_score": 0,
  "spo2_score": 1,
  "oxygen_score": 0,
  "systolic_bp_score": 0,
  "pulse_score": 1,
  "temperature_score": 0,
  "consciousness_score": 0,
  "total_score": 2,
  "risk_level": "low",
  "alert_required": false,
  "single_parameter_trigger": false,
  "trigger_reason": "NEWS2 total score below alert threshold"
}
```

---

# IMPLEMENTATION FILES

Prefer implementing the engine in:

```text
app/services/news2_service.py
```

If useful, create:

```text
app/news2/
├── __init__.py
├── engine.py
├── constants.py
└── validators.py
```

Choose the cleaner architecture, but avoid overengineering.

The implementation must be reusable by:

- API routes
- seed data
- future write workflows
- future alert engine
- future analytics

---

# PYDANTIC SCHEMAS

Add or update schemas in:

```text
app/schemas.py
```

Required schemas:

```text
NEWS2CalculationRequest
NEWS2CalculationResult
NEWS2ComponentScores
```

Request fields:

```text
respiratory_rate
spo2
oxygen_therapy
systolic_bp
pulse_rate
temperature
consciousness_level
spo2_scale
```

Validation rules:

- respiratory_rate must be positive
- spo2 must be between 0 and 100
- systolic_bp must be positive
- pulse_rate must be positive
- temperature must be clinically plausible
- consciousness_level must be one of allowed values
- spo2_scale must default to `scale_1`

Use practical clinical validation ranges, not overly restrictive ranges.

---

# API ENDPOINT

Create a calculation endpoint:

```text
POST /api/news2/calculate
```

Request example:

```json
{
  "respiratory_rate": 18,
  "spo2": 95,
  "oxygen_therapy": false,
  "systolic_bp": 125,
  "pulse_rate": 88,
  "temperature": 37.2,
  "consciousness_level": "alert",
  "spo2_scale": "scale_1"
}
```

Response:

```json
{
  "respiratory_score": 0,
  "spo2_score": 1,
  "oxygen_score": 0,
  "systolic_bp_score": 0,
  "pulse_score": 0,
  "temperature_score": 0,
  "consciousness_score": 0,
  "total_score": 1,
  "risk_level": "low",
  "alert_required": false,
  "single_parameter_trigger": false,
  "trigger_reason": "NEWS2 total score below alert threshold"
}
```

Do not save this calculation to the database yet unless a safe optional helper exists.

Persistence belongs to a later workflow phase.

---

# SEED DATA ALIGNMENT

Update seed data so seeded NEWS2 assessment records are generated using the new engine instead of hardcoded inconsistent scoring.

Requirements:

- Seed assessments must remain medically plausible.
- Existing API tests should still pass.
- Research summary average NEWS2 must remain valid.
- Do not create duplicate data on repeated seed runs.

---

# FRONTEND PREPARATION

Add a small frontend helper for future use if appropriate.

Do not fully redesign the NEWS2 screen.

Allowed improvements:

- Add a NEWS2 calculator demo panel if simple and safe.
- Use the new `POST /api/news2/calculate` endpoint.
- Show component scores.
- Show total score.
- Show Arabic risk label.
- Show alert required flag.
- Show a medical disclaimer note.

Do not convert the whole monitoring workflow yet.

If adding frontend integration is too risky, document the endpoint and leave UI connection for the next phase.

---

# ARABIC LABELS

Add Arabic display helpers if needed.

Risk labels:

```text
low      => منخفض
medium   => متوسط
high     => مرتفع
critical => حرج
```

Consciousness labels:

```text
alert         => يقظ
voice         => يستجيب للصوت
pain          => يستجيب للألم
unresponsive  => لا يستجيب
new_confusion => ارتباك حديث
```

Trigger labels:

```text
NEWS2 total score below alert threshold
NEWS2 total score requires clinical alert
Single parameter scored 3
```

Arabic UI wording must be professional and clinical.

---

# TESTING REQUIREMENTS

Add strong unit tests for NEWS2 scoring.

Create:

```text
tests/test_news2_engine.py
```

Test all component boundaries.

Required test categories:

## Respiratory Rate

Test:

```text
8, 9, 11, 12, 20, 21, 24, 25
```

## SpO2 Scale 1

Test:

```text
91, 92, 93, 94, 95, 96
```

## Oxygen Therapy

Test:

```text
true, false
```

## Systolic BP

Test:

```text
90, 91, 100, 101, 110, 111, 219, 220
```

## Pulse Rate

Test:

```text
40, 41, 50, 51, 90, 91, 110, 111, 130, 131
```

## Temperature

Test:

```text
35.0, 35.1, 36.0, 36.1, 38.0, 38.1, 39.0, 39.1
```

## Consciousness

Test all allowed consciousness values.

## Total Score

Test low, medium, and high classifications.

## Single Parameter Trigger

Test at least one scenario where:

```text
total_score < 5
but one component score = 3
```

## API Test

Add or update:

```text
tests/test_news2_api.py
```

Test:

- valid request returns expected score
- invalid vitals return 422
- high score returns alert_required true

---

# DOCUMENTATION

Create or update:

```text
docs/news2_engine.md
```

Must include:

- Purpose of NEWS2 engine
- Scored parameters
- Score bands
- Risk classification
- Alert threshold
- Single-parameter trigger
- SpO2 Scale 1 default
- SpO2 Scale 2 caution
- Medical disclaimer
- API endpoint example
- Testing summary

Update:

```text
docs/system_architecture.md
docs/research_workflow.md
README.md
```

Mention that NEWS2 calculation engine now exists.

---

# VALIDATION COMMANDS

Run and report:

```bash
python -m compileall app
python -m app.seed
python -m pytest
node --check app/static/app.js
```

Also test manually:

```bash
uvicorn app.main:app --reload
```

Then call:

```text
POST http://127.0.0.1:8000/api/news2/calculate
```

with a valid sample request.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. NEWS2 engine architecture
4. Scoring rules implemented
5. API endpoint created
6. Seed data updates
7. Frontend changes, if any
8. Tests added
9. Validation results
10. Medical safety notes
11. Risks / next phase recommendation
12. Git commands

Do not skip validation.

---

# NEXT PHASE PREVIEW

After this phase, the recommended next phase is:

```text
Phase 05 — Monitoring Write Workflow
```

That phase will create real intradialytic measurement submission, calculate NEWS2 from submitted vitals, save the assessment, and prepare alert creation.
