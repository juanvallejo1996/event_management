
from uuid import UUID

from src.domain.sessions.session import Session
from src.domain.sessions.ports.session_repository import SessionRepository
from src.domain.events.ports.event_repository import EventRepository
from src.application.sessions.dto.update_session_dto import UpdateSessionDTO
from src.domain.sessions.value_objects.speaker import Speaker
from src.domain.events.event_exceptions import EventNotFound
from src.domain.sessions.session_exceptions import SessionNotFound, InvalidSessionCapacity


class UpdateSessionUseCase:
    
    def __init__(
        self,
        repository: SessionRepository,
        event_repository: EventRepository
    ):
        self.repository = repository
        self.event_repository = event_repository

    async def execute(
        self,
        session_id: UUID,
        data: UpdateSessionDTO
    ) -> Session:

        session = await self.repository.get_by_id(session_id)
        if not session:
            raise SessionNotFound("Session not found")
        
        event_id = data.event_id if data.event_id is not None else session.event_id
        
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFound("Event not found")
        
        if session.capacity != data.capacity:
            total_capacity = await self.repository.get_total_capacity_by_event_id(event_id)
            total_capacity -= session.capacity
            if not event.can_add_session(data.capacity, total_capacity):
                raise InvalidSessionCapacity("Session capacity exceeds event capacity")

        session.event_id = event_id
        if data.title is not None:
            session.title = data.title
        if data.description is not None:
            session.description = data.description
            
        if data.speaker_name is not None or data.speaker_bio is not None:
            speaker = Speaker(name=data.speaker_name, bio=data.speaker_bio)
            session.speaker = speaker
            
        if data.capacity is not None:
            session.capacity = data.capacity
        if data.starts_at is not None:
            session.starts_at = data.starts_at
        if data.ends_at is not None:
            session.ends_at = data.ends_at

        return await self.repository.save(session)