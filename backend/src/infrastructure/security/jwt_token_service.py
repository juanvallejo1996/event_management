
import jwt
from uuid import UUID

from src.domain.users.ports.token_service import TokenService

class JWTTokenService(TokenService):
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    async def generate_token(self, user_id: UUID) -> str:
        payload = {"user_id": str(user_id)}
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    async def verify_token(self, token: str) -> UUID | None:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return UUID(payload["user_id"])
