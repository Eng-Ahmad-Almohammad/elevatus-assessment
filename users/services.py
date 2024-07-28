"""This module has the service for interacting with User model."""
from typing import Any

from fastapi import HTTPException, status

from users.models import User
from users.repos import UserRepo
from users.schemas import UserIn
from utils.security import get_password_hash


class UserServices:
    """Service that interact with User model."""

    def __init__(self, user_repo: UserRepo) -> None:
        """Class constructor.

        Args:
            user_repo (UserRepo): Instance of UserRepo
        """
        self.repo: UserRepo = user_repo

    async def get_user_by_email(self, email: str) -> User | None:
        """Get an instance of User by email.

        Args:
            email (str)

        Returns:
            User: Instance of beanie Document.
        """
        return await self.repo.get_user_by_email(email)

    async def create(self, user: UserIn) -> User:
        """Create an instance of User.

        Args:
            user (UserIn): pydantic BaseModel instance that has user's data to create.

        Returns:
            User: Instance of beanie Document that has the created instance.
        """
        created_user = await self.repo.get_by_email(user.email)
        if created_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )
        user_data: dict[str, Any] = user.model_dump()
        hashed_password: str = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data.update({"hashed_password": hashed_password})
        user = User(**user_data)
        return await self.repo.create(user)
