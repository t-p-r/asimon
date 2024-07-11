"""
Worker for running tests.
"""

from subprocess import run, PIPE
from pathlib import Path
from collections import namedtuple
from lib.checkers import *

ProcessResult = namedtuple("ProcessResult", ["runtime", "retcode", "output"])


class Worker:
    def __init__(self, checker: str, timeout=99):
        """Create a worker."""
        if checker == "token":
            self.checker = TokenChecker()
        elif checker == "dummy":
            self.checker = DummyChecker()
        else:
            raise Exception("Invalid checker name.")

        self.timeout = timeout

    def anal_process(command: str | list[str], **kwargs):
        """Run a subprocess and returns a ProcessResult representing its result."""
        pass

    def evaluate_test(
        self,
        testgen_command: str | list[str],
        judge_command: str,
        contestant_command: str | None,
    ) -> CheckerResult:
        """
        Perform a test case.
        """
        input = run(testgen_command, stdout=PIPE, encoding="UTF-8").stdout
        answer = run(judge_command, input=input, stdout=PIPE, encoding="UTF-8").stdout

        # this is optional e.g. `testgen.py` only needs `judge.cpp`
        if contestant_command != None:
            output = run(
                contestant_command, input=input, stdout=PIPE, encoding="UTF-8"
            ).stdout
        else:
            output = ""

        return self.checker.check(input, answer, output)

    def generate_test(
        self,
        testgen_command: str,
        judge_command: str,
        export_input_at: Path,
        export_answer_at: Path,
    ) -> bool:
        """Generate a test case. TODO: add timeout."""

        with open(export_input_at, "wb") as input_file:
            # I could have achieved a much more efficient piping scheme than this fuckery
            # (will become very apparent for large IO sets),
            # but both run and Popen refused to coorporate, so I gave up.
            # P/S : this doesn't even matter for some eldritch reasons.
            input = run(testgen_command, stdout=PIPE).stdout
            input_file.write(input)

            with open(export_answer_at, "wb") as answer_output:
                answer = run(judge_command, input=input, stdout=PIPE).stdout
                answer_output.write(answer)

            return True
