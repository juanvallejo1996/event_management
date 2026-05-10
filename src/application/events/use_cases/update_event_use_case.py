from datetime import datetime, timezone
from uuid import UUID

from src.domain.events.ports.event_repository import EventRepository
from src.domain.events.event_exceptions import EventNotFound
from src.domain.events.value_objects.event_capacity import EventCapacity

from src.application.events.dto.update_event_dto import UpdateEventDTO


class UpdateEventUseCase:

    def __init__(
        self,
        repository: EventRepository
    ):
        self.repository = repository

    async def execute(
        self,
        event_id: UUID,
        data: UpdateEventDTO
    ):

        event = await self.repository.get_by_id(
            event_id
        )

        if not event:
            raise EventNotFound()

        if data.name is not None:
            event.name = data.name

        if data.description is not None:
            event.description = data.description

        if data.capacity is not None:
            capacity = EventCapacity(data.capacity)

            event.capacity = capacity.value

        if data.starts_at is not None:
            event.starts_at = data.starts_at

        if data.ends_at is not None:
            event.ends_at = data.ends_at

        if data.status is not None:
            event.status = data.status

        event.updated_at = datetime.now(timezone.utc)

        return await self.repository.save(event)
