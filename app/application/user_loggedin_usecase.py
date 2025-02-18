from typing import AsyncGenerator

from fastapi.params import Depends

from app.domain.services.auth_service import AuthService, get_auth_service


class UserLoggedUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, username: str, password: str):
        return await self.auth_service.login_user(username, password)

async def get_loggedin_use_case(
        auth_service: AuthService = Depends(get_auth_service)
)-> AsyncGenerator[UserLoggedUseCase, None]:
    return UserLoggedUseCase(auth_service)