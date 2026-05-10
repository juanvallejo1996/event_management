from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEventDTO:
    name: str
    description: str
    capacity: int
    starts_at: datetime
    ends_at: datetime