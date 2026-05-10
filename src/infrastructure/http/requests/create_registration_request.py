
from uuid import UUID
from pydantic import BaseModel


class CreateRegistrationRequest(BaseModel):
    event_id: UUID