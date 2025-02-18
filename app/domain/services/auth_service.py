import os
from base64 import b64decode
from datetime import datetime, timedelta
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi_users import jwt
import jwt as pyJwt

from app.adapters.out.database.repositories.user_repository import UserRepository
from app.adapters.out.database.entities.user import User, UserCreate
from app.config.config import app_config
from logging import getLogger

logger = getLogger(__name__)

# Convert bytes to string for JWT strategy
SECRET = b64decode(app_config.SECRET_KEY)


class AuthService:
    """ Service class for user authentication using FastAPI-Users and JWT """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> User:
        """ Register a new user programmatically """
        existing_user = await self.user_repo.get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"User with email {user.email} already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        new_user = await self.user_repo.create_user(user.dict())
        logger.info(f"User {new_user.id} created successfully")
        return new_user

    async def login_user(self, email: str, password: str) -> str:
        """ Authenticate user and return JWT token """
        user = await self.user_repo.get_user_by_email(email)
        if not user or not await self.user_repo.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = self.generate_jwt(user)
        return access_token

    def generate_jwt(self, user: User) -> str:
        """ Generate JWT token with user information """
        try:
            payload = {
                "sub": str(user.id),
                "email": user.email,
                "name": user.name,
                "isStaff": user.is_staff,
                "isSuperuser": user.is_superuser,
                "isActive": user.is_active,
                "isLocked": user.is_locked,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat(),
                "exp": datetime.utcnow() + timedelta(hours=1),
            }
            return jwt.generate_jwt(payload, secret=SECRET, lifetime_seconds=3600)

        except Exception as e:
            logger.exception("Error generating JWT")
            raise

    def decode_jwt(self, token: str) -> Optional[dict]:
        """ Decode JWT token and extract payload """
        try:
            return jwt.decode_jwt(token, SECRET, algorithms=["HS256"])
        except pyJwt.PyJWTError:
            return None


# Dependency injection for AuthService
async def get_auth_service(
    user_repo: UserRepository = Depends(UserRepository),
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(user_repo)