from uuid import UUID

from fastapi import APIRouter, Depends
from src.infrastructure.http.event_dependencies import (
    get_create_event_use_case, 
    get_get_event_use_case, 
    get_search_events_use_case,
    get_update_event_use_case, 
    get_delete_event_use_case
)
from src.infrastructure.http.auth_dependencies import get_current_user

from src.application.events.dto.update_event_dto import UpdateEventDTO
from src.application.events.dto.create_event_dto import CreateEventDTO

from src.infrastructure.http.requests.create_event_request import CreateEventRequest
from src.infrastructure.http.requests.update_event_request import UpdateEventRequest
from src.infrastructure.http.responses.event_response import EventResponse


router = APIRouter()


@router.get("/search/{event_name}", response_model=list[EventResponse], status_code=200)
async def search_events(
    event_name: str,
    _ = Depends(get_current_user),
    search_events_use_case = Depends(get_search_events_use_case)
):
    events = await search_events_use_case.execute(event_name)

    return [EventResponse.model_validate(event) for event in events]

@router.get("/{event_id}", response_model=EventResponse, status_code=200)
async def get_event(
    event_id: UUID,
    _ = Depends(get_current_user),
    get_event_use_case = Depends(get_get_event_use_case)
):
    event = await get_event_use_case.execute(
        event_id
    )
    return EventResponse.model_validate(event)


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    request: CreateEventRequest,
    _ = Depends(get_current_user),
    create_event_use_case = Depends(get_create_event_use_case)
    ):
    dto = CreateEventDTO(
        name=request.name,
        description=request.description,
        capacity=request.capacity,
        starts_at=request.starts_at,
        ends_at=request.ends_at
    )

    event = await create_event_use_case.execute(
        dto
    )

    return EventResponse.model_validate(event)


@router.put("/{event_id}", response_model=EventResponse, status_code=200)
async def update_event(
    event_id: UUID,
    request: UpdateEventRequest,
    _ = Depends(get_current_user),
    update_event_use_case = Depends(get_update_event_use_case)
):
    dto = UpdateEventDTO(
        name=request.name,
        description=request.description,
        capacity=request.capacity,
        starts_at=request.starts_at,
        ends_at=request.ends_at,
        status=request.status,
    )

    event = await update_event_use_case.execute(event_id, dto)

    return EventResponse.model_validate(event)


@router.delete("/{event_id}", response_model=None, status_code=204)
async def delete_event(
    event_id: UUID,
    _ = Depends(get_current_user),
    delete_event_use_case = Depends(get_delete_event_use_case)
    ):
    await delete_event_use_case.execute(event_id)

    return
