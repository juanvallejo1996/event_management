
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator("email", "role", mode="before")
    @classmethod
    def extract_value(cls, v):
        if hasattr(v, "value"):
            return v.value
        return v