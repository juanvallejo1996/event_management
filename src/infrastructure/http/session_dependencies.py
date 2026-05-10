
from fastapi import Depends

from src.domain.sessions.ports.session_repository import SessionRepository
from src.domain.events.ports.event_repository import EventRepository

from src.config.container import (
    build_session_repository,
    build_event_repository
)

from src.application.sessions.use_cases.create_session_use_case import CreateSessionUseCase
from src.application.sessions.use_cases.get_session_use_case import GetSessionUseCase
from src.application.sessions.use_cases.get_sessions_by_event_use_case import GetSessionByEventUseCase
from src.application.sessions.use_cases.update_session_use_case import UpdateSessionUseCase
from src.application.sessions.use_cases.delete_session_use_case import DeleteSessionUseCase

def get_session_repository():
    return build_session_repository()

def get_event_repository():
    return build_event_repository()


def get_get_session_use_case(
    repo: SessionRepository = Depends(get_session_repository)
) -> GetSessionUseCase:
    return GetSessionUseCase(repo)


def get_get_sessions_by_event_use_case(
    repo: SessionRepository = Depends(get_session_repository)
) -> GetSessionByEventUseCase:
    return GetSessionByEventUseCase(repo)


def get_create_session_use_case(
    repo: SessionRepository = Depends(get_session_repository),
    event_repo: EventRepository = Depends(get_event_repository)
) -> CreateSessionUseCase:
    return CreateSessionUseCase(repo, event_repo)


def get_update_session_use_case(
    repo: SessionRepository = Depends(get_session_repository),
    event_repo: EventRepository = Depends(get_event_repository)
) -> UpdateSessionUseCase:
    return UpdateSessionUseCase(repo, event_repo)


def get_delete_session_use_case(
    repo: SessionRepository = Depends(get_session_repository)
) -> DeleteSessionUseCase:
    return DeleteSessionUseCase(repo)