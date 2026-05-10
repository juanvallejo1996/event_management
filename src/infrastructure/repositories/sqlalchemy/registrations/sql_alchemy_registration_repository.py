from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.registrations.ports.registration_repository import RegistrationRepository
from src.domain.registrations.registration import Registration
from src.domain.registrations.registration_status import RegistrationStatus
from src.infrastructure.repositories.sqlalchemy.registrations.registration_model import RegisterModel


class SQLAlchemyRegistrationRepository(RegistrationRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, registration: Registration) -> Registration:
        model = self._to_model(registration)
        merged = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(merged)
        return registration

    async def find_by_user_and_event(self, user_id: UUID, event_id: UUID) -> Registration | None:
        statement = select(RegisterModel).where(
            RegisterModel.user_id == user_id,
            RegisterModel.event_id == event_id,
        )
        result = await self.session.execute(statement)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def count_by_event(self, event_id: UUID) -> int:
        statement = select(func.count(RegisterModel.id)).where(
            RegisterModel.event_id == event_id,
            RegisterModel.status == RegistrationStatus.CONFIRMED.value,
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_by_user(self, user_id: UUID) -> list[Registration]:
        statement = select(RegisterModel).where(RegisterModel.user_id == user_id)
        result = await self.session.execute(statement)
        return [self._to_domain(model) for model in result.scalars().all()]

    def _to_model(self, registration: Registration) -> RegisterModel:
        return RegisterModel(
            id=registration.id,
            user_id=registration.user_id,
            event_id=registration.event_id,
            registered_at=registration.registered_at.replace(tzinfo=None),
            status=registration.status.value,
        )

    def _to_domain(self, model: RegisterModel) -> Registration:
        return Registration(
            id=model.id,
            user_id=model.user_id,
            event_id=model.event_id,
            registered_at=model.registered_at,
            status=RegistrationStatus(model.status),
        )
