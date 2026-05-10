import bcrypt
from dataclasses import dataclass
from src.domain.users.user_exceptions import InvalidPasswordFormat

@dataclass(frozen=True)
class HashedPassword:
    value: str

    @classmethod
    def from_plain(cls, plain: str) -> "HashedPassword":
        if len(plain) < 8:
            raise InvalidPasswordFormat("Password must be at least 8 characters")
        
        hashed = bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
        return cls(value=hashed)

    def verify(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode(), self.value.encode())