""" 
checker abstract class and checkerResult
"""

from abc import ABC, abstractmethod
from collections import namedtuple

CheckerResult = namedtuple(
    "checkerResult",
    ["status", "comment", "testdata", "answer", "contestant_output"],
)
"""The result of the evaluation process."""


class Checker(ABC):
    def __init__(self, policy: str) -> None:
        pass

    @abstractmethod
    def check(
        self, testdata: str, answer: str, contestant_output: str
    ) -> CheckerResult:
        """Evaluate the test result. Returns an `CheckerResult`, being one of:
        - `(True,  comment, testdata, answer, contestant_output)` if the evaluating process is succesful;
        - `(False, comment, testdata)` if the checker policy is "custom";
        - `(False, comment, testdata, answer, contestant_output)` for any other policy.
        See concrete `checker` classes for the specific comments.
        """
        pass
