"""A module for Candidate data repository."""
from candidates.models import Candidate
from core.common_repos import AbstractRepo


class CandidateRepo(AbstractRepo):
    """Data layer class to interact with Candidate model."""

    def __init__(self) -> None:
        """Class constructor."""
        super().__init__(Candidate)
