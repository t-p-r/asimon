from .base import *


class DummyChecker(Checker):
    """Does no evaluation and returns all data as-is."""

    def __init__(self) -> None:
        pass

    def check(self, input: str, answer: str, output: str) -> CheckerResult:
        return CheckerResult(
            status=ContestantResultStatus.AC,
            comment="All seems well.",
            # input=input,
            # answer=answer,
            # output=output,
        )
