
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    capacity: int
    status: str
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)