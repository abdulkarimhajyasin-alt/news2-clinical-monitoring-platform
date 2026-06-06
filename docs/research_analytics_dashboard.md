# Research Analytics Dashboard

Phase 12 adds descriptive research analytics over the Phase 11 research dataset.

## KPI Definitions

The KPI dashboard is calculated from research dataset rows:

- `total_patients`: unique anonymized patient codes.
- `total_sessions`: unique dialysis sessions.
- `total_measurements`: unique intradialytic measurements.
- `total_news2_assessments`: unique NEWS2 assessments.
- `total_alerts`: unique alerts.
- `total_deterioration_events`: unique deterioration events.
- `total_responses`: unique clinical responses.
- `total_outcomes`: unique clinical outcomes.
- `average_news2_score`: mean NEWS2 total score.
- `average_response_time_minutes`: mean time to response.
- `alerts_per_100_sessions`: alerts divided by sessions, multiplied by 100.
- `deterioration_rate`: deterioration events divided by sessions, multiplied by 100.
- `response_completion_rate`: responses divided by alerts.
- `outcome_completion_rate`: outcomes divided by deterioration events.
- `dataset_quality_score`: Phase 11 dataset quality score.

## Distribution Calculations

NEWS2 distribution uses these score buckets:

- `0_2`: very low.
- `3_4`: low.
- `5_6`: medium.
- `7_plus`: high.

Each bucket returns count and percentage. Percentages are adjusted so populated distributions total 100%.

Risk-level analysis returns count, percentage, outcome distribution, and average response time for `low`, `medium`, and `high`.

## Outcome Calculations

Outcome analysis covers:

- `stable_completed_session`
- `session_stopped_early`
- `hospital_admission`
- `emergency_department_transfer`
- `icu_admission`
- `death`

Good outcome rate currently counts `stable_completed_session`.

Adverse outcome rate counts hospital admission, emergency transfer, ICU admission, and death.

## Response Calculations

Response analytics calculate:

- Average time to alert.
- Average time to view.
- Average time to response.
- Average time to action.
- Average total response time.
- Fastest response.
- Slowest response.
- Median response.

Missing response timestamps remain nullable and are excluded from averages.

## Group Comparison Logic

The dashboard supports descriptive comparison for:

- `study_group`
- `study_phase`

Each comparison returns `group_a` and `group_b` with row count, average NEWS2, average response time, and outcome distribution. Empty or single-group datasets return safe empty structures.

## Limitations

Phase 12 does not implement:

- T-tests.
- ANOVA.
- Regression.
- Prediction.
- Machine learning.
- Publication-ready statistical inference.

Pre/post support is descriptive only and returns baseline/intervention counts and averages.

## Research Usage Notes

The dashboard is intended for study monitoring, quality review, and descriptive visibility. It should not be interpreted as statistical proof of effect without later inferential analysis and protocol review.

## Phase 13 Integration

The Study Management & Research Protocol Center consumes these analytics as one readiness input. Analytics are considered available when the dataset contains NEWS2 assessment rows and the descriptive KPI layer can be calculated. The study readiness score remains an operational governance signal, not a statistical-validity statement.
