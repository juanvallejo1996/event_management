
from uuid import UUID

from src.domain.registrations.registration import Registration
from src.domain.registrations.ports.registration_repository import RegistrationRepository

from src.domain.registrations.registration_status import RegistrationStatus


class InMemoryRegistrationRepository(RegistrationRepository):

    def __init__(self):
        self.registrations: dict[UUID, Registration] = {}

    async def save(self, registration: Registration) -> Registration:
        self.registrations[registration.id] = registration
        return registration

    async def find_by_user_and_event(self, user_id: UUID, event_id: UUID) -> Registration:
        for registration in self.registrations.values():
            if registration.user_id == user_id and registration.event_id == event_id:
                return registration
        return None
    
    async def count_by_event(self, event_id: UUID) -> int:
        return sum(1 for r in self.registrations.values() 
                   if r.event_id == event_id and r.status == RegistrationStatus.CONFIRMED)
    
    async def get_by_user(self, user_id: UUID) -> list[Registration]:
        return [r for r in self.registrations.values() if r.user_id == user_id]