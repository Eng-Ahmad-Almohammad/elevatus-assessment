"""A module that has the DB model for User."""

from uuid import UUID, uuid4

from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    """DB model to interact with User collections."""

    uuid: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str

    class Settings:
        """Setting class."""

        collection = "users"

    class Config:
        """Configuration class."""

        json_encoders = {
            UUID: str,
        }
        populate_by_name = True
