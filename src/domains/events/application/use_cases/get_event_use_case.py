
from uuid import UUID

from src.domains.events.domain.entities.event import Event
from src.domains.events.domain.repositories.event_repository import EventRepository
from src.domains.events.domain.exceptions.event_exceptions import EventNotFound


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