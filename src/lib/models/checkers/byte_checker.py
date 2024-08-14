from .base import *


class ByteChecker(Checker):
    """
    Does no evaluation and returns all data as-is.
    This class serves as a template for user-created checkers.
    """

    def __str__():
        return "byte"

    def check(self, input: bytes, answer: bytes, output: bytes) -> CheckerResult:
        if answer == output:
            return CheckerResult(
                status=ContestantExecutionStatus.AC,
                comment="Answer and output is the exact same",
            )
        else:
            return CheckerResult(
                status=ContestantExecutionStatus.WA,
                comment="Answer and output is not the exact same",
            )
