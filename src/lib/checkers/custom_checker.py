from lib.checkers.base import *
from pathlib import Path
from uuid import uuid4


class CustomChecker(Checker):
    """Test whether the token list of `answer` and `output` is the same."""

    def __init__(self, checker_path: Path) -> None:
        if checker_path is not None:
            self.path = checker_path
        else:
            raise Exception("No path is provided to custom checker.")

    def check(self, input: str, output: str, answer: str) -> CheckerResult:
        """
        Check result using external checker in `checker_path`. \\
        Pass `input`, `output` and `answer` to checker's `stdin` sequentially and seperated using UUIDs 
        in the `--delimiter<1,2,3>=uuid` format; therefore the C++ checker or one of its included libraries
        must implement a function that decodes its `stdin` back to the three aforementioned streams. \\
        Checker's `stdout` and `stderr` are captured and combined into the resulting `CheckerResult`'s comment.
        """
        # TODO: implement this
        pass
