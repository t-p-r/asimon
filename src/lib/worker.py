"""
Worker for running tests.
"""

from subprocess import run, PIPE
from pathlib import Path
from collections import namedtuple
from lib.checkers import *

ProcessResult = namedtuple("ProcessResult", ["runtime", "retcode", "output"])


class Worker:
    def __init__(self, checker: str, timeout=5):
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

        # this is optional e.g. testgen.py only needs judge's code to run
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
        input_file = open(export_input_at, "w")
        output_file = open(export_answer_at, "w")

        run(testgen_command, stdout=input_file)
        # These two lines exists because even if input_file's open mode is set to be w+,
        # the second run command wouldn't be able to fetch any data from it.
        input_file.close()
        input_file = open(export_input_at, "r")

        run(judge_command, stdin=input_file, stdout=output_file)
        input_file.close()
        output_file.close()
        return True
