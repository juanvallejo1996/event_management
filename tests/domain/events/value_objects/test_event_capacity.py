import pytest

from src.domain.events.event_exceptions import InvalidEventCapacity
from src.domain.events.value_objects.event_capacity import EventCapacity


class TestEventCapacity:

    def test_creates_with_valid_capacity(self):
        capacity = EventCapacity(50)
        assert capacity.value == 50

    def test_creates_with_minimum_valid_capacity(self):
        capacity = EventCapacity(1)
        assert capacity.value == 1

    def test_raises_when_capacity_is_zero(self):
        with pytest.raises(InvalidEventCapacity):
            EventCapacity(0)

    def test_raises_when_capacity_is_negative(self):
        with pytest.raises(InvalidEventCapacity):
            EventCapacity(-10)

    def test_error_message_is_descriptive(self):
        with pytest.raises(InvalidEventCapacity, match="greater than zero"):
            EventCapacity(0)
