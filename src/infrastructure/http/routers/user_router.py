
from uuid import UUID

from fastapi import APIRouter, Depends
from src.infrastructure.http.user_dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_search_user_use_case,
    get_login_use_case,
    get_update_user_role_use_case,
    get_delete_user_use_case,
)
from src.infrastructure.http.auth_dependencies import get_current_user, require_admin

from src.application.users.dto.create_user_dto import CreateUserDTO
from src.application.users.dto.login_dto import LoginDTO

from src.infrastructure.http.requests.create_user_request import CreateUserRequest
from src.infrastructure.http.requests.login_request import LoginRequest
from src.infrastructure.http.requests.update_user_role_request import UpdateUserRoleRequest

from src.infrastructure.http.responses.user_response import UserResponse

router = APIRouter()

@router.get("/search/{email}", response_model=UserResponse, status_code=200)
async def search_user_by_email(
    email: str,
    _ = Depends(get_current_user),
    search_user_use_case = Depends(get_search_user_use_case)
):
    user = await search_user_use_case.execute(email)

    return UserResponse.model_validate(user)

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(
    user_id: UUID,
    _ = Depends(get_current_user),
    get_user_use_case = Depends(get_get_user_use_case)
):
    user = await get_user_use_case.execute(
        user_id
    )
    return UserResponse.model_validate(user)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    create_user_use_case = Depends(get_create_user_use_case)
    ):
    dto = CreateUserDTO(
        email=request.email,
        password=request.password,
        name=request.name
    )

    user = await create_user_use_case.execute(
        dto
    )

    return UserResponse.model_validate(user)

@router.post("/login", status_code=200)
async def login(
    request: LoginRequest,
    login_use_case = Depends(get_login_use_case)
):
    dto = LoginDTO(
        email=request.email,
        password=request.password
    )

    token = await login_use_case.execute(
        dto
    )

    return {"access_token": token}


@router.patch("/{user_id}/role", response_model=UserResponse, status_code=200)
async def update_user_role(
    user_id: UUID,
    request: UpdateUserRoleRequest,
    _ = Depends(require_admin),
    update_role_use_case = Depends(get_update_user_role_use_case),
):
    user = await update_role_use_case.execute(user_id, request.role)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", response_model=None, status_code=204)
async def delete_user(
    user_id: UUID,
    _ = Depends(require_admin),
    delete_use_case = Depends(get_delete_user_use_case),
):
    await delete_use_case.execute(user_id)