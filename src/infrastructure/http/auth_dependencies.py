
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.users.user import User
from src.infrastructure.security.jwt_token_service import JWTTokenService
from src.domain.users.ports.user_repository import UserRepository

from src.config.container import build_jwt_token_service, build_user_repository


bearer = HTTPBearer()


def get_token_service():
    return build_jwt_token_service()

def get_user_repository():
    return build_user_repository()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    token_service: JWTTokenService = Depends(get_token_service),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    try:
        user_id = await token_service.verify_token(credentials.credentials)
        
        user = await user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")