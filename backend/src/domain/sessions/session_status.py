
from enum import Enum


class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
    FINISHED = "finished"