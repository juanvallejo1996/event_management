from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.sessions.ports.session_repository import SessionRepository
from src.domain.sessions.session import Session
from src.domain.sessions.session_status import SessionStatus
from src.domain.sessions.value_objects.speaker import Speaker
from src.infrastructure.repositories.sqlalchemy.sessions.session_model import SessionModel


class SQLAlchemySessionRepository(SessionRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, session: Session) -> Session:
        model = self._to_model(session)
        merged = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(merged)
        return session

    async def get_by_id(self, session_id: UUID) -> Session | None:
        result = await self.session.get(SessionModel, session_id)
        return self._to_domain(result) if result else None

    async def get_by_title(self, query: str) -> list[Session]:
        statement = select(SessionModel).where(SessionModel.title.ilike(f"%{query}%"))
        result = await self.session.execute(statement)
        return [self._to_domain(model) for model in result.scalars().all()]

    async def get_by_event_id(self, event_id: UUID) -> list[Session]:
        statement = select(SessionModel).where(SessionModel.event_id == event_id)
        result = await self.session.execute(statement)
        return [self._to_domain(model) for model in result.scalars().all()]

    async def delete(self, session_id: UUID) -> None:
        model = await self.session.get(SessionModel, session_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()

    async def get_total_capacity_by_event_id(self, event_id: UUID) -> int:
        statement = select(func.sum(SessionModel.capacity)).where(
            SessionModel.event_id == event_id
        )
        result = await self.session.execute(statement)
        total = result.scalar_one_or_none()
        return total or 0

    def _to_model(self, session: Session) -> SessionModel:
        return SessionModel(
            id=session.id,
            event_id=session.event_id,
            title=session.title,
            description=session.description,
            capacity=session.capacity,
            speaker_name=session.speaker.name,
            speaker_bio=session.speaker.bio,
            status=session.status.value,
            starts_at=session.starts_at.replace(tzinfo=None),
            ends_at=session.ends_at.replace(tzinfo=None),
            created_at=session.created_at.replace(tzinfo=None),
            updated_at=session.updated_at.replace(tzinfo=None),
        )

    def _to_domain(self, model: SessionModel) -> Session:
        return Session(
            id=model.id,
            event_id=model.event_id,
            title=model.title,
            description=model.description,
            capacity=model.capacity,
            speaker=Speaker(name=model.speaker_name, bio=model.speaker_bio),
            status=SessionStatus(model.status),
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
