"""Notes on RBAC in this codebase.

The primary RBAC enforcement point is `app.core.deps.require_roles`, used as
a FastAPI dependency on individual routes (see app/api/v1/routers/*.py).
This module exists for cross-cutting policy helpers that don't map to a
single dependency, e.g. resource-ownership checks."""
from app.core.exceptions import ForbiddenError
from app.domain.entities.user import UserRole


def assert_owner_or_role(resource_owner_id: str, current_user_id: str, current_role: UserRole, *allowed_roles: UserRole) -> None:
    """Allow if the current user owns the resource, or holds one of the
    allowed elevated roles (e.g. ADMIN can act on anyone's resources)."""
    if resource_owner_id == current_user_id:
        return
    if current_role in allowed_roles:
        return
    raise ForbiddenError("You do not have permission to access this resource")
