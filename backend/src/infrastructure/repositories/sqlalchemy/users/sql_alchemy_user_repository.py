from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.value_objects.email import Email
from src.domain.users.value_objects.hashed_password import HashedPassword
from src.infrastructure.repositories.sqlalchemy.users.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        model = self._to_model(user)
        merged = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(merged)
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.get(UserModel, user_id)
        return self._to_domain(result) if result else None

    async def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(statement)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def delete(self, user_id: UUID) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_model(self, user: User) -> UserModel:
        hashed = user.hashed_password
        return UserModel(
            id=user.id,
            name=user.name,
            email=user.email.value,
            hashed_password=hashed.value if hasattr(hashed, "value") else hashed,
            role=user.role.value,
            created_at=user.created_at.replace(tzinfo=None),
        )

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=Email(model.email),
            hashed_password=HashedPassword(model.hashed_password),
            role=UserRole(model.role),
            created_at=model.created_at,
        )
