from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.registrations.ports.registration_repository import RegistrationRepository
from src.domain.events.ports.event_repository import EventRepository
from src.domain.users.ports.user_repository import UserRepository
from src.infrastructure.http.database_dependencies import get_db_session
from src.infrastructure.repositories.sqlalchemy.registrations.sql_alchemy_registration_repository import SQLAlchemyRegistrationRepository
from src.infrastructure.repositories.sqlalchemy.events.sql_alchemy_event_repository import SQLAlchemyEventRepository
from src.infrastructure.repositories.sqlalchemy.users.sql_alchemy_user_repository import SQLAlchemyUserRepository

from src.application.registrations.use_cases.get_user_registrations_use_case import GetUserRegistrationsUseCase
from src.application.registrations.use_cases.register_user_to_event_use_case import RegisterUserToEventUseCase


def get_registration_repository(
    session: AsyncSession = Depends(get_db_session)
) -> RegistrationRepository:
    return SQLAlchemyRegistrationRepository(session)


def get_event_repository(
    session: AsyncSession = Depends(get_db_session)
) -> EventRepository:
    return SQLAlchemyEventRepository(session)


def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_get_user_registration_use_case(
    repo: RegistrationRepository = Depends(get_registration_repository)
) -> GetUserRegistrationsUseCase:
    return GetUserRegistrationsUseCase(repo)


def get_register_user_to_event_use_case(
    repo: RegistrationRepository = Depends(get_registration_repository),
    event_repo: EventRepository = Depends(get_event_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> RegisterUserToEventUseCase:
    return RegisterUserToEventUseCase(repo, event_repo, user_repo)
