from datetime import datetime

from pydantic import BaseModel


class CreateEventRequest(BaseModel):
    name: str
    description: str
    capacity: int
    starts_at: datetime
    ends_at: datetime