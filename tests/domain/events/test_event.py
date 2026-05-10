from datetime import datetime

import pytest

from src.domain.events.event import Event
from src.domain.events.event_exceptions import InvalidEventDates
from src.domain.events.event_status import EventStatus


class TestEventHasCapacity:

    def test_returns_true_when_registrations_below_capacity(self, sample_event):
        assert sample_event.has_capacity(current_registrations=99) is True

    def test_returns_false_when_registrations_equal_to_capacity(self, sample_event):
        assert sample_event.has_capacity(current_registrations=100) is False

    def test_returns_false_when_registrations_exceed_capacity(self, sample_event):
        assert sample_event.has_capacity(current_registrations=101) is False

    def test_returns_true_when_no_registrations(self, sample_event):
        assert sample_event.has_capacity(current_registrations=0) is True


class TestEventCanAddSession:

    def test_returns_true_when_session_fits_within_capacity(self, sample_event):
        assert sample_event.can_add_session(session_capacity=30, current_sessions_total=60) is True

    def test_returns_true_when_session_exactly_fills_capacity(self, sample_event):
        assert sample_event.can_add_session(session_capacity=30, current_sessions_total=70) is True

    def test_returns_false_when_session_exceeds_capacity(self, sample_event):
        assert sample_event.can_add_session(session_capacity=30, current_sessions_total=80) is False

    def test_returns_true_when_no_existing_sessions(self, sample_event):
        assert sample_event.can_add_session(session_capacity=50, current_sessions_total=0) is True

    def test_returns_false_when_session_alone_exceeds_capacity(self, sample_event):
        assert sample_event.can_add_session(session_capacity=101, current_sessions_total=0) is False


class TestEventValidateDates:

    def test_valid_future_dates(self):
        now = datetime(2025, 1, 1, 10, 0, 0)
        Event.validate_dates(
            starts_at=datetime(2025, 6, 1, 9, 0, 0),
            ends_at=datetime(2025, 6, 1, 18, 0, 0),
            now=now,
        )

    def test_raises_when_starts_at_is_in_the_past(self):
        now = datetime(2025, 6, 1, 12, 0, 0)
        with pytest.raises(InvalidEventDates, match="future"):
            Event.validate_dates(
                starts_at=datetime(2025, 6, 1, 10, 0, 0),
                ends_at=datetime(2025, 6, 1, 18, 0, 0),
                now=now,
            )

    def test_raises_when_starts_at_equals_now(self):
        now = datetime(2025, 6, 1, 10, 0, 0)
        with pytest.raises(InvalidEventDates):
            Event.validate_dates(
                starts_at=datetime(2025, 6, 1, 10, 0, 0),
                ends_at=datetime(2025, 6, 1, 18, 0, 0),
                now=now,
            )

    def test_raises_when_ends_at_before_starts_at(self):
        now = datetime(2025, 1, 1, 10, 0, 0)
        with pytest.raises(InvalidEventDates, match="after the start"):
            Event.validate_dates(
                starts_at=datetime(2025, 6, 1, 18, 0, 0),
                ends_at=datetime(2025, 6, 1, 9, 0, 0),
                now=now,
            )

    def test_raises_when_ends_at_equals_starts_at(self):
        now = datetime(2025, 1, 1, 10, 0, 0)
        with pytest.raises(InvalidEventDates):
            Event.validate_dates(
                starts_at=datetime(2025, 6, 1, 10, 0, 0),
                ends_at=datetime(2025, 6, 1, 10, 0, 0),
                now=now,
            )


class TestEventStatus:

    def test_all_statuses_are_defined(self):
        statuses = {s.value for s in EventStatus}
        assert statuses == {"draft", "published", "cancelled", "finished"}

    def test_status_is_string_comparable(self):
        assert EventStatus.PUBLISHED == "published"
