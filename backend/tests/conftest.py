from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.events.event import Event
from src.domain.events.event_status import EventStatus
from src.domain.sessions.session import Session
from src.domain.sessions.session_status import SessionStatus
from src.domain.sessions.value_objects.speaker import Speaker
from src.domain.registrations.registration import Registration
from src.domain.registrations.registration_status import RegistrationStatus
from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.value_objects.email import Email
from src.domain.users.value_objects.hashed_password import HashedPassword


@pytest.fixture
def event_id():
    return uuid4()


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def session_id():
    return uuid4()


@pytest.fixture
def now():
    return datetime(2025, 6, 1, 9, 0, 0)


@pytest.fixture
def sample_event(event_id, now):
    return Event(
        id=event_id,
        name="PyCon 2025",
        description="Python conference",
        capacity=100,
        status=EventStatus.PUBLISHED,
        starts_at=now,
        ends_at=datetime(2025, 6, 1, 18, 0, 0),
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_speaker():
    return Speaker(name="Ana García", bio="Senior Python developer")


@pytest.fixture
def sample_session(session_id, event_id, sample_speaker, now):
    return Session(
        id=session_id,
        event_id=event_id,
        title="Async Python",
        description="Deep dive into asyncio",
        capacity=30,
        speaker=sample_speaker,
        status=SessionStatus.SCHEDULED,
        starts_at=now,
        ends_at=datetime(2025, 6, 1, 11, 0, 0),
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_user(user_id, now):
    return User(
        id=user_id,
        name="Juan Pérez",
        email=Email("juan@example.com"),
        hashed_password=HashedPassword.from_plain("securepass123"),
        role=UserRole.ATTENDEE,
        created_at=now,
    )


@pytest.fixture
def sample_registration(user_id, event_id, now):
    return Registration(
        id=uuid4(),
        user_id=user_id,
        event_id=event_id,
        registered_at=now,
        status=RegistrationStatus.CONFIRMED,
    )
