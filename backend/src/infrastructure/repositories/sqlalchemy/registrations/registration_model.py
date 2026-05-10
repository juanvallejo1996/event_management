
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime


class RegisterModel(SQLModel, table=True):
    __tablename__ = "registrations"
    
    id: UUID  = Field(primary_key=True)
    user_id: UUID
    event_id: UUID
    registered_at: datetime
    status: str
