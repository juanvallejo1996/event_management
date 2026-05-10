
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class RegistrationResponse(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    status: str
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("status", mode="before")
    @classmethod
    def extract_status(cls, v):
        if hasattr(v, "value"):
            return v.value
        return v
