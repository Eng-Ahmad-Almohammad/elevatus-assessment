"""A module that contains User's data pydantic schemas."""
import re
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseUser(BaseModel):
    """Base class for user info."""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserIn(BaseUser):
    """A class that represent the user's input data that is required to create a User instance."""

    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate the password.

        Args:
            v (str): password

        Raises:
            ValueError: Where it does not meet the requirements.

        Returns:
            str: valid password
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        if re.search(r"\s", v):
            raise ValueError("Password must not contain any whitespace characters")
        return v


class UserOut(BaseUser):
    """A class that represent the output to return for the created user."""

    uuid: UUID = uuid4()

    class Config:
        """Configuration class."""

        from_attributes = True
        json_encoders = {
            UUID: str,
        }
