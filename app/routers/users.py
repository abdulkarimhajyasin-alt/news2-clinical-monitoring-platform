from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.rbac import require_permission
from app.schemas import StaffUserCreate, StaffUserCreateResult, StaffUserRead, StaffUserStatusUpdate, StaffUserUpdate
from app.services.user_management_service import (
    StaffUserDuplicateError,
    StaffUserInvalidRoleError,
    StaffUserNotFoundError,
    create_staff_user,
    get_staff_user,
    list_staff_users,
    set_staff_user_active_status,
    update_staff_user,
)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[StaffUserRead])
def read_staff_users(
    role: str | None = None,
    is_active: bool | None = Query(default=None),
    department: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("users:view")),
):
    return list_staff_users(db, role=role, is_active=is_active, department=department, search=search)


@router.post("", response_model=StaffUserCreateResult, status_code=status.HTTP_201_CREATED)
def create_staff_user_record(
    payload: StaffUserCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("users:create")),
):
    try:
        user = create_staff_user(db, payload)
    except StaffUserDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except StaffUserInvalidRoleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"user": user, "user_created": True, "message": "staff_user_created"}


@router.get("/{user_id}", response_model=StaffUserRead)
def read_staff_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("users:view")),
):
    try:
        return get_staff_user(db, user_id)
    except StaffUserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{user_id}", response_model=StaffUserRead)
def update_staff_user_record(
    user_id: int,
    payload: StaffUserUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("users:update")),
):
    try:
        return update_staff_user(db, user_id, payload)
    except StaffUserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except StaffUserDuplicateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except StaffUserInvalidRoleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{user_id}/status", response_model=StaffUserRead)
def update_staff_user_status(
    user_id: int,
    payload: StaffUserStatusUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_permission("users:disable")),
):
    try:
        return set_staff_user_active_status(db, user_id, payload.is_active)
    except StaffUserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
