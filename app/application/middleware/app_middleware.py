from logging import getLogger

from fastapi import FastAPI, Request
import time
logger = getLogger(__name__)


def app_middleware(application: FastAPI):
    @application.middleware("http")
    async def middleware(request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"Request processed in {process_time:.2f}s with status code {response.status_code}")

        return response