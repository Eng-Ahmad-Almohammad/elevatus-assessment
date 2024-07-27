"""This module has the service for interacting with User model."""
from typing import Any

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

    async def create(self, user: UserIn) -> User:
        """Create an instance of User.

        Args:
            user (UserIn): pydantic BaseModel instance that has user's data to create.

        Returns:
            User: Instance of beanie Document that has the created instance.
        """
        user_data: dict[str, Any] = user.model_dump()
        hashed_password: str = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data.update({"hashed_password": hashed_password})
        user = User(**user_data)
        return await self.repo.create(user)
