from collections.abc import AsyncGenerator

from fastapi.params import Depends

from app.domain.services.auth_service import AuthService, get_auth_service


class RefreshTokenUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, token: str):
        refreshed_token = await self.auth_service.refresh_access_token(token)
        return refreshed_token

async def get_refresh_token_use_case(
        auth_service: AuthService = Depends(get_auth_service)
)-> AsyncGenerator[RefreshTokenUseCase, None]:
    return RefreshTokenUseCase(auth_service)