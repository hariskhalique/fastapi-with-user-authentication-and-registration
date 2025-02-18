from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.adapters.out.database.db import OutDatabase  # Singleton DB instance
from app.application.middleware.app_middleware import app_middleware
from app.config.logging.logging_config import setup_logging
from app.config.exception.exception_handler import register_exception_handler
from app.adapters.http.user_route import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Handle startup & shutdown for DB connection """
    async with OutDatabase.initialize():
        yield  # Application runs here
        OutDatabase.get_instance().close() # Gracefully close DB

def app_module(application: FastAPI):
    """ Register all application components """
    setup_logging()  # Configure Logging
    app_middleware(application)  # Register Middleware
    register_exception_handler(application)  # Register Exception Handlers

    # Attach lifespan function to FastAPI
    application.router.lifespan_context = lifespan

    @application.get("/healthcheck")
    async def heartbeat():
        """ Health check endpoint """
        return {"status": 200, "message": "I am alive."}

    application.include_router(auth_router, prefix="/auth", tags=["Authentication"])