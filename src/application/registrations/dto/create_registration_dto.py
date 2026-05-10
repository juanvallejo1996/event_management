
from uuid import UUID
from dataclasses import dataclass


@dataclass
class CreateRegistrationDTO:
    user_id: UUID
    event_id: UUID
    