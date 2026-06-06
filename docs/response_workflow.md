# Medical and Nursing Response Workflow

## Purpose

The response workflow records the primary medical and nursing response after a clinical deterioration event. It preserves traceability from the patient and dialysis session through NEWS2, alert, deterioration event, and documented response.

## Relationship to Deterioration Events and Alerts

A response is created from a clinical deterioration event. The service derives the alert relationship from that event and stores the alert creation time as `digital_alert_time`.

The response record stores:

- Actual response start time.
- Response delay in minutes.
- Patient actions.
- Vascular access actions.
- Responding user.
- Notes.

## Patient Actions

- `stop_ultrafiltration`
- `give_fluids`
- `give_oxygen`
- `position_adjustment`
- `medication_given`
- `doctor_called`
- `transfer_prepared`
- `other`

## Vascular Access Actions

- `check_flow`
- `inspect_access_site`
- `blood_culture_from_catheter`
- `catheter_evaluation`
- `other`

## Response Delay

`response_delay_minutes` is calculated as:

```text
actual_response_start_time - digital_alert_time
```

If timestamps cannot be compared safely, the delay is stored as null instead of failing the workflow.

## Duplicate Prevention

The MVP supports one primary response record per deterioration event. If a response already exists for the event, the API returns the existing response and writes an audit log entry.

## API Endpoints

```http
POST /api/responses
GET /api/responses
GET /api/responses/{id}
```

List filters:

- `clinical_deterioration_event_id`
- `alert_id`
- `patient_id`
- `dialysis_session_id`
- `responded_by_user_id`
- `limit`

## UI Behavior

Event Details includes a response form. Medical Response Log, Nursing Response Log, and Response Workflow screens use real response API data. Delay badges are display-only: green for 5 minutes or less, orange for 6-15 minutes, and red above 15 minutes.

Phase 09 extends the Response Workflow screen with persisted response tracking data. The timeline now shows vital signs recorded, alert created, alert viewed, deterioration event opened, response started, and alert closed. Missing optional steps remain visible as pending.

## Clinical Safety Note

The response log documents clinical actions but does not replace local clinical policy or professional judgment. Outcome tracking and full timing analytics remain deferred.

## Response Tracking

The response tracking engine computes and persists:

- `time_to_alert_minutes`
- `time_to_view_minutes`
- `time_to_response_minutes`
- `time_to_action_minutes`
- `total_response_time_minutes`

For Phase 09 MVP, `clinical_action_at` uses `actual_response_start_time`. Negative durations are stored as null metrics with service warnings instead of being silently accepted.
