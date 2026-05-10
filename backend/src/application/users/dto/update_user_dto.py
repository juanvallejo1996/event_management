
from dataclasses import dataclass


@dataclass
class UpdateUserDTO:
    name: str
    role: str