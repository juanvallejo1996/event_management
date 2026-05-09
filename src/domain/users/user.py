from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.users.user_role import UserRole
from src.domain.users.value_objects.email import Email


@dataclass
class User:
    id: UUID
    name: str
    email: Email
    hashed_password: str
    role: UserRole
    created_at: datetime
