from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.events.ports.event_repository import EventRepository
from src.infrastructure.http.database_dependencies import get_db_session
from src.infrastructure.repositories.sqlalchemy.events.sql_alchemy_event_repository import SQLAlchemyEventRepository

from src.application.events.use_cases.create_event_use_case import CreateEventUseCase
from src.application.events.use_cases.get_event_use_case import GetEventUseCase
from src.application.events.use_cases.search_event_use_case import SearchEventsUseCase
from src.application.events.use_cases.update_event_use_case import UpdateEventUseCase
from src.application.events.use_cases.delete_event_use_case import DeleteEventUseCase


def get_event_repository(
    session: AsyncSession = Depends(get_db_session)
) -> EventRepository:
    return SQLAlchemyEventRepository(session)


def get_get_event_use_case(
    repo: EventRepository = Depends(get_event_repository)
) -> GetEventUseCase:
    return GetEventUseCase(repo)


def get_search_events_use_case(
    repo: EventRepository = Depends(get_event_repository)
) -> SearchEventsUseCase:
    return SearchEventsUseCase(repo)


def get_create_event_use_case(
    repo: EventRepository = Depends(get_event_repository)
) -> CreateEventUseCase:
    return CreateEventUseCase(repo)


def get_update_event_use_case(
    repo: EventRepository = Depends(get_event_repository)
) -> UpdateEventUseCase:
    return UpdateEventUseCase(repo)


def get_delete_event_use_case(
    repo: EventRepository = Depends(get_event_repository)
) -> DeleteEventUseCase:
    return DeleteEventUseCase(repo)
