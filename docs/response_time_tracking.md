# Response Time Tracking Engine

Phase 09 adds persisted response-time metrics for the NEWS2 hemodialysis deterioration workflow.

## Purpose

Response tracking preserves the research traceability chain from patient and dialysis session through vital-sign measurement, NEWS2 assessment, alert, deterioration event, medical/nursing response, and final response-time metrics.

The goal is to support analysis of whether digital NEWS2 monitoring improves early detection and clinical response time.

## Timestamp Sources

- `vital_signs_recorded_at`: `intradialytic_measurements.measurement_time`, falling back to `created_at`.
- `alert_created_at`: `alerts.created_at`.
- `alert_viewed_at`: `alerts.viewed_at`, optional.
- `actual_response_start_time`: `clinical_responses.actual_response_start_time`, optional until response is documented.
- `clinical_action_at`: Phase 09 MVP uses `clinical_responses.actual_response_start_time`.
- `alert_closed_at`: `alerts.closed_at`, optional.

## Metric Formulas

All metrics are integer minutes.

- `time_to_alert_minutes`: alert created minus vital signs recorded.
- `time_to_view_minutes`: alert viewed minus alert created.
- `time_to_response_minutes`: response start minus alert created.
- `time_to_action_minutes`: clinical action minus alert created.
- `total_response_time_minutes`: response start minus vital signs recorded.

## Null And Invalid Timestamp Handling

Missing optional timestamps produce `null` metrics and do not block workflow progression.

Negative durations are never silently accepted. The metric is set to `null`, and the service result includes a warning, for example after manual repair or test data with an invalid timestamp sequence.

## API Endpoints

- `GET /api/response-tracking`: list enriched tracking records, newest first.
- `GET /api/response-tracking/{id}`: read one enriched tracking record.
- `POST /api/response-tracking/recalculate/{alert_id}`: recalculate and upsert one alert tracking row.
- `GET /api/response-tracking/summary`: aggregate response-time KPIs.

## UI Behavior

The Response Time Dashboard and Response Analytics screens consume the real tracking endpoints. They display KPI cards, response tracking tables, simple charts, and a workflow timeline showing completed and pending timestamps.

## Audit Behavior

Tracking writes create audit log entries:

- `response_tracking_created`
- `response_tracking_updated`
- `response_tracking_recalculated`

## Safety Note

The engine supports research and operational review. It does not replace clinical judgment, escalation policy, or bedside assessment.

## Later Phases

Phase 10 now adds 24-72h outcome capture after deterioration events. Later phases should add SPSS export, richer research comparison, and formal role-based access control.
