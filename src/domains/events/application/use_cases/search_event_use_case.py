
from src.domains.events.domain.entities.event import Event
from src.domains.events.domain.repositories.event_repository import EventRepository


class SearchEventsUseCase:

    def __init__(
        self,
        repository: EventRepository
    ):
        self.repository = repository

    async def execute(
        self,
        query: str
    ) -> list[Event]:

        return await self.repository.search_by_name(
            query
        )