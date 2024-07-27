import csv
import io
from uuid import UUID

from fastapi import HTTPException

from candidates.models import Candidate
from candidates.repos import CandidateRepo
from candidates.schemas import (
    CandidateIn,
    CareerLevel,
    Countries,
    DegreeType,
    Gender,
    JobMajor,
    UpdateCandidate,
)


class CandidateServices:
    def __init__(self, candidate_repo: CandidateRepo) -> None:
        self.repo = candidate_repo

    async def get_candidate_by_uuid(self, candidate_uuid: UUID) -> Candidate:
        candidate = await self.repo.get_by_uuid(candidate_uuid)
        if candidate:
            return candidate
        raise HTTPException(status_code=404, detail="Candidate not found")

    async def create(self, candidate: CandidateIn) -> Candidate:
        candidate = Candidate(**candidate.model_dump())
        return await self.repo.create(candidate)

    async def update_candidate_by_uuid(
        self, candidate_uuid: UUID, candidate_update: UpdateCandidate
    ):
        updated_data: dict = candidate_update.model_dump(exclude_unset=True)
        return await self.repo.update(candidate_uuid, updated_data)

    async def delete_candidate_by_uuid(self, candidate_uuid: UUID):
        return await self.repo.delete(candidate_uuid)

    async def get_all_candidates(
        self,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        career_level: CareerLevel | None,
        job_major: JobMajor | None,
        years_of_experience: int | None,
        degree_type: DegreeType | None,
        skills: str | None,
        nationality: Countries | None,
        city: str | None,
        salary: float | None,
        gender: Gender | None,
        keyword: str | None,
    ):
        filters = {}
        if first_name:
            filters["first_name"] = first_name
        if last_name:
            filters["last_name"] = last_name
        if email:
            filters["email"] = email
        if career_level:
            filters["career_level"] = career_level.value
        if job_major:
            filters["job_major"] = job_major.value
        if years_of_experience:
            filters["years_of_experience"] = years_of_experience
        if degree_type:
            filters["degree_type"] = degree_type.value
        if skills:
            filters["skills"] = skills
        if nationality:
            filters["nationality"] = nationality.value
        if city:
            filters["city"] = city
        if salary is not None:
            filters["salary"] = salary
        if gender:
            filters["gender"] = gender.value
        if keyword:
            filters["$or"] = [
                {"first_name": {"$regex": keyword, "$options": "i"}},
                {"last_name": {"$regex": keyword, "$options": "i"}},
                {"email": {"$regex": keyword, "$options": "i"}},
                {"career_level": {"$regex": keyword, "$options": "i"}},
                {"job_major": {"$regex": keyword, "$options": "i"}},
                {"years_of_experience": {"$regex": keyword, "$options": "i"}},
                {"degree_type": {"$regex": keyword, "$options": "i"}},
                {"skills": {"$regex": keyword, "$options": "i"}},
                {"nationality": {"$regex": keyword, "$options": "i"}},
                {"city": {"$regex": keyword, "$options": "i"}},
                {"salary": {"$regex": keyword, "$options": "i"}},
                {"gender": {"$regex": keyword, "$options": "i"}},
            ]

        return await self.repo.get_all(filters)

    async def generate_csv_file_with_all_candidates(self):
        all_candidates: list[Candidate] = await self.get_all_candidates()
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "UUID",
                "First Name",
                "Last Name",
                "Email",
                "Career Level",
                "Job Major",
                "Years Of Experience",
                "Degree Type",
                "Skills",
                "Nationality",
                "City",
                "Salary",
                "Gender",
            ]
        )

        for candidate in all_candidates:
            uuid = str(candidate.uuid)
            skills = "; ".join(candidate.skills)
            writer.writerow(
                [
                    uuid,
                    candidate.first_name,
                    candidate.last_name,
                    candidate.email,
                    candidate.career_level,
                    candidate.job_major,
                    candidate.years_of_experience,
                    candidate.degree_type,
                    skills,
                    candidate.nationality,
                    candidate.city,
                    candidate.salary,
                    candidate.gender,
                ]
            )

        output.seek(0)
        return output
