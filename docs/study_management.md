# Study Management and Research Protocol Center

Phase 13 adds a governance layer above the clinical, export, and analytics workflows.

## Scope

The study management center supports:

- Study registry records in `research_studies`.
- Protocol configuration for design, periods, groups, sample size, and notes.
- Study timeline visibility.
- Research readiness checks.
- Audit events for study creation, update, and readiness review.

This phase does not implement authentication, RBAC, publication writing, statistical inference, or multi-center federation.

## API

- `POST /api/studies`
- `GET /api/studies`
- `GET /api/studies/{study_id}`
- `PUT /api/studies/{study_id}`
- `GET /api/studies/{study_id}/readiness`

## Readiness Engine

The readiness report evaluates:

- `study_defined`
- `dataset_available`
- `analytics_available`
- `exports_available`
- `outcomes_available`
- `response_tracking_available`

The readiness score is the percentage of completed checks, returned as `0-100`.

## Audit Log Actions

- `study_created`
- `study_updated`
- `study_readiness_viewed`

## Safety Notes

The readiness engine is descriptive. It confirms operational availability of research inputs and linked workflows, but it does not validate statistical power, publication suitability, IRB approval, or causal inference.

## RBAC

Phase 14 protects study endpoints:

- `studies:view` for listing, detail, and readiness.
- `studies:create` for creating study records.
- `studies:update` for editing protocol configuration.

The frontend disables study edit controls when the temporary development role lacks the required permission.
