from lib.checkers.base import *


class DummyChecker(Checker):
    """Does no evaluation and returns all data as-is."""

    def __init__(self) -> None:
        pass

    def check(self, input: str, output: str, answer: str) -> CheckerResult:
        return CheckerResult(True, "All seems well.", input, output, answer)
