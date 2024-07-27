"""A module that has the routes to interact with User model."""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from DIContainer import DIContainer
from users.schemas import UserIn, UserOut
from users.services import UserServices

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user: UserIn,
    user_services: UserServices = Depends(Provide[DIContainer.user_services]),
):
    """### Create User instance in the database."""
    return await user_services.create(user)
