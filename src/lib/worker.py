"""
Worker for running tests.
"""

from subprocess import run, PIPE
from pathlib import Path
from lib.checkers import *


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

    # def handle(command:str | list[str], input, encoding, stdin=PIPE,stdout=PIPE):


    def evaluate_test(
        self,
        testgen_command: str | list[str],
        judge_command: str,
        contestant_command: str | None,
    ) -> CheckerResult:
        """
        Perform a test case.
        """
        testdata = run(testgen_command, stdout=PIPE, encoding="UTF-8").stdout
        answer = run(
            judge_command, input=testdata, stdout=PIPE, encoding="UTF-8"
        ).stdout

        # this is optional e.g. `testgen.py` only needs `judge.cpp`
        if contestant_command != None:
            contestant_output = run(
                contestant_command, input=testdata, stdout=PIPE, encoding="UTF-8"
            ).stdout
        else:
            contestant_output = ""

        return self.checker.check(testdata, answer, contestant_output)

    def generate_test(
        self,
        testgen_command: str,
        judge_command: str,
        export_testdata_at: Path,
        export_answer_at: Path,
    ) -> bool:
        """Generate a test case."""

        with open(export_testdata_at, "wb") as testdata_output:
            # I could have achieved a much more efficient piping scheme than this fuckery
            # (will become very apparent for large IO sets),
            # but both run and Popen refused to coorporate, so I gave up.
            # P/S : this doesn't even matter for some eldritch reasons.
            testdata = run(testgen_command, stdout=PIPE).stdout
            testdata_output.write(testdata)

            with open(export_answer_at, "wb") as answer_output:
                answer = run(judge_command, input=testdata, stdout=PIPE).stdout
                answer_output.write(answer)

            return True
