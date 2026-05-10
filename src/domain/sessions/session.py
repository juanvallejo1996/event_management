
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.sessions.session_status import SessionStatus
from src.domain.sessions.value_objects.speaker import Speaker


@dataclass
class Session:
    id: UUID
    event_id: UUID
    title: str
    description: str
    capacity: int
    speaker: Speaker
    status: SessionStatus
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    updated_at: datetime