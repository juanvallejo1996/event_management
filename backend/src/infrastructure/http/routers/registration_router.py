
from uuid import UUID

from fastapi import APIRouter, Depends
from src.infrastructure.http.registration_dependencies import (
    get_get_user_registration_use_case,
    get_register_user_to_event_use_case
)
from src.domain.users.user import User
from src.infrastructure.http.auth_dependencies import get_current_user

from src.application.registrations.dto.create_registration_dto import CreateRegistrationDTO

from src.infrastructure.http.requests.create_registration_request import CreateRegistrationRequest
from src.infrastructure.http.responses.registration_response import RegistrationResponse


router = APIRouter()


@router.get("/", response_model=list[RegistrationResponse], status_code=200)
async def get_registrations(
    current_user: User = Depends(get_current_user),
    get_registration_use_case = Depends(get_get_user_registration_use_case)
):
    user_id = current_user.id
    registrations = await get_registration_use_case.execute(
        user_id
    )
    
    return [RegistrationResponse.model_validate(registration) for registration in registrations]
    

@router.post("/", response_model=RegistrationResponse, status_code=201)
async def create_register(
    request: CreateRegistrationRequest,
    current_user: User = Depends(get_current_user),
    register_to_event_use_case = Depends(get_register_user_to_event_use_case)
):
    user_id = current_user.id
    dto = CreateRegistrationDTO(
        user_id=user_id,
        event_id=request.event_id
    )
    registration = await register_to_event_use_case.execute(
        dto
    )
    
    return RegistrationResponse.model_validate(registration)
    
