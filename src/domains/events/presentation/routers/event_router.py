
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.domains.events.domain.exceptions.event_exceptions import (
    EventNotFound
)

from src.domains.events.application.dto.create_event_dto import (
    CreateEventDTO
)

from src.domains.events.application.use_cases.get_event_use_case import (
    GetEventUseCase
)

from src.domains.events.application.use_cases.create_event_use_case import (
    CreateEventUseCase
)

from src.domains.events.infrastructure.repositories.in_memory.in_memory_event_repository import (
    InMemoryEventRepository
)

from src.domains.events.presentation.schemas.create_event_request import (
    CreateEventRequest
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

repository = InMemoryEventRepository()

create_event_use_case = CreateEventUseCase(
    repository
)

get_event_use_case = GetEventUseCase(
    repository
)

@router.get("/{event_id}")
async def get_event(event_id: UUID):
    try:
        event = await get_event_use_case.execute(
            event_id
        )

        return event

    except EventNotFound:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


@router.post("/")
async def create_event(request: CreateEventRequest):
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

    return event