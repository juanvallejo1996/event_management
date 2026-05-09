from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.events.event_exceptions import EventNotFound, InvalidEventCapacity
from src.domain.users.user_exceptions import (
    UserNotFound, 
    UserAlreadyExists, 
    UserInvalidCredentials, 
    UserUnauthorized, 
    InvalidEmailFormat, 
    InvalidPasswordFormat)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EventNotFound)
    async def event_not_found_handler(request: Request, exc: EventNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidEventCapacity)
    async def invalid_capacity_handler(request: Request, exc: InvalidEventCapacity):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

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