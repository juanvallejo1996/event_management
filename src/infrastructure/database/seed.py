import os
from datetime import datetime, timezone
from uuid import uuid4

from src.infrastructure.database.session import async_session_factory
from src.infrastructure.repositories.sqlalchemy.users.sql_alchemy_user_repository import SQLAlchemyUserRepository
from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.value_objects.email import Email
from src.domain.users.value_objects.hashed_password import HashedPassword


async def seed_admin_user() -> None:
    admin_email = os.environ["ADMIN_EMAIL"]
    admin_password = os.environ["ADMIN_PASSWORD"]
    admin_name = os.environ["ADMIN_NAME"]

    async with async_session_factory() as session:
        repo = SQLAlchemyUserRepository(session)

        existing = await repo.get_by_email(admin_email)
        if existing:
            return

        admin = User(
            id=uuid4(),
            name=admin_name,
            email=Email(admin_email),
            hashed_password=HashedPassword.from_plain(admin_password),
            role=UserRole.ADMIN,
            created_at=datetime.now(timezone.utc),
        )
        await repo.save(admin)
