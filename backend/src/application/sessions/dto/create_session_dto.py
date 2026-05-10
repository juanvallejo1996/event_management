
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateSessionDTO:
    event_id: UUID
    title: str
    description: str
    speaker_name: str
    speaker_bio: str
    capacity: int
    starts_at: datetime
    ends_at: datetime