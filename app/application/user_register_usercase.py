from typing import AsyncGenerator

from fastapi.params import Depends

from app.adapters.out.database.entities.user import UserCreate, User
from app.domain.services.auth_service import AuthService, get_auth_service


class UserRegisterUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, user: UserCreate) -> User:
        return await self.auth_service.create_user(user)

async def get_register_use_case(
    auth_service: AuthService = Depends(get_auth_service),
) -> AsyncGenerator[UserRegisterUseCase, None]:
    yield UserRegisterUseCase(auth_service)