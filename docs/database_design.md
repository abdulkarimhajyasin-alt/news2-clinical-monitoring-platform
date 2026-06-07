# Database Design

The schema uses English table and field names with SQLAlchemy models. Arabic display text belongs in the frontend/i18n layer, not in database identifiers.

Core tables:

- `users`: staff identity, role, department, language preference, status, timestamps.
- `auth_sessions`: hashed HTTP-only cookie session tokens, owning user, expiration, and last-seen timestamps.
- `patients`: anonymized patient baseline and study grouping.
- `patient_vascular_access`: access type, location, insertion date, notes.
- `dialysis_sessions`: session timing, prescription/operational settings, status.
- `intradialytic_measurements`: repeated vital signs and consciousness observations.
- `news2_assessments`: NEWS2 component scores, total score, risk level, trigger reason.
- `alerts`: alert severity, status, priority, assignment, timestamps.
- `clinical_deterioration_events`: deterioration type, timing, NEWS2 trigger, description.
- `clinical_responses`: patient actions, vascular access actions, response delay, notes.
- `response_tracking`: measured response timeline intervals.
- `clinical_outcomes`: 24-72 hour outcome classification and description.
- `clinical_notes`: structured clinical notes attached to workflow entities.
- `research_studies`: research study metadata.
- `audit_logs`: user action traceability.
- `system_settings`: configurable platform settings.

Key relationships:

- Patient to vascular access.
- Patient to dialysis sessions.
- Dialysis session to measurements.
- Measurement to NEWS2 assessment.
- NEWS2 assessment to alert.
- Alert to clinical deterioration event.
- Clinical deterioration event to clinical response.
- Clinical deterioration event to clinical outcome.
- User to created sessions.
- User to recorded measurements.
- User to audit logs.

Locking fields:

Clinical and research records that may become part of a locked dataset include `is_locked`, `locked_at`, and `locked_by_user_id`. These fields support future data integrity controls without deleting or rewriting research evidence.

Research data governance:

- Use anonymized patient codes in research exports.
- Avoid storing direct identifiers in exported datasets.
- Preserve audit logs for sensitive actions.
- Lock finalized study records before analysis.
- Prefer additive corrections over destructive updates.

Export privacy rules:

- Exports must exclude passwords, direct contact details, and operational-only identifiers.
- Exports should include only approved research variables.
- Export requests should be auditable and linked to study approval metadata in future phases.
