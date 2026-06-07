from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets

from fastapi import HTTPException, Request, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import AuditLog, AuthSession, User
from app.security.passwords import verify_password


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    full_name: str
    username: str | None
    email: str | None
    role: str
    is_dev_context: bool = False


def authenticate_user(db: Session, identifier: str, password: str, request: Request | None = None) -> User:
    normalized_identifier = identifier.strip().lower()
    user = (
        db.query(User)
        .filter(or_(User.username == normalized_identifier, User.email == normalized_identifier))
        .first()
    )
    if user is None or not verify_password(password, user.password_hash):
        _write_audit_log(db, "auth_login_failed", None, "auth", normalized_identifier, request=request)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.is_active or user.status != "active":
        _write_audit_log(db, "auth_login_failed", user.id, "auth", "inactive_user", request=request)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")

    user.last_login_at = datetime.now(timezone.utc)
    _write_audit_log(db, "auth_login_success", user.id, "auth", user.username or user.email, request=request, commit=False)
    db.commit()
    db.refresh(user)
    return user


def create_auth_session(db: Session, user: User) -> tuple[str, AuthSession]:
    settings = get_settings()
    token = secrets.token_urlsafe(48)
    now = datetime.now(timezone.utc)
    session = AuthSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=now + timedelta(seconds=settings.session_max_age_seconds),
        last_seen_at=now,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return token, session


def get_user_for_session_token(db: Session, token: str) -> User | None:
    session = db.query(AuthSession).filter(AuthSession.token_hash == hash_session_token(token)).first()
    if session is None:
        return None
    now = datetime.now(timezone.utc)
    expires_at = _as_aware_utc(session.expires_at)
    if expires_at <= now:
        db.delete(session)
        db.commit()
        return None
    user = session.user
    if user is None or not user.is_active or user.status != "active":
        db.delete(session)
        db.commit()
        return None
    session.last_seen_at = now
    db.commit()
    db.refresh(user)
    return user


def get_current_user_from_request(db: Session, request: Request) -> User:
    token = request.cookies.get(get_settings().session_cookie_name)
    if not token:
        _write_audit_log(db, "auth_unauthorized_access", None, "auth", request.url.path, request=request)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user = get_user_for_session_token(db, token)
    if user is None:
        _write_audit_log(db, "auth_unauthorized_access", None, "auth", request.url.path, request=request)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


def logout_current_session(db: Session, request: Request) -> None:
    token = request.cookies.get(get_settings().session_cookie_name)
    if not token:
        return
    session = db.query(AuthSession).filter(AuthSession.token_hash == hash_session_token(token)).first()
    if session is None:
        return
    user_id = session.user_id
    db.delete(session)
    _write_audit_log(db, "auth_logout", user_id, "auth", "session", request=request, commit=False)
    db.commit()


def hash_session_token(token: str) -> str:
    secret = get_settings().resolved_session_secret().encode("utf-8")
    return hmac.new(secret, token.encode("utf-8"), hashlib.sha256).hexdigest()


def _write_audit_log(
    db: Session,
    action: str,
    user_id: int | None,
    entity_type: str,
    entity_id: str | None,
    *,
    request: Request | None = None,
    commit: bool = True,
) -> None:
    try:
        db.add(
            AuditLog(
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                ip_address=request.client.host if request and request.client else None,
                user_agent=request.headers.get("user-agent") if request else None,
            )
        )
        if commit:
            db.commit()
    except Exception:
        db.rollback()


def _as_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
