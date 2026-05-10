from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.events.event import Event


class EventRepository(ABC):

    @abstractmethod
    async def save(self, event: Event) -> Event:
        pass

    @abstractmethod
    async def get_by_id(self, event_id: UUID) -> Event | None:
        pass

    @abstractmethod
    async def search_by_name(self, query: str) -> list[Event]:
        pass

    @abstractmethod
    async def delete(self, event_id: UUID) -> None:
        pass