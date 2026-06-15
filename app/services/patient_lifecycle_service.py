from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import AuditLog, Patient
from app.rbac import CurrentUserContext
from app.schemas import PatientArchiveRequest, PatientDeleteRequest, PatientDischargeRequest


DELETE_CONFIRMATION_TEXTS = {"DELETE PATIENT", "حذف المريض"}
ACTIVE_STATUS = "active"
DISCHARGED_STATUS = "discharged"
ARCHIVED_STATUS = "archived"
DELETED_STATUS = "deleted"


class PatientLifecycleError(ValueError):
    pass


class PatientNotFoundError(PatientLifecycleError):
    pass


class PatientDeletedError(PatientLifecycleError):
    pass


class PatientDeleteConfirmationError(PatientLifecycleError):
    pass


class PatientRestorePermissionError(PatientLifecycleError):
    pass


def discharge_patient(db: Session, patient_id: int, payload: PatientDischargeRequest, current_user: CurrentUserContext) -> Patient:
    patient = _get_patient(db, patient_id)
    _ensure_not_deleted(patient)
    old_status = patient.status
    patient.status = DISCHARGED_STATUS
    patient.discharged_at = _now()
    patient.discharge_reason = payload.discharge_reason
    patient.discharge_notes = payload.discharge_notes
    _write_audit_log(db, patient, current_user, "patient_discharged", old_status, payload.discharge_reason)
    db.commit()
    db.refresh(patient)
    return patient


def archive_patient(db: Session, patient_id: int, payload: PatientArchiveRequest, current_user: CurrentUserContext) -> Patient:
    patient = _get_patient(db, patient_id)
    _ensure_not_deleted(patient)
    old_status = patient.status
    patient.status = ARCHIVED_STATUS
    patient.archived_at = _now()
    patient.archived_by_user_id = current_user.id
    _write_audit_log(db, patient, current_user, "patient_archived", old_status, payload.archive_reason or "archived")
    db.commit()
    db.refresh(patient)
    return patient


def restore_patient(db: Session, patient_id: int, current_user: CurrentUserContext) -> Patient:
    patient = _get_patient(db, patient_id)
    _ensure_restore_allowed(patient, current_user)
    old_status = patient.status
    patient.status = ACTIVE_STATUS
    _write_audit_log(db, patient, current_user, "patient_restored", old_status, "restore_to_active")
    db.commit()
    db.refresh(patient)
    return patient


def soft_delete_patient(db: Session, patient_id: int, payload: PatientDeleteRequest, current_user: CurrentUserContext) -> Patient:
    if payload.confirmation_text not in DELETE_CONFIRMATION_TEXTS:
        raise PatientDeleteConfirmationError("delete confirmation text is invalid")
    patient = _get_patient(db, patient_id)
    old_status = patient.status
    patient.status = DELETED_STATUS
    patient.deleted_at = _now()
    patient.deleted_by_user_id = current_user.id
    patient.delete_reason = payload.delete_reason
    _write_audit_log(db, patient, current_user, "patient_soft_deleted", old_status, payload.delete_reason)
    db.commit()
    db.refresh(patient)
    return patient


def ensure_patient_is_active(patient: Patient) -> None:
    if patient.status != ACTIVE_STATUS:
        raise PatientLifecycleError("Patient is not active")


def _get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise PatientNotFoundError("Patient not found")
    return patient


def _ensure_not_deleted(patient: Patient) -> None:
    if patient.status == DELETED_STATUS:
        raise PatientDeletedError("Deleted patient cannot be changed except restore")


def _ensure_restore_allowed(patient: Patient, current_user: CurrentUserContext) -> None:
    if patient.status == DELETED_STATUS:
        if current_user.role in {"admin", "technical_admin"} or "patients:delete" in current_user.permissions:
            return
        raise PatientRestorePermissionError("Deleted patient restore requires elevated permission")
    if current_user.role == "doctor" and patient.status != ARCHIVED_STATUS:
        raise PatientRestorePermissionError("Doctor can restore archived patients only")


def _write_audit_log(
    db: Session,
    patient: Patient,
    current_user: CurrentUserContext,
    action: str,
    old_status: str | None,
    reason: str | None,
) -> None:
    db.add(
        AuditLog(
            user_id=current_user.id,
            action=action,
            entity_type="patient",
            entity_id=str(patient.id),
            old_value=old_status,
            new_value=json.dumps(
                {
                    "patient_id": patient.id,
                    "patient_code": patient.patient_code,
                    "actor_user_id": current_user.id,
                    "reason": reason,
                },
                ensure_ascii=False,
            ),
        )
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)
