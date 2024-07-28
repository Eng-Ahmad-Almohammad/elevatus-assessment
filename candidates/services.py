"""This module has the service for interacting with Candidate model."""
import csv
import io
from uuid import UUID

from fastapi import HTTPException, status

from candidates.models import Candidate
from candidates.repos import CandidateRepo
from candidates.schemas import CandidateIn, CareerLevel, Countries, DegreeType, Gender, JobMajor


class CandidateServices:
    """Service that interact with Candidate model."""

    def __init__(self, candidate_repo: CandidateRepo) -> None:
        """Class constructor.

        Args:
            candidate_repo (CandidateRepo): instance of CandidateRepo
        """
        self.repo = candidate_repo

    async def get_candidate_by_uuid(self, candidate_uuid: UUID) -> Candidate:
        """Get the candidate by uuid.

        Args:
            candidate_uuid (UUID): Candidate uuid.

        Raises:
            HTTPException: If the user not found.

        Returns:
            Candidate: An instance of Candidate model.
        """
        candidate: Candidate | None = await self.repo.get_by_uuid(candidate_uuid)
        if candidate:
            return candidate
        raise HTTPException(status_code=404, detail="Candidate not found")

    async def create(self, candidate: CandidateIn) -> Candidate:
        """Create candidate in the db.

        Args:
            candidate (CandidateIn): The required data to create candidate.

        Returns:
            Candidate: An instance of Candidate.
        """
        created_candidate = await self.repo.get_by_email(candidate.email)
        if created_candidate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already used.",
            )
        candidate = Candidate(**candidate.model_dump())
        return await self.repo.create(candidate)

    async def update_candidate_by_uuid(
        self,
        candidate_uuid: UUID,
        candidate_update: CandidateIn,
    ) -> Candidate:
        """Update candidate in the db.

        Args:
            candidate_uuid (UUID): Candidate uuid.
            candidate_update (CandidateIn): The required data to update candidate.

        Returns:
            Candidate: Updated record.
        """
        if candidate_update.email:
            created_candidate = await self.repo.get_by_email(candidate_update.email)
            if created_candidate and str(created_candidate.uuid) != str(candidate_uuid):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already used.",
                )
        updated_data: dict = candidate_update.model_dump(exclude_unset=True)
        return await self.repo.update(candidate_uuid, updated_data)

    async def delete_candidate_by_uuid(self, candidate_uuid: UUID) -> None:
        """Delete candidate.

        Args:
            candidate_uuid (UUID): Candidate uuid.
        """
        return await self.repo.delete(candidate_uuid)

    async def get_all_candidates(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        career_level: CareerLevel | None = None,
        job_major: JobMajor | None = None,
        years_of_experience: int | None = None,
        degree_type: DegreeType | None = None,
        skills: str | None = None,
        nationality: Countries | None = None,
        city: str | None = None,
        salary: float | None = None,
        gender: Gender | None = None,
        keyword: str | None = None,
    ) -> list[Candidate] | None:
        """Get all candidates or filter them based on search criteria.

        This method is filtering candidates using 'and' between search terms.

        Args:
            first_name (str | None): Candidate first name to search for.
            last_name (str | None): Candidate last name to search for.
            email (str | None): Candidate email to search for.
            career_level (CareerLevel | None): Candidate career level to search for.
            job_major (JobMajor | None): Candidate job major to search for.
            years_of_experience (int | None): Candidate years of experience to search for.
            degree_type (DegreeType | None): Candidate degree type to search for.
            skills (str | None): Candidate skill to search for.
            nationality (Countries | None): Candidate nationality to search for.
            city (str | None): Candidate city to search for.
            salary (float | None): Candidate salary to search for.
            gender (Gender | None): Candidate gender to search for.
            keyword (str | None): Any info about candidate to search for
            the candidate using all candidate's fields.

        Returns:
            list[Candidate] | None: If no candidate found using the search criteria
            then return None else return list of Candidates.
        """
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

    async def generate_csv_file_with_all_candidates(self) -> io.StringIO:
        """Generate CSV StringIO with all candidates data.

        Returns:
            io.StringIO: In memeory csv file.
        """
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
            ],
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
                ],
            )

        output.seek(0)
        return output
