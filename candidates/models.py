"""A module that has the DB model for Candidate."""
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class Candidate(Document):
    """DB model to interact with Candidate collections."""

    uuid: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr = Indexed(unique=True)
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: list[str]
    nationality: str
    city: str
    salary: float
    gender: str

    class Settings:
        """Setting class."""

        collection = "candidates"

    class Config:
        """Configuration class."""

        json_encoders = {
            UUID: str,
        }
        populate_by_name = True
