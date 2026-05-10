
from uuid import UUID

from src.domain.sessions.session import Session
from src.domain.sessions.ports.session_repository import SessionRepository

from src.domain.sessions.session_exceptions import SessionNotFound


class GetSessionByEventUseCase:
    
    def __init__(
        self,
        repository: SessionRepository
    ):
        self.repository = repository

    async def execute(
        self,
        event_id: UUID
    ) -> list[Session]:

        sessions = await self.repository.get_by_event_id(event_id)
        if not sessions:
            raise SessionNotFound("No sessions found for this event")

        return sessions