from src.domain.users.user import User
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user_exceptions import UserNotFound


class SearchUserUseCase:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def execute(
        self,
        query: str
    ) -> User:

        user = await self.repository.get_by_email(query)

        if not user:
            raise UserNotFound()

        return user
