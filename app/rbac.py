from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import AuditLog, User
from app.services.auth_service import get_current_user_from_request


ROLE_ADMIN = "admin"
ROLE_TECHNICAL_ADMIN = "technical_admin"
ROLE_DOCTOR = "doctor"
ROLE_ON_CALL_DOCTOR = "on_call_doctor"
ROLE_NURSE = "nurse"
ROLE_RESEARCHER = "researcher"

ROLE_LABELS = {
    ROLE_ADMIN: "مدير النظام",
    ROLE_TECHNICAL_ADMIN: "تقني النظام",
    ROLE_DOCTOR: "طبيب",
    ROLE_ON_CALL_DOCTOR: "طبيب مناوب",
    ROLE_NURSE: "ممرض/ممرضة",
    ROLE_RESEARCHER: "باحث",
}

PERMISSIONS = {
    "patients:view",
    "patients:create",
    "patients:update",
    "patients:discharge",
    "patients:archive",
    "patients:restore",
    "patients:delete",
    "sessions:view",
    "sessions:create",
    "sessions:update",
    "measurements:view",
    "measurements:create",
    "news2:view",
    "alerts:view",
    "alerts:manage",
    "deterioration:view",
    "deterioration:create",
    "responses:view",
    "responses:create",
    "outcomes:view",
    "outcomes:create",
    "research:view",
    "research:analytics",
    "research:export",
    "studies:view",
    "studies:create",
    "studies:update",
    "users:view",
    "users:create",
    "users:update",
    "users:disable",
    "users:manage",
    "rbac:view",
    "rbac:manage",
    "staff:view",
    "staff:create",
    "staff:update",
    "audit:view",
    "settings:view",
    "settings:manage",
}

ROLE_PERMISSIONS = {
    ROLE_ADMIN: set(PERMISSIONS),
    ROLE_TECHNICAL_ADMIN: {
        "users:view",
        "users:create",
        "users:update",
        "users:disable",
        "users:manage",
        "rbac:view",
        "rbac:manage",
        "staff:view",
        "staff:create",
        "staff:update",
        "audit:view",
        "settings:view",
        "settings:manage",
        "patients:view",
        "patients:archive",
        "patients:restore",
        "sessions:view",
        "alerts:view",
        "research:view",
    },
    ROLE_DOCTOR: {
        "patients:view",
        "patients:create",
        "patients:update",
        "patients:discharge",
        "patients:restore",
        "sessions:view",
        "sessions:create",
        "sessions:update",
        "measurements:view",
        "measurements:create",
        "news2:view",
        "alerts:view",
        "alerts:manage",
        "deterioration:view",
        "deterioration:create",
        "responses:view",
        "responses:create",
        "outcomes:view",
        "outcomes:create",
        "research:view",
        "research:analytics",
        "studies:view",
    },
    ROLE_ON_CALL_DOCTOR: {
        "patients:view",
        "sessions:view",
        "measurements:view",
        "measurements:create",
        "news2:view",
        "alerts:view",
        "alerts:manage",
        "deterioration:view",
        "deterioration:create",
        "responses:view",
        "responses:create",
        "outcomes:view",
        "outcomes:create",
        "research:view",
    },
    ROLE_NURSE: {
        "patients:view",
        "sessions:view",
        "measurements:view",
        "measurements:create",
        "news2:view",
        "alerts:view",
        "deterioration:view",
        "responses:view",
        "responses:create",
        "outcomes:view",
    },
    ROLE_RESEARCHER: {
        "patients:view",
        "sessions:view",
        "measurements:view",
        "news2:view",
        "alerts:view",
        "deterioration:view",
        "responses:view",
        "outcomes:view",
        "research:view",
        "research:analytics",
        "research:export",
        "studies:view",
        "studies:create",
        "studies:update",
    },
}


@dataclass(frozen=True)
class CurrentUserContext:
    role: str
    role_label: str
    permissions: list[str]
    id: int | None = None
    full_name: str | None = None
    username: str | None = None
    email: str | None = None
    is_dev_context: bool = False
    allow_dev_role: bool = False


DevUser = CurrentUserContext


def get_current_dev_user(x_dev_role: str | None = Header(default=None, alias="X-Dev-Role")) -> CurrentUserContext:
    role = (x_dev_role or ROLE_ADMIN).strip()
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid development role")
    return CurrentUserContext(
        role=role,
        role_label=ROLE_LABELS[role],
        permissions=sorted(ROLE_PERMISSIONS[role]),
        full_name=ROLE_LABELS[role],
        username="dev",
        is_dev_context=True,
        allow_dev_role=True,
    )


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    x_dev_role: str | None = Header(default=None, alias="X-Dev-Role"),
) -> CurrentUserContext:
    settings = get_settings()
    if request.cookies.get(settings.session_cookie_name):
        return user_context_from_model(get_current_user_from_request(db, request), allow_dev_role=settings.allow_dev_role)
    if settings.allow_dev_role:
        return get_current_dev_user(x_dev_role)
    _audit_auth_unauthorized(db, request)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")


def user_context_from_model(user: User, *, allow_dev_role: bool = False) -> CurrentUserContext:
    role = str(user.role)
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user role")
    return CurrentUserContext(
        id=user.id,
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        role=role,
        role_label=ROLE_LABELS[role],
        permissions=sorted(ROLE_PERMISSIONS[role]),
        is_dev_context=False,
        allow_dev_role=allow_dev_role,
    )


def role_has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())


def require_permission(permission: str):
    def dependency(
        request: Request,
        current_user: CurrentUserContext = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> CurrentUserContext:
        if role_has_permission(current_user.role, permission):
            return current_user
        _audit_permission_denial(db, current_user.role, permission, request.url.path)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return dependency


def require_any_permission(permissions: Iterable[str]):
    permission_list = list(permissions)

    def dependency(
        request: Request,
        current_user: CurrentUserContext = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> CurrentUserContext:
        if any(role_has_permission(current_user.role, permission) for permission in permission_list):
            return current_user
        _audit_permission_denial(db, current_user.role, ",".join(permission_list), request.url.path)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return dependency


def permission_matrix() -> dict[str, object]:
    return {
        "roles": [
            {
                "role": role,
                "role_label": ROLE_LABELS[role],
                "permissions": sorted(permissions),
            }
            for role, permissions in ROLE_PERMISSIONS.items()
        ],
        "permissions": sorted(PERMISSIONS),
        "is_dev_context": False,
    }


def _audit_permission_denial(db: Session, role: str, permission: str, path: str) -> None:
    try:
        db.add(
            AuditLog(
                action="permission_denied",
                entity_type="rbac",
                entity_id=permission,
                old_value=role,
                new_value=path,
            )
        )
        db.commit()
    except Exception:
        db.rollback()


def _audit_auth_unauthorized(db: Session, request: Request) -> None:
    try:
        db.add(
            AuditLog(
                action="auth_unauthorized_access",
                entity_type="auth",
                entity_id=request.url.path,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
            )
        )
        db.commit()
    except Exception:
        db.rollback()
