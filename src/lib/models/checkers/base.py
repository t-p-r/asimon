""" 
Checker abstract class and checkerResult.
"""

from abc import ABC, abstractmethod
from enum import Enum


class ContestantResultStatus(Enum):
    """
    Represents the correctness of the contestant's solution. \\
    Note that, for `TLE` and `RTE`, the contestant's solution's output is ignored,
    and thus the Worker doesn't need to invoke the checker.
    """

    # These are from ContestantResultStatus:
    AC = 0  # The output is correct, follows the output format and represents an optimal answer (if applicable in this problem).
    WA = 1  # The output is wrong or incorrect.
    PE = 2  # The output doesn't follow output format specification of the task. Possible deprecation in the future.
    FAIL = 3  # Critical internal error from checker, requires investigation from judge.
    DIRT = 4  # No idea what this is.
    POINTS = 5  # Partial point awarded (not yet supported).
    UNEXPECTED_EOF = 8
    PARTIALLY = 16

    # These are special cases, where:
    TLE = 400  # Contestant's solution timed out ...
    MLE = 402  # ... or used too much memory (not yet supported).
    RTE = 401  # ... or exited with an error code ...

    def __str__(self) -> str:
        CES_to_string = {
            self.AC: "accepted",
            self.WA: "wrong answer",
            self.PE: "presentation error",
            self.FAIL: "checker failure",
            self.UNEXPECTED_EOF: "unexpected EOF found",
            self.PARTIALLY: "partial point awarded",
            self.TLE: "time limit exceeded",
            self.MLE: "memory limit exceeded",
            self.RTE: "runtime error",
        }
        return CES_to_string[self]


class CheckerResult:
    """The result of the evaluation process."""

    # def __init__(self, **kwargs) -> None:
    #     self.status = kwargs.get("status")
    #     self.comment = kwargs.get("comment")
    #     # self.input = kwargs.get("input")
    #     # self.answer = kwargs.get("answer")
    #     # self.output = kwargs.get("output")

    def __init__(self, status: ContestantResultStatus, comment: str):
        self.status = status
        self.comment = comment
        # self.input = input
        # self.answer = answer
        # self.output = output


class Checker(ABC):
    # def __init__(self, policy: str) -> None:
    #     pass

    @abstractmethod
    def check(self, input: str, answer: str, output: str) -> CheckerResult:
        """Evaluate the test result and return a `CheckerResult`.
        See concrete `checker` classes for the specific comments.
        """
        pass
