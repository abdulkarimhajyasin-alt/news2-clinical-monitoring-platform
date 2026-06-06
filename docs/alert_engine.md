# Alert Creation Engine

## Purpose

The alert creation engine evaluates persisted NEWS2 assessments after monitoring measurements are saved. It creates governed clinical alerts while preventing duplicate active alerts for the same patient/session deterioration chain.

## Alert Thresholds

An alert is required when:

- NEWS2 total score is 5 or higher.
- Any single NEWS2 component scores 3, even when total score is below 5.

## Severity Mapping

- NEWS2 5-6: `risk_level = medium`, `severity_level = medium`, `priority = normal`.
- NEWS2 >= 7: `risk_level = high`, `severity_level = high`, `priority = urgent`.
- Single-parameter trigger with total score below 5: `risk_level = medium`, `severity_level = medium`, `priority = normal`.

## Duplicate Prevention

The engine checks for an existing active alert for the same patient and dialysis session before creating a new alert.

Active statuses are:

- `new`
- `viewed`
- `acknowledged`
- `in_progress`

If an active alert exists, the engine reuses it and returns the existing alert identifier instead of creating another row. If the newer assessment has a higher severity or priority, the existing alert is upgraded and an audit entry is written. This keeps the workflow to one active alert per active clinical deterioration chain while still reflecting clinical escalation.

## Alert Lifecycle

Supported statuses:

- `new`
- `viewed`
- `acknowledged`
- `in_progress`
- `closed`
- `cancelled`

Lifecycle endpoints:

```http
POST /api/alerts/{id}/view
POST /api/alerts/{id}/acknowledge
POST /api/alerts/{id}/start
POST /api/alerts/{id}/close
```

Each transition updates the matching timestamp field and writes an audit log entry.

## API Endpoints

Read:

```http
GET /api/alerts
GET /api/alerts/{id}
```

Supported filters on `GET /api/alerts`:

- `status`
- `risk_level`
- `severity_level`
- `patient_id`
- `dialysis_session_id`

Monitoring integration:

```http
POST /api/monitoring/measurements
```

This endpoint now saves the measurement, saves the NEWS2 assessment, evaluates alert rules, creates or reuses an alert when required, and returns `measurement`, `news2_assessment`, `alert`, and `message`.

Clinical deterioration integration:

```http
POST /api/deterioration/events
```

This endpoint creates or reuses a structured clinical deterioration event for an active alert. Closed and cancelled alerts cannot open new deterioration events.

## Audit Logging

Audit log entries are created when alerts are:

- Created.
- Reused because an active duplicate exists.
- Viewed.
- Acknowledged.
- Started.
- Closed.

## Clinical Safety Notes

Alerts are decision-support workflow aids. They do not replace clinical judgment, local escalation policy, or qualified professional assessment. Clinical deterioration events, response tracking, and outcomes are intentionally reserved for later phases.
