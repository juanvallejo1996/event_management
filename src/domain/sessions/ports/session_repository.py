
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.sessions.session import Session


class SessionRepository(ABC):

    @abstractmethod
    async def save(self, session: Session) -> Session:
        pass

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Session | None:
        pass

    @abstractmethod
    async def get_by_title(self, query: str) -> list[Session]:
        pass

    @abstractmethod
    async def get_by_event_id(self, event_id: UUID) -> list[Session]:
        pass

    @abstractmethod
    async def delete(self, session_id: UUID) -> None:
        pass
    
    @abstractmethod
    async def get_total_capacity_by_event_id(self, event_id: UUID) -> int:
        pass


