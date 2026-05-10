
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime

class EventModel(SQLModel, table=True):
    __tablename__ = "events"

    id: UUID = Field(primary_key=True)
    name: str
    description: str
    capacity: int
    status: str
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    updated_at: datetime