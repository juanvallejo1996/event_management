from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.events.event_status import EventStatus

@dataclass
class UpdateEventDTO:

    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    status: EventStatus | None = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
