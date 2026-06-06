# Clinical Deterioration Workflow

## Purpose

Clinical deterioration events turn clinically significant alerts into structured records that preserve the traceability chain from patient and dialysis session through vital signs, NEWS2 assessment, alert, and event.

This phase documents the deterioration event. Phase 08 adds the primary medical/nursing response record linked to the event, while full response time tracking and outcomes remain later workflow phases.

## Relationship to Alerts and NEWS2

A deterioration event is created from an existing active alert. The service derives patient, dialysis session, NEWS2 assessment, and triggering NEWS2 score from the alert relationship rather than trusting frontend-supplied identifiers.

Traceability:

```text
Patient
Dialysis Session
Intradialytic Measurement
NEWS2 Assessment
Alert
Clinical Deterioration Event
```

## Duplicate Prevention

Only one deterioration event can exist for a given alert. If a user tries to create another event for the same alert, the API returns the existing event with a duplicate-safe message and writes an audit log entry.

## Deterioration Types

- `acute_hypotension`
- `suspected_sepsis_or_fever`
- `arrhythmia`
- `seizures`
- `reduced_consciousness`
- `other`

## API Endpoints

```http
POST /api/deterioration/events
GET /api/deterioration/events
GET /api/deterioration/events/{id}
```

List filters:

- `patient_id`
- `dialysis_session_id`
- `alert_id`
- `deterioration_type`
- `limit`

## UI Behavior

The Active Alerts screen includes a form to open a deterioration event for an active alert. The Clinical Deterioration Events, Event Details, and Event Timeline screens use real API data.

The timeline shows vital-sign recording, NEWS2 calculation, alert creation, event creation, and a pending response-documentation step.

## Clinical Safety Note

The event record supports clinical documentation and research traceability. It does not replace clinical judgment, escalation policy, or response documentation. The response workflow is intentionally deferred to Phase 08.

## Later Phases

Phase 08 adds medical and nursing response documentation, response delays, clinical actions, and vascular access actions. Phase 09 should add full response-time tracking metrics.
