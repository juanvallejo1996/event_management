
from src.domain.users.ports.user_repository import UserRepository
from src.domain.users.ports.token_service import TokenService
from src.domain.users.value_objects.email import Email
from src.domain.users.user_exceptions import UserInvalidCredentials
from src.application.users.dto.login_dto import LoginDTO


class LoginUseCase:
    
    def __init__(
        self,
        repository: UserRepository, token_service: TokenService
    ):
        self.repository = repository
        self.token_service = token_service

    async def execute(
        self,
        data: LoginDTO
    ) -> str:
        email = Email(data.email)
        user = await self.repository.get_by_email(email.value)

        if not user:
            raise UserInvalidCredentials()

        if not user.hashed_password.verify(data.password):
            raise UserInvalidCredentials() 
        
        return await self.token_service.generate_token(user.id)