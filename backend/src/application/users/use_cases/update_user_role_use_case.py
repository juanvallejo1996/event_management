from uuid import UUID

from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user_exceptions import UserNotFound


class UpdateUserRoleUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID, new_role: UserRole) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFound("User not found")

        user.role = new_role
        return await self.repository.save(user)
