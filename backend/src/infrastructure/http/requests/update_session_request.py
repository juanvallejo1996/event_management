
from datetime import datetime

from pydantic import BaseModel


class UpdateSessionRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    speaker_name: str | None = None
    speaker_bio: str | None = None
    capacity: int | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None