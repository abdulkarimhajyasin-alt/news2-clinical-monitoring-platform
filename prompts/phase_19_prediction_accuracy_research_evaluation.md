# Phase 19 — Prediction Accuracy & Research Evaluation Module

## Objective
Implement the research evaluation layer required by the PhD protocol to measure whether the HD2-mNEWS digital monitoring platform successfully predicted clinical deterioration in hemodialysis patients.

This phase must transform the stored 72-hour outcome validation data into research-ready prediction performance metrics without changing or breaking the existing NEWS2, HD2-mNEWS, alert, response, outcome, RBAC, authentication, lifecycle, or export workflows.

The platform must remain Arabic-first, RTL, production-safe, and aligned strictly with the doctor’s final digital monitoring form.

---

## Current Baseline
The project already has:

- Standard NEWS2 calculation and persistence.
- HD2-mNEWS 10-variable scoring engine.
- Risk colors: green, yellow, red.
- Nursing protocol guidance by color.
- Patient baseline/context fields.
- Dialysis session context fields.
- Alerts, responses, outcomes, research dataset/export, analytics, studies, RBAC, authentication, lifecycle.
- 72-hour post-dialysis outcome validation linked to dialysis sessions.

Phase 19 must build on those existing structures.

---

## Study Logic to Implement
The 72-hour validation form already captures whether deterioration occurred and whether the platform predicted it.

Use the validation field equivalent to:

- `predicted_before_event`
- `predicted_at_event`
- `not_predicted`
- `false_negative`

If the exact field names differ in the implementation, inspect the current schemas/models/services and use the existing names.

The research evaluation layer must classify each validated session into prediction outcome categories.

### Prediction Classification Rules

For each dialysis session with a completed 72-hour validation:

#### True Positive — Early
Patient deteriorated and platform predicted before occurrence.

#### True Positive — Concurrent
Patient deteriorated and platform alerted at the time of deterioration.

#### False Negative
Patient deteriorated and platform did not alert, or validation explicitly marks false negative.

#### True Negative
Patient did not deteriorate and no red/high-risk HD2-mNEWS alert was present for the session.

#### False Positive
Patient did not deteriorate but HD2-mNEWS produced a red/high-risk alert during the session.

#### Unclassified / Incomplete
Validation missing, incomplete, or insufficient data to classify.

Do not guess silently. If data is insufficient, classify as incomplete and expose the reason.

---

## Backend Requirements

### 1. Add Research Evaluation Service
Create a dedicated service, for example:

`app/services/research_evaluation_service.py`

It should provide deterministic functions such as:

- `classify_session_prediction(...)`
- `build_prediction_evaluation_dataset(...)`
- `build_prediction_summary(...)`
- `build_prediction_by_risk_color(...)`
- `build_prediction_by_deterioration_type(...)`
- `build_response_time_prediction_summary(...)`

Keep the service pure where practical and testable independently from the router.

---

### 2. Add API Router
Create a router, for example:

`app/routers/research_evaluation.py`

Register it in `app/main.py`.

Required endpoints:

```http
GET /api/research/evaluation/prediction-dataset
GET /api/research/evaluation/prediction-summary
GET /api/research/evaluation/by-risk-color
GET /api/research/evaluation/by-deterioration-type
GET /api/research/evaluation/response-time-summary
```

Use existing `research:view` or `research:analytics` permission gates consistently with current research analytics routes.

Do not expose this to unauthorized roles.

---

### 3. Prediction Summary Metrics
The summary endpoint must return at minimum:

- total_sessions
- validated_sessions
- unvalidated_sessions
- deteriorated_sessions
- non_deteriorated_sessions
- true_positive_early
- true_positive_concurrent
- true_positive_total
- false_negative
- true_negative
- false_positive
- incomplete_classification_count
- sensitivity
- specificity
- positive_predictive_value
- negative_predictive_value
- early_detection_rate
- false_negative_rate
- false_positive_rate

Use safe division. If denominator is zero, return `null` instead of crashing.

### Metric Definitions

- Sensitivity = TP / (TP + FN)
- Specificity = TN / (TN + FP)
- PPV = TP / (TP + FP)
- NPV = TN / (TN + FN)
- Early detection rate = TP early / deteriorated sessions
- False negative rate = FN / deteriorated sessions
- False positive rate = FP / non-deteriorated sessions

Where:

- TP total = true_positive_early + true_positive_concurrent

---

### 4. Dataset Rows
The prediction dataset endpoint should return row-level research data for each eligible dialysis session.

Include at minimum:

- patient_id
- patient_code / coded medical number
- session_id
- session_date
- session_start_time
- hd2_mnews_total_score
- hd2_risk_color
- hd2_risk_label_ar
- critical_trigger_present
- critical_trigger_reasons
- red_alert_present
- deterioration_occurred
- deterioration_types
- deterioration_timing
- prediction_status_from_validation
- prediction_classification
- classification_reason
- doctor_response_time_minutes
- final_result
- verification_sources

Do not include deleted patients. Preserve the existing deleted-patient exclusion behavior.

---

### 5. Research Export Alignment
Extend the existing export center so CSV/XLSX exports include the new prediction evaluation fields.

Do not remove existing export columns.

Add clearly named columns for:

- prediction_classification
- true_positive_early
- true_positive_concurrent
- false_negative
- true_negative
- false_positive
- sensitivity_group_marker if useful
- specificity_group_marker if useful
- early_detection_marker
- classification_reason

Keep exports stable and deterministic.

---

## Frontend Requirements

### 1. Add Arabic Research Evaluation Screen
Add a new visible page under the research/analytics area with Arabic labels.

Suggested sidebar item:

`تقييم التنبؤ`

Only show it to users with the same permission required for research analytics.

### 2. Screen Content
The page should include:

#### KPI Cards
- الجلسات المؤهلة
- الجلسات التي تم التحقق منها بعد 72 ساعة
- حالات التدهور
- التنبؤ المبكر الصحيح
- التنبؤ المتزامن الصحيح
- الحالات السلبية الكاذبة
- الحساسية
- النوعية
- معدل الكشف المبكر

#### Tables / Sections
- جدول تصنيف الجلسات.
- تحليل حسب لون الخطورة: أخضر / أصفر / أحمر.
- تحليل حسب نوع التدهور.
- ملخص زمن استجابة الطبيب عند توفره.

### 3. UX Rules
- Keep the UI Arabic-first and RTL.
- Preserve current visual identity.
- Use clear medical/research wording, not generic dashboard wording.
- Do not overcrowd the page.
- Show empty states when no validations are available yet.
- Show percentages with a clear denominator when possible.

---

## Tests Required

Add or update tests for:

### Service Tests
- True positive early classification.
- True positive concurrent classification.
- False negative classification.
- True negative classification.
- False positive classification.
- Incomplete classification.
- Safe division with zero denominators.

### API Tests
- Permission protection.
- Prediction summary returns expected metrics.
- Prediction dataset excludes deleted patients.
- By-risk-color grouping works.
- By-deterioration-type grouping works.

### Export Tests
- CSV/XLSX export contains prediction classification fields.
- Deleted patients remain excluded.

### Frontend Regression Tests
If the project has existing navigation tests, add `تقييم التنبؤ` to the permitted research sidebar scope and ensure no removed out-of-scope pages reappear.

---

## Non-Negotiable Constraints

- Do not remove or break standard NEWS2.
- Do not remove or break HD2-mNEWS.
- Do not change scoring thresholds unless directly required by existing code defects.
- Do not change patient lifecycle restrictions.
- Do not expose deleted patients in research outputs.
- Do not weaken RBAC/auth/session security.
- Do not introduce destructive migrations.
- Use nullable/additive schema changes only if needed.
- Preserve Arabic-first UI and current design language.
- Keep implementation production-safe and test-covered.

---

## Validation Commands
Run all of the following:

```bash
python -m compileall app
node --check app/static/app.js
python -m pytest
git diff --check
```

If `pytest` is not available directly, use:

```bash
python -m pytest
```

---

## Final Response Required from Codex
At the end, report:

1. Objective summary.
2. Files changed.
3. Backend changes.
4. Frontend changes.
5. Export changes.
6. Tests added/updated.
7. Validation results.
8. Risk analysis.
9. Final GitHub commands.

Include final GitHub commands:

```bash
git add .
git commit -m "Add prediction accuracy research evaluation"
git push origin main
```
