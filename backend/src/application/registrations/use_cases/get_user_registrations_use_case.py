
from uuid import UUID

from src.domain.registrations.registration import Registration
from src.domain.registrations.ports.registration_repository import RegistrationRepository
from src.domain.registrations.registration_exceptions import UserNotRegister


class GetUserRegistrationsUseCase:
    def __init__(
        self,
        registration_repository: RegistrationRepository
    ):
        self.registration_repository = registration_repository

    async def execute(self, user_id: UUID) -> list[Registration]:
        return await self.registration_repository.get_by_user(user_id)
