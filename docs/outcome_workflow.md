# Clinical Outcomes Workflow

Phase 10 adds 24-72 hour clinical outcome tracking after a documented clinical deterioration event.

## Purpose

Outcome tracking closes the research traceability chain from patient, dialysis session, measurement, NEWS2 assessment, alert, deterioration event, response, and response-time tracking through the final short-term clinical outcome.

This layer supports analysis of whether earlier detection and timely response are associated with safer post-event outcomes.

## Outcome Windows

The MVP supports one outcome record per deterioration event for each window:

- `24`
- `48`
- `72`

The value is stored in `clinical_outcomes.outcome_window_hours`.

## Outcome Types

- `stable_completed_session`
- `session_stopped_early`
- `hospital_admission`
- `emergency_department_transfer`
- `icu_admission`
- `death`

## Duplicate Prevention

The service enforces this MVP rule:

```text
one clinical_deterioration_event
+
one outcome_window_hours
=
one clinical_outcome
```

If the same event/window is submitted again, the API returns the existing record and writes a `clinical_outcome_reused` audit log instead of creating a duplicate row.

## API Endpoints

- `POST /api/outcomes`: create or reuse an outcome. Patient and session are derived from the deterioration event.
- `GET /api/outcomes`: list outcomes newest first, with filters for patient, session, event, type, window, and limit.
- `GET /api/outcomes/{id}`: read one enriched outcome.
- `GET /api/outcomes/summary`: return outcome counts by type.

## Analytics

Outcome summary metrics include:

- `total_outcomes`
- `stable_completed_session_count`
- `session_stopped_early_count`
- `hospital_admission_count`
- `emergency_department_transfer_count`
- `icu_admission_count`
- `death_count`

These metrics are also exposed through `/api/research/summary`.

## Research Relevance

The outcome layer provides the short-term clinical endpoint required to evaluate the NEWS2 hemodialysis monitoring workflow. It enables later dataset/export phases to compare response timing with hospital admission, emergency transfer, ICU admission, death, and stable session completion.

Phase 11 now includes outcomes in the research dataset/export layer. Export rows expose the first available 24-72h outcome for the linked deterioration event while preserving the measurement plus NEWS2 assessment as the primary row unit.

## Safety Note

Outcome records are research and clinical documentation artifacts. They do not replace bedside assessment, escalation policies, discharge criteria, or clinician judgment.
