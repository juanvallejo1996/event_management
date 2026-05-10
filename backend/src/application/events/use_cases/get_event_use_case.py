
from uuid import UUID

from src.domain.events.event import Event
from src.domain.events.ports.event_repository import EventRepository
from src.domain.events.event_exceptions import EventNotFound

class GetEventUseCase:

    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def execute(self, event_id: UUID) -> Event:

        event = await self.repository.get_by_id(
            event_id
        )

        if not event:
            raise EventNotFound()

        return event