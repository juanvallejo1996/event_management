
from src.domain.events.event_exceptions import InvalidEventCapacity

class EventCapacity:

    def __init__(self, value: int):
        if value <= 0:
            raise InvalidEventCapacity(
                "Capacity must be greater than zero"
            )

        self.value = value