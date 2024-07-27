"""A module that contains User's data pydantic schemas."""
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    """Base class for user info."""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserIn(BaseUser):
    """A class that represent the user's input data that is required to create a User instance."""

    password: str


class UserOut(BaseUser):
    """A class that represent the output to return for the created user."""

    uuid: UUID = uuid4()

    class Config:
        """Configuration class."""

        from_attributes = True
        json_encoders = {
            UUID: str,
        }
