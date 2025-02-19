import os
from base64 import b64decode
from datetime import datetime, timedelta
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi_users import jwt
import jwt as pyJwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.adapters.out.database.repositories.user_repository import UserRepository
from app.adapters.out.database.entities.user import User, UserCreate
from app.config.config import app_config
from logging import getLogger

logger = getLogger(__name__)

# Convert bytes to string for JWT strategy
SECRET = b64decode(app_config.SECRET_KEY)
ALGORITHM = "HS256"


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
        refresh_token = self.generate_refresh_token(user)

        await self.user_repo.save_refresh_token(str(user.id), refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def generate_jwt(self, user: User) -> str:
        """ Generate JWT token with user information """
        try:
            payload = self.get_payload(user)
            return jwt.generate_jwt(payload, secret=SECRET, algorithm=ALGORITHM)

        except Exception as e:
            logger.exception("Error generating JWT")
            raise

    def generate_refresh_token(self, user: User) -> str:
        """ Generate a long-lived JWT refresh token """
        try:
            payload = self.get_payload(user)
            refresh_token = jwt.generate_jwt(
                payload,
                app_config.REFRESH_SECRET_KEY,
                algorithm=ALGORITHM
            )
            return refresh_token
        except Exception as e:
            logger.exception("Error generating JWT")
            raise

    async def refresh_access_token(self, refresh_token: str) -> str:
        """ Validate refresh token and issue a new access token """
        try:
            payload = self.decode_jwt(
                refresh_token,
                app_config.REFRESH_SECRET_KEY
            )
            print(payload)
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )

            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            return self.generate_jwt(user)

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    def get_payload(self, user: User) -> Optional[dict]:
        return {
                "sub": str(user.id),
                "email": user.email,
                "name": user.name,
                "isStaff": user.is_staff,
                "isSuperuser": user.is_superuser,
                "isActive": user.is_active,
                "isLocked": user.is_locked,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat(),
                "aud": "api",
                "exp": datetime.utcnow() + timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES),
            }

    def decode_jwt(self, token: str, SECRET_TO_DECODE: str) -> Optional[dict]:
        """ Decode JWT token and extract payload """
        try:
            return jwt.decode_jwt(
                token,
                SECRET_TO_DECODE,
                algorithms=[ALGORITHM],
                audience = ["api"]
            )
        except pyJwt.PyJWTError:
            return None

# Dependency injection for AuthService
async def get_auth_service(
    user_repo: UserRepository = Depends(UserRepository),
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(user_repo)