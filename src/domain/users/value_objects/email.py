
import re
from dataclasses import dataclass
from src.domain.users.user_exceptions import InvalidEmailFormat

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.value):
            raise InvalidEmailFormat(f"Invalid email format: {self.value}")