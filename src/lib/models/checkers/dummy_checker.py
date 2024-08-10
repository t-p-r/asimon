from .base import *


class DummyChecker(Checker):
    """
    Does no evaluation and returns all data as-is.
    This class serves as a template for user-created checkers.
    """

    def __str__():
        return "dummy"

    def check(self, input: bytes, answer: bytes, output: bytes) -> CheckerResult:
        return CheckerResult(
            status=ContestantExecutionStatus.AC,
            comment="All seems well.",
        )
