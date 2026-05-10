
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.registrations.registration_status import RegistrationStatus


@dataclass
class Registration:
    id: UUID
    user_id: UUID
    event_id: UUID
    registered_at: datetime
    status: RegistrationStatus