"""A module for User data repository."""
from core.common_repos import AbstractRepo
from users.models import User


class UserRepo(AbstractRepo):
    """Data layer class to interact with User model."""

    def __init__(self) -> None:
        """Class constructor."""
        super().__init__(User)
