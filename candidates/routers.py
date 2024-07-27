from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from pydantic import EmailStr

from candidates.schemas import (
    CandidateIn,
    CandidateOut,
    CareerLevel,
    Countries,
    DegreeType,
    Gender,
    JobMajor,
    UpdateCandidate,
)
from candidates.services import CandidateServices
from DIContainer import DIContainer
from users.models import User
from utils.security import get_current_user

candidate_router = APIRouter(prefix="/candidate", tags=["candidate"])

all_candidate_router = APIRouter(prefix="/all-candidates", tags=["all_candidates"])

generate_report_router = APIRouter(prefix="/generate-report", tags=["generate_report"])


@candidate_router.get(
    "/{candidate_id}", response_model=CandidateOut, status_code=status.HTTP_200_OK
)
@inject
async def get_candidate(
    candidate_id: UUID,
    current_user: User = Depends(get_current_user),
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    return await candidate_services.get_candidate_by_uuid(candidate_id)


@candidate_router.post(
    "/", response_model=CandidateOut, status_code=status.HTTP_201_CREATED
)
@inject
async def create_candidate(
    candidate: CandidateIn,
    current_user: User = Depends(get_current_user),
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    return await candidate_services.create(candidate)


@candidate_router.put(
    "/{candidate_id}", response_model=CandidateOut, status_code=status.HTTP_201_CREATED
)
@inject
async def update_candidate(
    candidate_id: UUID,
    update_candidate: UpdateCandidate,
    current_user: User = Depends(get_current_user),
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    return await candidate_services.update_candidate_by_uuid(
        candidate_id, update_candidate
    )


@candidate_router.delete(
    "/{candidate_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_candidate(
    candidate_id: UUID,
    current_user: User = Depends(get_current_user),
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    return await candidate_services.delete_candidate_by_uuid(candidate_id)


@all_candidate_router.get(
    "/", response_model=list[CandidateOut], status_code=status.HTTP_200_OK
)
@inject
async def get_all_candidates(
    first_name: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    last_name: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    email: EmailStr | None = None,
    career_level: CareerLevel | None = None,
    job_major: JobMajor | None = None,
    years_of_experience: Annotated[int | None, Query(ge=0)] = None,
    degree_type: DegreeType | None = None,
    skills: Annotated[str | None, Query()] = None,
    nationality: Countries | None = None,
    city: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    salary: Annotated[float | None, Query(ge=0)] = None,
    gender: Gender | None = None,
    keyword: str | None = None,
    current_user: User = Depends(get_current_user),
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    return await candidate_services.get_all_candidates(
        first_name,
        last_name,
        email,
        career_level,
        job_major,
        years_of_experience,
        degree_type,
        skills,
        nationality,
        city,
        salary,
        gender,
        keyword,
    )


@generate_report_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "CSV file with all candidates",
            "content": {"text/csv": {"schema": {"type": "string", "format": "binary"}}},
        }
    },
)
@inject
async def generate_candidates_report(
    candidate_services: CandidateServices = Depends(
        Provide[DIContainer.candidate_services]
    ),
):
    csv_file = await candidate_services.generate_csv_file_with_all_candidates()
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"},
    )
