
from dataclasses import dataclass


@dataclass(frozen=True)
class Speaker:
    name: str
    bio: str