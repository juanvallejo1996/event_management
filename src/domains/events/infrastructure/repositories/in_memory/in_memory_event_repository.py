from uuid import UUID

from src.domains.events.domain.entities.event import Event
from src.domains.events.domain.repositories.event_repository import EventRepository


class InMemoryEventRepository(EventRepository):

    def __init__(self):
        self.events: dict[UUID, Event] = {}

    async def save(self, event: Event
    ) -> Event:

        self.events[event.id] = event

        return event

    async def get_by_id(self, event_id: UUID) -> Event | None:

        return self.events.get(event_id)

    async def search_by_name(self, query: str) -> list[Event]:

        query = query.lower()

        return [
            event
            for event in self.events.values()
            if query in event.name.lower()
        ]

    async def delete(self, event_id: UUID) -> None:

        if event_id in self.events:
            del self.events[event_id]