from uuid import UUID, uuid4

from beanie import Document
from pydantic import EmailStr, Field


class Candidate(Document):
    uuid: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr
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
        collection = "candidates"

    class Config:
        json_encoders = {
            UUID: str,
        }
        populate_by_name = True
