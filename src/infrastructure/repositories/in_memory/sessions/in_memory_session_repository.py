
from uuid import UUID

from src.domain.sessions.session import Session
from src.domain.sessions.ports.session_repository import SessionRepository


class InMemorySessionRepository(SessionRepository):
    
    def __init__(self):
        self.sessions: dict[UUID, Session] = {}

    async def save(self, session: Session) -> Session:
        self.sessions[session.id] = session
        return session

    async def get_by_id(self, session_id: UUID) -> Session | None:
        return self.sessions.get(session_id)

    async def get_by_title(self, query: str) -> list[Session]:
        query = query.lower()

        return [
            session
            for session in self.sessions.values()
            if query in session.title.lower()
        ]

    async def get_by_event_id(self, event_id: UUID) -> list[Session]:
        return [
            session
            for session in self.sessions.values()
            if session.event_id == event_id
        ]

    async def delete(self, session_id: UUID) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]

    async def get_total_capacity_by_event_id(self, event_id: UUID) -> int:
        return sum(
            session.capacity
            for session in self.sessions.values()
            if session.event_id == event_id
        )