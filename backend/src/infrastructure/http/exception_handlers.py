from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.events.event_exceptions import (
    EventNotFound,
    EventAlreadyFinished,
    InvalidEventDates,
    InvalidEventCapacity,
)
from src.domain.users.user_exceptions import (
    UserNotFound,
    UserAlreadyExists,
    UserInvalidCredentials,
    UserUnauthorized,
    InvalidEmailFormat,
    InvalidPasswordFormat,
)
from src.domain.sessions.session_exceptions import (
    SessionNotFound,
    SessionAlreadyFinished,
    InvalidSessionDates,
    InvalidSessionCapacity,
)

from src.domain.registrations.registration_exceptions import (
    UserAlreadyRegisteredException,
    EventNotAvailable,
    EventCapacityFull,
    UserNotRegister,
)

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EventNotFound)
    async def event_not_found_handler(request: Request, exc: EventNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidEventCapacity)
    async def invalid_capacity_handler(request: Request, exc: InvalidEventCapacity):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidEventDates)
    async def invalid_event_dates_handler(request: Request, exc: InvalidEventDates):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(EventAlreadyFinished)
    async def event_already_finished_handler(request: Request, exc: EventAlreadyFinished):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request: Request, exc: UserNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UserInvalidCredentials)
    async def user_invalid_credentials_handler(request: Request, exc: UserInvalidCredentials):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(UserUnauthorized)
    async def user_unauthorized_handler(request: Request, exc: UserUnauthorized):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(InvalidEmailFormat)
    async def invalid_email_format_handler(request: Request, exc: InvalidEmailFormat):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidPasswordFormat)
    async def invalid_password_format_handler(request: Request, exc: InvalidPasswordFormat):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(SessionNotFound)
    async def session_not_found_handler(request: Request, exc: SessionNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(SessionAlreadyFinished)
    async def session_already_finished_handler(request: Request, exc: SessionAlreadyFinished):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidSessionDates)
    async def invalid_sesison_dates_handler(request: Request, exc: InvalidSessionDates):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidSessionCapacity)
    async def invalid_session_capacity_handler(request: Request, exc: InvalidSessionCapacity):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyRegisteredException)
    async def user_already_registered_handler(request: Request, exc: UserAlreadyRegisteredException):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(EventNotAvailable)
    async def event_not_available_handler(request: Request, exc: EventNotAvailable):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(EventCapacityFull)
    async def event_capacity_full_handler(request: Request, exc: EventCapacityFull):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UserNotRegister)
    async def user_not_register_handler(request: Request, exc: UserNotRegister):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
