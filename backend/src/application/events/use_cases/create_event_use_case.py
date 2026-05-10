from uuid import uuid4
from datetime import datetime, timezone

from src.domain.events.event import Event
from src.domain.events.event_status import EventStatus
from src.domain.events.ports.event_repository import EventRepository
from src.domain.events.value_objects.event_capacity import EventCapacity

from src.application.events.dto.create_event_dto import CreateEventDTO


class CreateEventUseCase:

    def __init__(
        self,
        repository: EventRepository
    ):
        self.repository = repository

    async def execute(
        self,
        data: CreateEventDTO
    ) -> Event:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        starts_at = data.starts_at.replace(tzinfo=None)
        ends_at = data.ends_at.replace(tzinfo=None)
        Event.validate_dates(starts_at, ends_at, now)

        capacity = EventCapacity(data.capacity)

        event = Event(
            id=uuid4(),
            name=data.name,
            description=data.description,
            capacity=capacity.value,
            status=EventStatus.DRAFT,
            starts_at=starts_at,
            ends_at=ends_at,
            created_at=now,
            updated_at=now,
        )

        return await self.repository.save(event)