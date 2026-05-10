from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.infrastructure.http.routers.event_router import router as event_router
from src.infrastructure.http.routers.user_router import router as user_router
from src.infrastructure.http.routers.session_router import router as session_router
from src.infrastructure.http.routers.registration_router import router as register_router

from src.infrastructure.http.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Event Management API", lifespan=lifespan)

app.include_router(event_router, prefix="/api/v1/events", tags=["events"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(session_router, prefix="/api/v1/events/{event_id}/sessions", tags=["sessions"])
app.include_router(register_router, prefix="/api/v1/register", tags=["registers"])

register_exception_handlers(app)
