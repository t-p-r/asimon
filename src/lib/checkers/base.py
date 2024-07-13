""" 
checker abstract class and checkerResult
"""

from abc import ABC, abstractmethod
from collections import namedtuple

CheckerResult = namedtuple(
    "CheckerResult",
    ["status", "comment", "input", "output", "answer"],
)
"""The result of the evaluation process."""


class Checker(ABC):
    def __init__(self, policy: str) -> None:
        pass

    @abstractmethod
    def check(self, input: str, output: str, answer: str) -> CheckerResult:
        """Evaluate the test result and return a `CheckerResult`.
        See concrete `checker` classes for the specific comments.
        """
        pass
