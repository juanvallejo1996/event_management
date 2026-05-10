
from datetime import datetime

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    title: str
    description: str
    speaker_name: str
    speaker_bio: str
    capacity: int
    starts_at: datetime
    ends_at: datetime