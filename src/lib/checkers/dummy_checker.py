from lib.checkers.base import *


class DummyChecker(Checker):
    """Does no evaluation and returns all data as-is."""

    def __init__(self) -> None:
        pass

    def check(
        self, testdata: str, answer: str, contestant_output: str
    ) -> CheckerResult:
        return CheckerResult(
            True, "All seems well.", testdata, answer, contestant_output
        )
