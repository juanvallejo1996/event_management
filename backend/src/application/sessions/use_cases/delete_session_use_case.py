
from uuid import UUID

from src.domain.sessions.ports.session_repository import SessionRepository
from src.domain.sessions.session_exceptions import SessionNotFound

class DeleteSessionUseCase:
    
    def __init__(
        self,
        repository: SessionRepository
    ):
        self.repository = repository

    async def execute(
        self,
        session_id: UUID
    ) -> None:
        
        session = await self.repository.get_by_id(session_id)
        if not session:
            raise SessionNotFound("Session not found")
        
        await self.repository.delete(session_id)