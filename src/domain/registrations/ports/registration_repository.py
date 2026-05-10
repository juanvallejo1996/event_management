
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.registrations.registration import Registration


class RegistrationRepository(ABC):
    
    @abstractmethod
    async def save(self, registration: Registration) -> Registration:
        pass

    @abstractmethod
    async def find_by_user_and_event(self, user_id: UUID, event_id: UUID) -> Registration:
        pass
    
    @abstractmethod
    async def count_by_event(self, event_id: UUID) -> int:
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Registration]:
        pass