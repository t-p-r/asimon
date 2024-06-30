"""
Worker for running tests.
"""

from subprocess import run, Popen, PIPE
from pathlib import Path
from lib.evaluators import *


class Worker:
    def __init__(self, evaluator_policy: str, timeout=-1):
        if evaluator_policy == "token":
            self.evaluator = TokenEvaluator()
        elif evaluator_policy == "dummy":
            self.evaluator = DummyEvaluator()
        else:
            raise Exception("Invalid evaluator policy.")
        
        self.timeout = timeout

    def evaluate_test(
        self, testgen_command: str, judge_command: str, contestant_command: str | None
    ) -> EvaluatorResult:
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

        return self.evaluator.evaluate(testdata, answer, contestant_output)

    def generate_test(
        self,
        testgen_command: str,
        judge_command: str,
        export_testdata_at: Path,
        export_answer_at: Path,
    ) -> bool:
        """Generate a test case."""

        with open(export_testdata_at, "w+") as testdata_output:
            # I could have achieved a much more efficient piping scheme than this
            # (this will become very apparent for large IO sets),
            # but both run and Popen refused to coorporate, so I gave up.
            testdata = run(testgen_command, stdout=PIPE, encoding="UTF-8").stdout
            testdata_output.write(testdata)

            with open(export_answer_at, "w+") as answer_output:
                answer = run(
                    judge_command,
                    input=testdata,
                    stdout=PIPE,
                    encoding="UTF-8",
                ).stdout
                answer_output.write(answer)

            return True
