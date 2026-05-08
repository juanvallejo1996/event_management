from fastapi import FastAPI

from src.domains.events.presentation.routers.event_router import (
    router as event_router
)

app = FastAPI(
    title="Event Management API"
)

app.include_router(
    event_router
)