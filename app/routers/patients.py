from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import CurrentUserContext, require_permission
from app.schemas import PatientArchiveRequest, PatientCreate, PatientCreateResult, PatientDeleteRequest, PatientDischargeRequest, PatientLifecycleResult, PatientRead, PatientUpdate
from app.services.patient_lifecycle_service import (
    PatientDeleteConfirmationError,
    PatientDeletedError,
    PatientNotFoundError,
    PatientRestorePermissionError,
    archive_patient,
    discharge_patient,
    restore_patient,
    soft_delete_patient,
)
from app.services.patient_service import PatientCodeExistsError, create_patient, list_patients, update_patient

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
def read_patients(
    patient_status: str | None = Query(default=None, alias="status", pattern="^(active|discharged|archived|deleted)$"),
    include_archived: bool = False,
    include_deleted: bool = False,
    db: Session = Depends(get_db),
    current_user: CurrentUserContext = Depends(require_permission("patients:view")),
):
    can_view_deleted = "patients:delete" in current_user.permissions
    if (patient_status == "deleted" or include_deleted) and not can_view_deleted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return list_patients(
        db,
        status=patient_status,
        include_archived=include_archived,
        include_deleted=include_deleted and can_view_deleted,
    )


@router.post("", response_model=PatientCreateResult, status_code=status.HTTP_201_CREATED)
def create_patient_record(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("patients:create")),
):
    try:
        patient = create_patient(db, payload)
    except PatientCodeExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"patient": patient, "patient_created": True, "message": "patient_created"}


@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient_record(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("patients:update")),
):
    patient = update_patient(db, patient_id, payload)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.post("/{patient_id}/discharge", response_model=PatientLifecycleResult)
def discharge_patient_record(
    patient_id: int,
    payload: PatientDischargeRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserContext = Depends(require_permission("patients:discharge")),
):
    try:
        patient = discharge_patient(db, patient_id, payload, current_user)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PatientDeletedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"patient": patient, "message": "patient_discharged"}


@router.post("/{patient_id}/archive", response_model=PatientLifecycleResult)
def archive_patient_record(
    patient_id: int,
    payload: PatientArchiveRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserContext = Depends(require_permission("patients:archive")),
):
    try:
        patient = archive_patient(db, patient_id, payload, current_user)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PatientDeletedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"patient": patient, "message": "patient_archived"}


@router.post("/{patient_id}/restore", response_model=PatientLifecycleResult)
def restore_patient_record(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUserContext = Depends(require_permission("patients:restore")),
):
    try:
        patient = restore_patient(db, patient_id, current_user)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PatientRestorePermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return {"patient": patient, "message": "patient_restored"}


@router.post("/{patient_id}/delete", response_model=PatientLifecycleResult)
def soft_delete_patient_record(
    patient_id: int,
    payload: PatientDeleteRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserContext = Depends(require_permission("patients:delete")),
):
    try:
        patient = soft_delete_patient(db, patient_id, payload, current_user)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PatientDeleteConfirmationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"patient": patient, "message": "patient_soft_deleted"}
