# Patient Lifecycle Workflow

Phase 17 adds safe patient discharge, archive, restore, and soft-delete workflows.

## Statuses

- `active`: visible in operational lists and available for clinical workflows.
- `discharged`: retained for clinical/research traceability but hidden from active operational lists.
- `archived`: retained for research/export context but hidden from normal operational lists.
- `deleted`: soft-deleted. The patient is hidden from normal UI and default lists; related clinical rows remain intact.

Hard physical delete is intentionally avoided because hemodialysis monitoring records may be part of clinical audit and research traceability.

## API

- `GET /api/patients`: active patients by default.
- `GET /api/patients?status=discharged`: discharged patients.
- `GET /api/patients?status=archived`: archived patients.
- `GET /api/patients?status=deleted&include_deleted=true`: deleted patients, admin only.
- `POST /api/patients/{id}/discharge`
- `POST /api/patients/{id}/archive`
- `POST /api/patients/{id}/restore`
- `POST /api/patients/{id}/delete`

Safe delete requires a reason and exact confirmation text: `DELETE PATIENT` or `حذف المريض`.

## Permissions

- `admin`: discharge, archive, restore, delete.
- `technical_admin`: archive and restore.
- `doctor`: discharge and restore.
- `on_call_doctor`, `nurse`, `researcher`: view only for lifecycle actions.

## Clinical Safety

The backend blocks new intradialytic measurements for patients whose status is not `active`. The frontend also limits vital-sign entry options to active patients.

## Audit

Lifecycle transitions write audit rows:

- `patient_discharged`
- `patient_archived`
- `patient_restored`
- `patient_soft_deleted`

Audit values include patient id, patient code, actor user id when available, and the lifecycle reason.

## Research

Discharged and archived patients remain available to research summaries and dataset traceability. Soft-deleted patients are hidden from operational patient lists by default, while related clinical records remain preserved.
