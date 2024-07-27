from candidates.models import Candidate
from core.common_repos import AbstractRepo


class CandidateRepo(AbstractRepo):
    def __init__(self) -> None:
        super().__init__(Candidate)
