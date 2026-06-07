from fastapi import APIRouter, Depends

from app.rbac import CurrentUserContext, get_current_user, permission_matrix, require_permission

router = APIRouter(prefix="/api/rbac", tags=["rbac"])


@router.get("/me")
def read_current_permission_context(current_user: CurrentUserContext = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "role_label": current_user.role_label,
        "permissions": current_user.permissions,
        "is_dev_context": current_user.is_dev_context,
        "allow_dev_role": current_user.allow_dev_role,
    }


@router.get("/permissions")
def read_permission_matrix(_current_user=Depends(require_permission("rbac:view"))):
    return permission_matrix()
