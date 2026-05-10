from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.events.event_status import EventStatus


@dataclass
class Event:
    id: UUID
    name: str
    description: str
    capacity: int
    status: EventStatus
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    updated_at: datetime

    def has_capacity(self, current_registrations: int) -> bool:
        return self.capacity > current_registrations

    def can_add_session(self, session_capacity: int, current_sessions_total: int) -> bool:
        return self.capacity >= (current_sessions_total + session_capacity)
