from .base import *


class DummyChecker(Checker):
    """
    Does no evaluation and returns all data as-is.
    This class serves as a template for user-created checkers.
    """

    def __init__(self) -> None:
        pass

    def check(self, input: str, answer: str, output: str) -> CheckerResult:
        return CheckerResult(
            status=ContestantExecutionStatus.AC,
            comment="All seems well.",
        )
