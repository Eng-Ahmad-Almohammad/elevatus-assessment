"""This module is responsible to create an instance of DIContainer.

DIContainer will include all our services and repositories
that we will inject later on to use them in our methods and functions.
"""
from dependency_injector import containers, providers

from candidates.repos import CandidateRepo
from candidates.services import CandidateServices
from users.repos import UserRepo
from users.services import UserServices


class DIContainer(containers.DeclarativeContainer):
    """Create an instance for each repository and service that we will use later on.

    In this class we are going to declare each repository and service
    then we can inject them to any function or method to use them.
    """

    user_repo = providers.Singleton(UserRepo)
    candidate_repo = providers.Singleton(CandidateRepo)
    candidate_services = providers.Singleton(
        CandidateServices,
        candidate_repo=candidate_repo,
    )
    user_services = providers.Singleton(
        UserServices,
        user_repo=user_repo,
    )
