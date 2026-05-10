
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class UpdateSessionDTO:
    event_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    speaker_name: Optional[str] = None
    speaker_bio: Optional[str] = None
    capacity: Optional[int] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None