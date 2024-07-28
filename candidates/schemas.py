"""A module that contains Candidate's data pydantic schemas."""
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class CareerLevel(str, Enum):
    """Enum for career level.

    It inherits str so pydantic recognize the value as string.
    """

    junior = "Junior"
    senior = "Senior"
    mid_level = "Mid Level"


class JobMajor(str, Enum):
    """Enum for job major.

    It inherits str so pydantic recognize the value as string.
    """

    computer_science = "Computer Science"
    computer_information_systems = "Computer Information Systems"
    software_engineer = "Software Engineering"
    information_technology = "Information Technology"
    data_science = "Data Science"
    other = "Other"


class DegreeType(str, Enum):
    """Enum for degree type.

    It inherits str so pydantic recognize the value as string.
    """

    high_school = "High School"
    bachelor = "Bachelor"
    master = "Master"
    doctorate = "Doctorate"


class Countries(str, Enum):
    """Enum for countries.

    It inherits str so pydantic recognize the value as string.
    """

    # We went with Enum for countries because those values are not changing frequently,
    # so it is easier for validation to use it as Enum
    us = "United States"
    ca = "Canada"
    gb = "United Kingdom"
    fr = "France"
    de = "Germany"
    jp = "Japan"
    cn = "China"
    jo = "Jordan"


class Gender(str, Enum):
    """Enum for gender.

    It inherits str so pydantic recognize the value as string.
    """

    m = "Male"
    f = "Female"
    ns = "Not Specified"


class Candidate(BaseModel):
    """Base class for candidate info."""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    career_level: CareerLevel
    job_major: JobMajor
    years_of_experience: int = Field(..., ge=0)
    degree_type: DegreeType
    skills: list[str] = Field(..., min_items=1)
    nationality: Countries
    city: str = Field(..., min_length=2, max_length=100)
    salary: float = Field(..., ge=0)
    gender: Gender


class CandidateIn(Candidate):
    """A class that represent the candidate's input data that is required to create a Candidate instance."""

    pass


class CandidateOut(Candidate):
    """A class that represent the output to return for the created candidate."""

    uuid: UUID = uuid4()

    class Config:
        """Configuration class."""

        from_attributes = True
        json_encoders = {
            UUID: str,
        }
