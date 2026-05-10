from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.events.ports.event_repository import EventRepository
from src.domain.events.event import Event
from src.domain.events.event_status import EventStatus
from src.infrastructure.repositories.sqlalchemy.events.event_model import EventModel


class SQLAlchemyEventRepository(EventRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, event: Event) -> Event:
        model = self._to_model(event)
        merged = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(merged)
        return event

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.get(EventModel, event_id)
        return self._to_domain(result) if result else None

    async def search_by_name(self, query: str) -> list[Event]:
        statement = select(EventModel).where(EventModel.name.ilike(f"%{query}%"))
        result = await self.session.execute(statement)
        return [self._to_domain(model) for model in result.scalars().all()]

    async def delete(self, event_id: UUID) -> None:
        model = await self.session.get(EventModel, event_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_model(self, event: Event) -> EventModel:
        return EventModel(
            id=event.id,
            name=event.name,
            description=event.description,
            capacity=event.capacity,
            status=event.status.value,
            starts_at=event.starts_at.replace(tzinfo=None),
            ends_at=event.ends_at.replace(tzinfo=None),
            created_at=event.created_at.replace(tzinfo=None),
            updated_at=event.updated_at.replace(tzinfo=None),
        )

    def _to_domain(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            name=model.name,
            description=model.description,
            capacity=model.capacity,
            status=EventStatus(model.status),
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
