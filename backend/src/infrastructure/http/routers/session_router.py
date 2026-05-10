
from uuid import UUID

from fastapi import APIRouter, Depends
from src.application.sessions.dto.create_session_dto import CreateSessionDTO
from src.application.sessions.dto.update_session_dto import UpdateSessionDTO
from src.infrastructure.http.requests.create_session_request import CreateSessionRequest
from src.infrastructure.http.requests.update_session_request import UpdateSessionRequest
from src.infrastructure.http.responses.session_response import SessionResponse

from src.infrastructure.http.auth_dependencies import get_current_user, require_admin_or_organizer

from src.infrastructure.http.session_dependencies import (
    get_get_sessions_by_event_use_case,
    get_get_session_use_case, 
    get_create_session_use_case,
    get_delete_session_use_case,
    get_update_session_use_case
)

router = APIRouter()

@router.get("/", response_model=list[SessionResponse], status_code=200)
async def get_sessions(
    event_id: UUID,
    _ = Depends(get_current_user),
    search_sessions_use_case = Depends(get_get_sessions_by_event_use_case)
):
    sessions = await search_sessions_use_case.execute(event_id)

    return [SessionResponse.model_validate(session) for session in sessions]


@router.get("/{session_id}", response_model=SessionResponse, status_code=200)
async def get_session(
    event_id : UUID,
    session_id: UUID,
    __ = Depends(get_current_user),
    search_sessions_use_case = Depends(get_get_session_use_case)
):
    session = await search_sessions_use_case.execute(session_id)

    return SessionResponse.model_validate(session)


@router.post("/", response_model=SessionResponse, status_code=201)
async def create_session(
    event_id: UUID,
    request: CreateSessionRequest,
    _ = Depends(require_admin_or_organizer),
    create_session_use_case = Depends(get_create_session_use_case)
):
    
    dto = CreateSessionDTO(
        event_id=event_id,
        title=request.title,
        description=request.description,
        speaker_name=request.speaker_name,
        speaker_bio=request.speaker_bio,
        capacity=request.capacity,
        starts_at=request.starts_at,
        ends_at=request.ends_at
    )
    
    session = await create_session_use_case.execute(dto)
    
    return SessionResponse.model_validate(session)
    
    
@router.delete("/{session_id}", response_model=None, status_code=204)
async def delete_session(
    event_id: UUID,
    session_id: UUID,
    __ = Depends(require_admin_or_organizer),
    delete_session_use_case = Depends(get_delete_session_use_case)
):
    await delete_session_use_case.execute(session_id)
    
    return

@router.put("/{session_id}", response_model=SessionResponse, status_code=200)
async def update_session(
    event_id: UUID,
    session_id: UUID,
    request: UpdateSessionRequest,
    _ = Depends(require_admin_or_organizer),
    update_session_use_case = Depends(get_update_session_use_case)
):
    dto = UpdateSessionDTO(
        event_id=event_id,
        title=request.title,
        description=request.description,
        speaker_name=request.speaker_name,
        speaker_bio=request.speaker_bio,
        capacity=request.capacity,
        starts_at=request.starts_at,
        ends_at=request.ends_at
    )
    
    session = await update_session_use_case.execute(session_id, dto)
    
    return SessionResponse.model_validate(session)
