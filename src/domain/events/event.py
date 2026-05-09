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