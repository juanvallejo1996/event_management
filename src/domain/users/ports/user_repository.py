from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.users.user import User


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        pass
