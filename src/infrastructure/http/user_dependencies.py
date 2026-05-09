
from fastapi import Depends
from src.domain.users.ports.user_repository import UserRepository

from src.config.container import (
    build_user_repository,
    build_jwt_token_service
)

from src.application.users.use_cases.create_user_use_case import CreateUserUseCase
from src.application.users.use_cases.get_user_use_case import GetUserUseCase
from src.application.users.use_cases.search_user_use_case import SearchUserUseCase
from src.application.users.use_cases.login_use_case import LoginUseCase
from src.domain.users.ports.token_service import TokenService

def get_user_repository():
    return build_user_repository()

def get_token_service():
    return build_jwt_token_service()

def get_create_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)

def get_get_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> GetUserUseCase:
    return GetUserUseCase(repo)

def get_search_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> SearchUserUseCase:
    return SearchUserUseCase(repo)

def get_login_use_case(
    repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service)
) -> LoginUseCase:
    return LoginUseCase(repo, token_service)

