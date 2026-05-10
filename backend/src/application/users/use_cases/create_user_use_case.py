from uuid import uuid4
from datetime import datetime, timezone

from src.domain.users.value_objects.hashed_password import HashedPassword
from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.value_objects.email import Email
from src.domain.users.user_exceptions import UserAlreadyExists

from src.application.users.dto.create_user_dto import CreateUserDTO

class CreateUserUseCase:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def execute(
        self,
        data: CreateUserDTO
    ) -> User:

        email = Email(data.email)
        user = await self.repository.get_by_email(email.value)
        if user:
            raise UserAlreadyExists("User already exists")

        password = HashedPassword.from_plain(data.password)

        user = User( 
            id=uuid4(),
            name=data.name,
            email=email,
            hashed_password=password,
            role=UserRole.ATTENDEE,
            created_at=datetime.now(timezone.utc)
        )

        return await self.repository.save(user)
