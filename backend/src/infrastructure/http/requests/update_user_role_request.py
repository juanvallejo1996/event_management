from pydantic import BaseModel

from src.domain.users.user_role import UserRole


class UpdateUserRoleRequest(BaseModel):
    role: UserRole
