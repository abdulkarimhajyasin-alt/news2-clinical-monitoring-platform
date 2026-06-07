from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.rbac import CurrentUserContext, get_current_user
from app.schemas import AuthenticatedUserRead, AuthLoginRequest
from app.services.auth_service import authenticate_user, create_auth_session, logout_current_session

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=AuthenticatedUserRead)
def login(payload: AuthLoginRequest, response: Response, request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username_or_email, payload.password, request)
    token, _session = create_auth_session(db, user)
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_max_age_seconds,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
    )
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "role_label": current_role_label(user.role),
        "permissions": current_role_permissions(user.role),
        "is_dev_context": False,
        "allow_dev_role": settings.allow_dev_role,
    }


@router.get("/me", response_model=AuthenticatedUserRead)
def read_current_user(current_user: CurrentUserContext = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    logout_current_session(db, request)
    response.delete_cookie(key=settings.session_cookie_name, httponly=True, secure=settings.cookie_secure, samesite="lax")
    return {"message": "logged_out"}


def current_role_label(role: str) -> str:
    from app.rbac import ROLE_LABELS

    return ROLE_LABELS[str(role)]


def current_role_permissions(role: str) -> list[str]:
    from app.rbac import ROLE_PERMISSIONS

    return sorted(ROLE_PERMISSIONS[str(role)])
