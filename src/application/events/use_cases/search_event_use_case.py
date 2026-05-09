
from src.domain.events.event import Event
from src.domain.events.ports.event_repository import EventRepository

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