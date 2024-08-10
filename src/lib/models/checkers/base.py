""" 
Checker abstract class and CheckerResult.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from lib.models.ces import ContestantExecutionStatus


@dataclass
class CheckerResult:
    """The result of the evaluation process."""

    status: ContestantExecutionStatus
    comment: str


class Checker(ABC):
    @abstractmethod
    def check(self, input: bytes, answer: bytes, output: bytes) -> CheckerResult:
        """Evaluate the test result and return a `CheckerResult`.
        See concrete `checker` classes for the specific comments.
        """
        pass
