# Codex Prompt — Phase 18A: HD2-mNEWS Core Engine Alignment

## Objective
Implement Phase 18A of the NEWS2 Hemodialysis Monitoring Platform by aligning the monitoring calculation engine with the doctor-provided digital monitoring form.

The current system already supports standard NEWS2, monitoring measurements, alerts, deterioration, responses, outcomes, research datasets, analytics, authentication, RBAC, and patient lifecycle workflows. Phase 18 navigation cleanup has already been completed.

The next required step is to implement the study-specific modified hemodialysis early warning score:

`HD2-mNEWS`

This score must be based on 10 variables:

### 6 original NEWS2 variables
1. RR — Respiratory Rate
2. SpO2 — Oxygen Saturation
3. Temp — Temperature
4. SBP — Systolic Blood Pressure
5. HR — Heart Rate
6. AVPU — Consciousness Level

### 4 hemodialysis-specific variables
7. Fistula / Vascular Access Status
8. IDWG — Interdialytic Weight Gain percentage
9. UFR — Ultrafiltration Rate
10. K+ — Serum Potassium

The implementation must be professional, clinically clear, Arabic-first in the UI, production-safe, and compatible with the current architecture.

---

## Critical Scope Rules

- Do not remove or break the existing standard NEWS2 calculation unless necessary.
- Prefer adding HD2-mNEWS as a new study-specific layer that can coexist with current data.
- Preserve existing APIs where possible.
- Preserve current RBAC, authentication, patient lifecycle restrictions, audit logging, and research export protections.
- Do not add unrelated hospital/EMR features.
- Do not add IoT/device integration.
- Do not add complex clinical assignment or shift management.
- Focus strictly on what the doctor’s final digital monitoring form requires.

---

## Required Clinical Scoring Rules

### 1. Respiratory Rate — RR

| Range | Points |
|---|---:|
| 12–20 | 0 |
| 9–11 or 21–24 | 1 |
| ≤8 or ≥25 | 2 |

### 2. Oxygen Saturation — SpO2

| Range | Points |
|---|---:|
| ≥96% | 0 |
| 94–95% | 1 |
| 92–93% | 2 |
| ≤91% | 3 + automatic red alert |

### 3. Temperature — Temp

| Range | Points |
|---|---:|
| 36.1–38.0 | 0 |
| ≤36.0 or 38.1–39.0 | 1 |
| ≥39.1 | 2 |

### 4. Systolic Blood Pressure — SBP

| Range | Points |
|---|---:|
| 111–219 | 0 |
| 101–110 or 220–229 | 1 |
| ≤100 or ≥230 | 2 |
| ≤90 with symptoms | 3 + automatic red alert |

Add a boolean field if needed:

`sbp_symptomatic_hypotension`

### 5. Heart Rate — HR

| Range | Points |
|---|---:|
| 51–90 | 0 |
| 41–50 or 91–110 | 1 |
| ≤40 or ≥111 | 2 |

### 6. AVPU

| Value | Points |
|---|---:|
| Alert | 0 |
| Voice | 1 |
| Pain | 2 |
| Unresponsive | 3 + automatic red alert |

### 7. Fistula / Vascular Access Status

| Status | Description | Points |
|---|---|---:|
| normal | Strong regular thrill/bruit, no bleeding, no redness | 0 |
| weak | Weaker than usual, simple bruise | 1 |
| disturbed | Intermittent thrill/bruit, redness/warmth, bleeding <10 min | 2 |
| critical | Missing thrill/bruit, heavy bleeding, pus, red streak | 3 + automatic red alert |

### 8. IDWG Percentage

Formula:

`IDWG% = ((pre_dialysis_weight - dry_weight) / dry_weight) * 100`

| Range | Points |
|---|---:|
| <3% | 0 |
| 3–5% | 1 |
| 5–7% | 2 |

If value is greater than 7%, keep it clinically visible and assign at least 2 points unless existing domain logic suggests otherwise. Do not invent a 3-point category unless explicitly required elsewhere.

### 9. UFR

Formula:

`UFR = fluid_to_remove / (dry_weight * session_duration_hours)`

| Range | Points |
|---|---:|
| ≤10 | 0 |
| 10.1–13 | 1 |
| 13.1–15 | 2 |

If value is greater than 15, keep it clinically visible and assign at least 2 points unless existing domain logic suggests otherwise. Do not invent a 3-point category unless explicitly required elsewhere.

### 10. Potassium — K+

| Range | Points |
|---|---:|
| 3.5–5.0 | 0 |
| 3.0–3.4 or 5.1–5.5 | 1 |
| 2.5–2.9 or 5.6–6.0 | 2 |
| <2.5 or >6.0 | 3 + automatic red alert |

---

## Total Score

Add:

`hd2_mnews_total_score`

It must equal the sum of all 10 variables.

Expected range based on the doctor’s form:

`0–33`

Do not worry if the implemented category ranges make the practical maximum lower unless all fields support the doctor’s 0–33 statement. Preserve the doctor-facing label as `0–33` in UI text if already required by the form.

---

## Risk Color Engine

Add risk color classification:

| Condition | Risk Color | Arabic Label |
|---|---|---|
| 0–4 points | green | أخضر / آمن |
| 5–6 points | yellow | أصفر / مراقبة |
| ≥7 points | red | أحمر / طوارئ |
| Any critical 3-point variable | red | أحمر تلقائي |

Critical automatic red variables:

- AVPU = Unresponsive
- SpO2 ≤91%
- SBP ≤90 with symptoms
- Potassium <2.5 or >6.0
- Fistula / vascular access = critical

Store or return:

- `hd2_mnews_total_score`
- `hd2_mnews_risk_color`
- `hd2_mnews_risk_label_ar`
- `hd2_mnews_critical_trigger`
- `hd2_mnews_critical_reasons`
- component scores for all 10 variables

---

## Backend Requirements

### 1. Add or update calculation service

Preferred approach:

Create a dedicated service/module, for example:

`app/services/hd2_mnews_service.py`

or follow the current project structure if there is already a scoring/calculation module.

The service should expose a clear function such as:

`calculate_hd2_mnews(payload)`

or a typed equivalent.

It must be testable independently from routes.

### 2. Extend Pydantic schemas

Add request/response schemas for HD2-mNEWS calculation.

Include all required fields and optional derived fields:

- respiratory_rate
- oxygen_saturation
- temperature
- systolic_bp
- heart_rate
- consciousness_level
- vascular_access_status
- pre_dialysis_weight
- dry_weight
- session_duration_hours
- fluid_to_remove
- potassium
- sbp_symptomatic_hypotension

Derived:

- idwg_percent
- ufr
- component scores
- total score
- risk color
- risk label
- critical trigger metadata

### 3. Add calculation endpoint

Add endpoint if appropriate:

`POST /api/hd2-mnews/calculate`

It should return the full scoring breakdown.

Keep existing `/api/news2/calculate` endpoint intact.

### 4. Integrate with monitoring measurement creation

When a new monitoring measurement is created, the system should calculate and persist HD2-mNEWS if the necessary hemodialysis fields are available.

If the current measurement workflow cannot safely persist all fields yet, add the minimum schema/model fields required for Phase 18A without breaking existing records.

Use nullable fields or safe migrations/startup compatibility patches according to the current project’s migration/startup style.

### 5. Database compatibility

If adding columns/tables:

- Use safe additive changes only.
- Do not drop or rename existing columns.
- Ensure startup table creation remains safe on Render/Neon.
- Preserve existing data.

Recommended persisted fields may include:

- hd2_mnews_total_score
- hd2_mnews_risk_color
- hd2_mnews_critical_trigger
- hd2_mnews_breakdown_json
- vascular_access_status
- pre_dialysis_weight
- dry_weight
- session_duration_hours
- fluid_to_remove
- potassium
- idwg_percent
- ufr
- sbp_symptomatic_hypotension

Use the project’s existing JSON/SQLAlchemy conventions.

---

## Frontend Requirements

### 1. Monitoring digital form

Update the Arabic digital monitoring form to include the four hemodialysis-specific variables:

- حالة الوصول الوعائي
- الوزن قبل الجلسة
- الوزن الجاف
- مدة الجلسة بالساعات
- كمية السوائل المطلوب سحبها
- بوتاسيوم الدم
- أعراض هبوط الضغط الشديد عند الحاجة

### 2. Derived calculations in UI

Show calculated:

- IDWG%
- UFR
- HD2-mNEWS total score
- Risk color
- Component breakdown

Frontend can preview calculations, but backend must be the source of truth.

### 3. Arabic labels

Use Arabic-first labels:

- أخضر / آمن
- أصفر / مراقبة
- أحمر / طوارئ
- أحمر تلقائي

Keep the visual style consistent with the current medical RTL design.

### 4. Do not overload the UI

If the current form becomes too long, group fields professionally:

- العلامات الحيوية الأساسية
- متغيرات الغسيل الكلوي
- نتيجة HD2-mNEWS

---

## Testing Requirements

Add regression tests for the HD2-mNEWS service and endpoint.

Minimum test cases:

1. Normal values → green risk, score 0.
2. Score 5–6 → yellow risk.
3. Total score ≥7 → red risk.
4. SpO2 ≤91 → automatic red.
5. AVPU Unresponsive → automatic red.
6. SBP ≤90 with symptoms → automatic red.
7. Potassium >6.0 → automatic red.
8. Fistula critical → automatic red.
9. IDWG formula is calculated correctly.
10. UFR formula is calculated correctly.
11. Existing standard NEWS2 endpoint still works.
12. Existing monitoring measurement tests still pass.

---

## Validation Commands

Run:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

If the project has additional JS files touched, run `node --check` on them as well.

---

## Expected Final Response From Codex

When complete, provide:

1. Objective summary
2. Files changed
3. Backend changes
4. Frontend changes
5. Scoring rules implemented
6. Tests added/updated
7. Validation command results
8. Risk analysis
9. Final GitHub commands

Use these final GitHub commands:

```bash
git add .
git commit -m "Add HD2-mNEWS scoring engine"
git push origin main
```
