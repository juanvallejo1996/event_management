
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UpdateEventDTO:
    
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None