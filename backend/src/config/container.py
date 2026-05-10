import os

from src.infrastructure.security.jwt_token_service import JWTTokenService

_jwt_token_service = JWTTokenService(secret_key=os.environ["JWT_SECRET"])


def build_jwt_token_service() -> JWTTokenService:
    return _jwt_token_service
