from uuid import uuid4
from datetime import datetime

from src.domains.events.domain.entities.event import Event
from src.domains.events.domain.enums.event_status import EventStatus
from src.domains.events.domain.repositories.event_repository import EventRepository
from src.domains.events.domain.value_objects.event_capacity import EventCapacity

from src.domains.events.application.dto.create_event_dto import CreateEventDTO


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

        capacity = EventCapacity(data.capacity)

        event = Event(
            id=uuid4(),
            name=data.name,
            description=data.description,
            capacity=capacity.value,
            status=EventStatus.DRAFT,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        return await self.repository.save(event)