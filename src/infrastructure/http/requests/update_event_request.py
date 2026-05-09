from datetime import datetime

from pydantic import BaseModel


class UpdateEventRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    capacity: int | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None