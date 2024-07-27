from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class CareerLevel(str, Enum):
    junior = "Junior"
    senior = "Senior"
    mid_level = "Mid Level"


class JobMajor(str, Enum):
    computer_science = "Computer Science"
    computer_information_systems = "Computer Information Systems"
    software_engineer = "Software Engineering"
    information_technology = "Information Technology"
    data_science = "Data Science"
    other = "Other"


class DegreeType(str, Enum):
    high_school = "High School"
    bachelor = "Bachelor"
    master = "Master"
    doctorate = "Doctorate"


class Countries(str, Enum):
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
    m = "Male"
    f = "Female"
    ns = "Not Specified"


class Candidate(BaseModel):
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
    pass


class CandidateOut(Candidate):
    uuid: UUID = uuid4()

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,
        }


class UpdateCandidate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    career_level: Optional[CareerLevel] = None
    job_major: Optional[JobMajor] = None
    years_of_experience: Optional[int] = None
    degree_type: Optional[DegreeType] = None
    skills: Optional[list[str]] = None
    nationality: Optional[Countries] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    gender: Optional[Gender] = None
