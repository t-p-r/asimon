from .base import *
from pathlib import Path
from uuid import uuid4


class CustomChecker(Checker):
    """Test whether the token list of `answer` and `output` is the same."""

    def __init__(self, checker_path: Path) -> None:
        if checker_path is not None:
            self.path = checker_path
        else:
            raise Exception("No path is provided to custom checker.")

    def check(self, input: str, answer: str, output: str) -> CheckerResult:
        """Check result using external checker in `checker_path`.
        Pass `input`, `output` and `answer` to checker's `stdin` in the format:
        ```
            [input]
            --delimiter1=<an uuid>
            [answer]
            --delimiter2=<another uuid>
            [output]
            --delimiter3=<a different uuid>
        ```.
        The C++ checker or one of its included libraries must thus implement a function that decodes 
        `stdin` back to the three aforementioned streams. \\
        The checker's `stdout` and `stderr` are captured and combined into the resulting `CheckerResult`'s comment.
        """
        delimiter1 = uuid4()
        delimiter2 = uuid4()
        delimiter3 = uuid4()
        # TODO: implement this
