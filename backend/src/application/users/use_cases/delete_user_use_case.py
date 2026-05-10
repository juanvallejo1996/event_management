from uuid import UUID

from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user_exceptions import UserNotFound


class DeleteUserUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFound("User not found")

        await self.repository.delete(user_id)
