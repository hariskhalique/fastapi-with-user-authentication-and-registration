from app.adapters.out.database.db import OutDatabase
from app.adapters.out.database.entities.user import User
from passlib.context import CryptContext
from typing import Optional

class UserRepository:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """ Fetch a user by email """
        return await User.find_one(User.email == email)

    async def create_user(self, user_data: dict) -> User:
        """ Hash password and create a new user """
        hashed_password = self.pwd_context.hash(user_data["password"])
        user = User(**user_data, hashed_password=hashed_password)
        await user.insert()
        return user

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """ Verify hashed password """
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """ Fetch a user by ID """
        return await User.get(user_id)

    async def save_refresh_token(self, user_id: str, refresh_token: str):
        """ Save refresh token for a user """
        user = await User.get(user_id)
        if user:
            user.refresh_token = refresh_token
            await user.save()

    async def get_refresh_token(self, user_id: str) -> Optional[str]:
        """ Retrieve stored refresh token """
        user = await User.get(user_id)
        return user.refresh_token if user else None

    async def revoke_refresh_token(self, user_id: str):
        """ Revoke a user's refresh token """
        user = await User.get(user_id)
        if user:
            user.refresh_token = None
            await user.save()