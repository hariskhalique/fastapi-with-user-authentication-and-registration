import traceback
from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.config.exception.global_exception import GlobalException
logger = getLogger(__name__)

def register_exception_handler(app: FastAPI):
    print("Registering exception handler")

    # Handle custom exceptions
    @app.exception_handler(GlobalException)
    async def app_exception_handler(request: Request, exc: GlobalException):
        logger.error(f"AppException: {exc.message} - {exc.detail}")
        print('app_exception_handler triggered')  # Debug print
        return JSONResponse(
            content={"error": exc.message, "detail": exc.detail},
            status_code=exc.status,
        )

    # Handle unhandled exceptions
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """ Global exception handler for better debugging """
        error_message = {
            "error": str(exc),
            "method": request.method,
            "url": str(request.url),
            "traceback": traceback.format_exc()
        }
        logger.error(f"Unhandled Exception: {error_message}")  # Logs full stack trace

        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "details": str(exc)}
        )

    # Define a global handler for HTTP exceptions, including 404
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == 404:
            logger.warning(f"404 error at {request.url}")
            print('http_exception_handler triggered for 404')  # Debug print
            return JSONResponse(
                content={"error": "Not Found", "detail": "The requested resource was not found."},
                status_code=404,
            )
        logger.warning(f"HTTP exception: {exc.detail} at {request.url}")
        print('http_exception_handler triggered')  # Debug print
        return JSONResponse(
            content={"error": exc.detail},
            status_code=exc.status_code,
        )