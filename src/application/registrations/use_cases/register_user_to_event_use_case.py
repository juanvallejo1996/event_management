
from uuid import uuid4

from datetime import datetime, timezone

from src.domain.registrations.registration import Registration
from src.domain.events.event_status import EventStatus
from src.domain.registrations.registration_status import RegistrationStatus
from src.application.registrations.dto.create_registration_dto import CreateRegistrationDTO
from src.domain.registrations.ports.registration_repository import RegistrationRepository

from src.domain.events.ports.event_repository import EventRepository
from src.domain.users.ports.user_repository import UserRepository

from src.domain.registrations.registration_exceptions import (
    UserAlreadyRegisteredException,
    EventNotAvailable,
    EventCapacityFull,
)

from src.domain.users.user_exceptions import UserNotFound
from src.domain.events.event_exceptions import EventNotFound


class RegisterUserToEventUseCase:
    def __init__(
        self,
        registration_repository: RegistrationRepository,
        event_repository: EventRepository,
        user_repository: UserRepository,
    ):
        self.registration_repository = registration_repository
        self.event_repository = event_repository
        self.user_repository = user_repository

    async def execute(self, dto: CreateRegistrationDTO) -> Registration:
        user = await self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise UserNotFound("User does not exist")

        event = await self.event_repository.get_by_id(dto.event_id)
        if not event:
            raise EventNotFound("Event does not exist")
        
        elif event.status != EventStatus.PUBLISHED:
            raise EventNotAvailable(f"Event is not available the current event's state is {event.status.value}")

        existing_registration = await self.registration_repository.find_by_user_and_event(
            dto.user_id, dto.event_id
        )
        if existing_registration:
            raise UserAlreadyRegisteredException("User is already registered for this event")

        current_registrations = await self.registration_repository.count_by_event(dto.event_id)
        if not event.has_capacity(current_registrations):
            raise EventCapacityFull("Event capacity is full")

        registration = Registration(
            id=uuid4(),
            user_id=dto.user_id, 
            event_id=dto.event_id,
            registered_at=datetime.now(timezone.utc),
            status=RegistrationStatus.CONFIRMED
        )

        return await self.registration_repository.save(registration)

