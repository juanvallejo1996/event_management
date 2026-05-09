
from abc import ABC, abstractmethod
from uuid import UUID


class TokenService(ABC):
    
    @abstractmethod
    async def generate_token(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> UUID | None:
        pass