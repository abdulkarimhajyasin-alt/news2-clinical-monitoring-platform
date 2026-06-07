from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog


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
        "sessions:view",
        "alerts:view",
        "research:view",
    },
    ROLE_DOCTOR: {
        "patients:view",
        "patients:create",
        "patients:update",
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
class DevUser:
    role: str
    role_label: str
    permissions: list[str]
    is_dev_context: bool = True


def get_current_dev_user(x_dev_role: str | None = Header(default=None, alias="X-Dev-Role")) -> DevUser:
    role = (x_dev_role or ROLE_ADMIN).strip()
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid development role")
    return DevUser(
        role=role,
        role_label=ROLE_LABELS[role],
        permissions=sorted(ROLE_PERMISSIONS[role]),
    )


def role_has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())


def require_permission(permission: str):
    def dependency(
        request: Request,
        current_user: DevUser = Depends(get_current_dev_user),
        db: Session = Depends(get_db),
    ) -> DevUser:
        if role_has_permission(current_user.role, permission):
            return current_user
        _audit_permission_denial(db, current_user.role, permission, request.url.path)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return dependency


def require_any_permission(permissions: Iterable[str]):
    permission_list = list(permissions)

    def dependency(
        request: Request,
        current_user: DevUser = Depends(get_current_dev_user),
        db: Session = Depends(get_db),
    ) -> DevUser:
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
        "is_dev_context": True,
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
