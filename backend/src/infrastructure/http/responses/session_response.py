from uuid import UUID

from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

class SessionResponse(BaseModel):
    id: UUID
    event_id: UUID
    title: str
    description: str
    speaker_name: str
    speaker_bio: str
    capacity: int
    starts_at: datetime
    ends_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode="before")
    @classmethod
    def extract_speaker(cls, data):
        if hasattr(data, "speaker"):
            return {
                "id": data.id,
                "event_id": data.event_id,
                "title": data.title,
                "description": data.description,
                "speaker_name": data.speaker.name,
                "speaker_bio": data.speaker.bio,
                "capacity": data.capacity,
                "starts_at": data.starts_at,
                "ends_at": data.ends_at,
            }
        return data