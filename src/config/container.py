import os

from src.infrastructure.repositories.in_memory.events.in_memory_event_repository import InMemoryEventRepository
from src.infrastructure.repositories.in_memory.users.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.repositories.in_memory.sessions.in_memory_session_repository import InMemorySessionRepository
from src.infrastructure.repositories.in_memory.registrations.in_memory_registration_repository import (
    InMemoryRegistrationRepository,
)
from src.infrastructure.security.jwt_token_service import JWTTokenService

_event_repository = InMemoryEventRepository()
_user_repository = InMemoryUserRepository()
_session_repository = InMemorySessionRepository()
_registration_repository = InMemoryRegistrationRepository()
_jwt_token_service = JWTTokenService(secret_key=os.environ["JWT_SECRET"])


def build_event_repository() -> InMemoryEventRepository:
    return _event_repository


def build_user_repository() -> InMemoryUserRepository:
    return _user_repository


def build_session_repository() -> InMemorySessionRepository:
    return _session_repository


def build_registration_repository() -> InMemoryRegistrationRepository:
    return _registration_repository


def build_jwt_token_service() -> JWTTokenService:
    return _jwt_token_service
