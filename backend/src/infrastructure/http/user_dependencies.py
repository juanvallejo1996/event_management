from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.ports.token_service import TokenService
from src.infrastructure.http.database_dependencies import get_db_session
from src.infrastructure.repositories.sqlalchemy.users.sql_alchemy_user_repository import SQLAlchemyUserRepository

from src.config.container import build_jwt_token_service

from src.application.users.use_cases.create_user_use_case import CreateUserUseCase
from src.application.users.use_cases.get_user_use_case import GetUserUseCase
from src.application.users.use_cases.search_user_use_case import SearchUserUseCase
from src.application.users.use_cases.login_use_case import LoginUseCase
from src.application.users.use_cases.update_user_role_use_case import UpdateUserRoleUseCase
from src.application.users.use_cases.delete_user_use_case import DeleteUserUseCase


def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_token_service() -> TokenService:
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


def get_update_user_role_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> UpdateUserRoleUseCase:
    return UpdateUserRoleUseCase(repo)


def get_delete_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)
