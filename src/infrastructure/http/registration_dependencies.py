
from fastapi import Depends

from src.domain.registrations.ports.registration_repository import RegistrationRepository
from src.domain.events.ports.event_repository import EventRepository
from src.domain.users.ports.user_repository import UserRepository

from src.config.container import (
    build_registration_repository,
    build_event_repository,
    build_user_repository
)

from src.application.registrations.use_cases.get_user_registrations_use_case import GetUserRegistrationsUseCase
from src.application.registrations.use_cases.register_user_to_event_use_case import RegisterUserToEventUseCase


def get_registration_repository():
    return build_registration_repository()


def get_event_repository():
    return build_event_repository()


def get_user_repository():
    return build_user_repository()


def get_get_user_registration_use_case(
    repo: RegistrationRepository = Depends(get_registration_repository)
):
    return GetUserRegistrationsUseCase(repo)


def get_register_user_to_event_use_case(
    repo: RegistrationRepository = Depends(get_registration_repository),
    event_repo: EventRepository = Depends(get_event_repository),
    user_repo: UserRepository = Depends(get_user_repository)
):
    return RegisterUserToEventUseCase(repo, event_repo, user_repo)
