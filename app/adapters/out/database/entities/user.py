from datetime import datetime
from typing import override

from beanie import PydanticObjectId
from fastapi_users.schemas import BaseUserCreate, BaseUserUpdate, BaseUser
from fastapi_users_db_beanie import BeanieBaseUserDocument
from pydantic import Field


class UserCreate(BaseUserCreate):
    name: str
    two_factor_enabled: bool = False

class UserUpdate(BaseUserUpdate):
    name: str
    updated_at: datetime = Field(default_factory=datetime.now)
    two_factor_enabled: bool = False
    two_factor_secret: str | None = None
    two_factor_backup_codes: list[str] | None = None

class UserBase(BaseUser[PydanticObjectId]):
    name: str
    is_staff: bool = False
    is_locked: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: datetime | None = None
    last_failed_login: datetime | None = None
    failed_log_attempts: int = 0
    two_factor_enabled: bool = False
    two_factor_secret: str | None = None
    two_factor_backup_codes: list[str] | None = None
    preferred_language: str = "en"  # Default to English

class User(BeanieBaseUserDocument, UserBase):
    @override
    class Settings(BeanieBaseUserDocument.Settings):
        is_root = False
        name = "users"

    async def successful_login(self) -> None:
        self.last_login = datetime.now()
        await self.save()

    async def failed_login(self) -> None:
        self.last_failed_login = datetime.now()
        self.failed_log_attempts += 1
        await self.save()