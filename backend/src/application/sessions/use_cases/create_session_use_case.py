
from uuid import uuid4
from datetime import datetime, timezone

from src.domain.sessions.session import Session
from src.domain.sessions.value_objects.speaker import Speaker
from src.domain.sessions.ports.session_repository import SessionRepository
from src.domain.events.ports.event_repository import EventRepository
from src.application.sessions.dto.create_session_dto import CreateSessionDTO
from src.domain.sessions.session_status import SessionStatus

from src.domain.events.event_exceptions import EventNotFound
from src.domain.sessions.session_exceptions import InvalidSessionCapacity, InvalidSessionDates

class CreateSessionUseCase:
    
    def __init__(
        self,
        repository: SessionRepository,
        event_repository: EventRepository
    ):
        self.repository = repository
        self.event_repository = event_repository

    async def execute(
        self,
        data: CreateSessionDTO
    ) -> Session:

        event = await self.event_repository.get_by_id(data.event_id)
        if not event:
            raise EventNotFound("Event not found")

        starts_at = data.starts_at.replace(tzinfo=None)
        ends_at = data.ends_at.replace(tzinfo=None)

        if starts_at < event.starts_at:
            raise InvalidSessionDates("Session cannot start before the event starts")
        if ends_at > event.ends_at:
            raise InvalidSessionDates("Session cannot end after the event ends")
        if ends_at <= starts_at:
            raise InvalidSessionDates("Session end time must be after start time")

        total_capacity = await self.repository.get_total_capacity_by_event_id(data.event_id)
        if not event.can_add_session(data.capacity, total_capacity):
            raise InvalidSessionCapacity("Session capacity exceeds event capacity")
        
        speaker = Speaker(name=data.speaker_name, bio=data.speaker_bio)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        session = Session(
            id=uuid4(),
            event_id=data.event_id,
            title=data.title,
            description=data.description,
            capacity=data.capacity,
            speaker=speaker,
            status=SessionStatus.SCHEDULED,
            starts_at=starts_at,
            ends_at=ends_at,
            created_at=now,
            updated_at=now,
        )

        return await self.repository.save(session)