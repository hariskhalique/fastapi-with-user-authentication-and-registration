import json

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

from app.config.exception.global_exception import GlobalException


class Config(BaseSettings):
    MONGO_URI: str = Field(..., description="MongoDB URI")
    DATABASE_NAME: str = Field(..., description="Database name")
    APP_ENV: str = Field(..., description="Application environment ('development', 'production')")
    DEBUG: bool = Field(..., description="Debug mode")
    SECRET_KEY: str = Field(..., description="Secret key for jwt token")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

try:
    app_config = Config()
except ValidationError as e:
    errors = json.loads(e.json())
    formatted_errors = []
    for error in errors:
        field = ".".join(error['loc'])  # Get the field name
        message = error['msg']  # Get the error message
        formatted_errors.append(f"Error '{field}' is missing in .env: {message}")

    # Combine errors into a single exception message
    exception_message = "\n".join(formatted_errors)
    raise GlobalException(exception_message, 500) from None