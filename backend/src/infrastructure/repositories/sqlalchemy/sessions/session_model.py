
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime


class SessionModel(SQLModel, table=True):
    __tablename__ = "sessions"
    
    id: UUID  = Field(primary_key=True)
    event_id: UUID
    title: str
    description: str
    capacity: int
    speaker_name: str
    speaker_bio: str
    status: str
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    updated_at: datetime