# config/container.py

import os

from src.infrastructure.repositories.in_memory.events.in_memory_event_repository import InMemoryEventRepository
from src.infrastructure.repositories.in_memory.users.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.security.jwt_token_service import JWTTokenService

_event_repository = InMemoryEventRepository()
_user_repository = InMemoryUserRepository()
_jwt_token_service = JWTTokenService(secret_key=os.environ["JWT_SECRET"])



def build_event_repository() -> InMemoryEventRepository:
    return _event_repository

def build_user_repository() -> InMemoryUserRepository:
    return _user_repository

def build_jwt_token_service() -> JWTTokenService:
    return _jwt_token_service