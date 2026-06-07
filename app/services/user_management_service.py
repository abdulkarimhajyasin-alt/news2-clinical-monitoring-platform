from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import AuditLog, User
from app.rbac import ROLE_PERMISSIONS
from app.schemas import StaffUserCreate, StaffUserUpdate
from app.security.passwords import hash_password


class StaffUserNotFoundError(ValueError):
    pass


class StaffUserDuplicateError(ValueError):
    pass


class StaffUserInvalidRoleError(ValueError):
    pass


def list_staff_users(
    db: Session,
    *,
    role: str | None = None,
    is_active: bool | None = None,
    department: str | None = None,
    search: str | None = None,
) -> list[User]:
    query = db.query(User).order_by(User.created_at.desc(), User.id.desc())
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if department:
        query = query.filter(User.department == department)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(or_(User.full_name.ilike(pattern), User.username.ilike(pattern), User.email.ilike(pattern)))
    return query.all()


def get_staff_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise StaffUserNotFoundError("staff user not found")
    return user


def create_staff_user(db: Session, payload: StaffUserCreate) -> User:
    _validate_role(payload.role)
    username = payload.username.strip()
    email = str(payload.email or f"{username}@staff.local").strip().lower()
    _ensure_unique_identity(db, username=username, email=email)
    user = User(
        full_name=payload.full_name.strip(),
        username=username,
        email=email,
        phone=payload.phone,
        department=payload.department,
        job_title=payload.job_title,
        role=payload.role,
        is_active=payload.is_active,
        status="active" if payload.is_active else "inactive",
        password_hash=hash_password(payload.temporary_password),
        preferred_language="ar",
    )
    db.add(user)
    db.flush()
    _audit(db, "staff_user_created", user)
    db.commit()
    db.refresh(user)
    return user


def update_staff_user(db: Session, user_id: int, payload: StaffUserUpdate) -> User:
    user = get_staff_user(db, user_id)
    if payload.role is not None:
        _validate_role(payload.role)
    if payload.email is not None:
        email = str(payload.email).strip().lower()
        _ensure_unique_identity(db, email=email, exclude_user_id=user.id)
        user.email = email
    for field in ("full_name", "phone", "department", "job_title", "role"):
        value = getattr(payload, field)
        if value is not None:
            setattr(user, field, value)
    if payload.is_active is not None:
        user.is_active = payload.is_active
        user.status = "active" if payload.is_active else "inactive"
    _audit(db, "staff_user_updated", user)
    db.commit()
    db.refresh(user)
    return user


def set_staff_user_active_status(db: Session, user_id: int, is_active: bool) -> User:
    user = get_staff_user(db, user_id)
    user.is_active = is_active
    user.status = "active" if is_active else "inactive"
    _audit(db, "staff_user_status_changed", user, new_value=user.status)
    db.commit()
    db.refresh(user)
    return user


def _validate_role(role: str) -> None:
    if role not in ROLE_PERMISSIONS:
        raise StaffUserInvalidRoleError("invalid role")


def _ensure_unique_identity(db: Session, *, username: str | None = None, email: str | None = None, exclude_user_id: int | None = None) -> None:
    query = db.query(User)
    filters = []
    if username:
        filters.append(User.username == username)
    if email:
        filters.append(User.email == email)
    if not filters:
        return
    query = query.filter(or_(*filters))
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)
    if query.first():
        raise StaffUserDuplicateError("username or email already exists")


def _audit(db: Session, action: str, user: User, new_value: str | None = None) -> None:
    db.add(
        AuditLog(
            action=action,
            entity_type="user",
            entity_id=str(user.id),
            new_value=new_value or f"{user.username or user.email}:{user.role}",
        )
    )
