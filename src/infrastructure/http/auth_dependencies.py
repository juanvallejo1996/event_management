from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.user import User
from src.domain.users.user_role import UserRole
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.user_exceptions import UserUnauthorized
from src.infrastructure.http.database_dependencies import get_db_session
from src.infrastructure.repositories.sqlalchemy.users.sql_alchemy_user_repository import SQLAlchemyUserRepository
from src.infrastructure.security.jwt_token_service import JWTTokenService
from src.config.container import build_jwt_token_service


bearer = HTTPBearer()


def get_token_service() -> JWTTokenService:
    return build_jwt_token_service()


def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    return SQLAlchemyUserRepository(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    token_service: JWTTokenService = Depends(get_token_service),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    try:
        user_id = await token_service.verify_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise UserUnauthorized("This action requires admin privileges")
    return current_user


async def require_admin_or_organizer(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in (UserRole.ADMIN, UserRole.ORGANIZER):
        raise UserUnauthorized("This action requires admin or organizer privileges")
    return current_user
