# Monitoring Write Workflow

## Purpose

The intradialytic monitoring workflow records vital-sign measurements during a dialysis session and immediately calculates NEWS2 from the submitted clinical observations.

This workflow converts the platform from read-only monitoring to persisted measurement capture and governed alert creation.

## Submission Workflow

```text
Create intradialytic measurement
Calculate NEWS2 using the Phase 04 engine
Create linked NEWS2 assessment
Evaluate governed alert rules
Return measurement and assessment to the frontend
```

The write endpoint is:

```http
POST /api/monitoring/measurements
```

The endpoint validates:

- Patient exists.
- Dialysis session exists.
- Dialysis session belongs to the patient.
- Vital signs are clinically plausible.
- Consciousness level and SpO2 scale use supported values.

## Database Records Created

Each successful submission creates:

- One `intradialytic_measurements` row.
- One linked `news2_assessments` row.
- One linked `alerts` row only when Phase 06 alert rules require it and no active patient/session alert already exists.

No `clinical_deterioration_events`, `response_tracking`, or `clinical_outcomes` rows are created in Phase 06.

## NEWS2 Integration

The service calls the reusable NEWS2 engine after saving the measurement in the same transaction. The generated assessment stores component scores, total score, risk level, alert requirement flag, and trigger reason.

`single_parameter_trigger` is returned in API responses for frontend and future workflow use, but it is not stored as a database column in this phase.

## Alert Creation Boundary

Alerts are now created or reused automatically after the NEWS2 assessment is persisted. Clinical deterioration events, response tracking, and outcomes remain deferred so alert generation stays auditable and separate from later response workflows.

## Clinical Safety Note

NEWS2 supports early detection of clinical deterioration but does not replace clinical judgment. All results must be interpreted by qualified healthcare professionals, and the implementation requires clinical review before real-world deployment.
