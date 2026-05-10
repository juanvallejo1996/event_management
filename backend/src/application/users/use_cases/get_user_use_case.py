
from uuid import UUID

from src.domain.users.user import User
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user_exceptions import UserNotFound

class GetUserUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> User:

        user = await self.repository.get_by_id(
            user_id
        )

        if not user:
            raise UserNotFound()

        return user