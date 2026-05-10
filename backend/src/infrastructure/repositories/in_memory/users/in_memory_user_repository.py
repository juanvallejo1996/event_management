
from uuid import UUID

from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user import User


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users: dict[UUID, User] = {}

    async def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email.value == email:
                return user
        return None
