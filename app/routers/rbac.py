from fastapi import APIRouter, Depends

from app.rbac import DevUser, get_current_dev_user, permission_matrix, require_permission

router = APIRouter(prefix="/api/rbac", tags=["rbac"])


@router.get("/me")
def read_current_permission_context(current_user: DevUser = Depends(get_current_dev_user)):
    return {
        "role": current_user.role,
        "role_label": current_user.role_label,
        "permissions": current_user.permissions,
        "is_dev_context": current_user.is_dev_context,
    }


@router.get("/permissions")
def read_permission_matrix(_current_user=Depends(require_permission("rbac:view"))):
    return permission_matrix()
