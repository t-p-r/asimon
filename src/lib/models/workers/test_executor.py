"""
Umbrella class for running tests.
"""

from subprocess import TimeoutExpired, CalledProcessError
from pathlib import Path
from lib.models.checkers import CheckerResult, Checker, DISCOVERED_CHECKERS
from lib.models.ces import ContestantExecutionStatus
from lib.utils.system import terminate_proc
from dataclasses import dataclass

from .anal_process import anal_process


@dataclass
class ContestantExecutionResult:
    """
    Result of contestant running the test. Fields are:
        - `path`: Path to the contestant's solution' executable.
        - `status`: Status of the run (AC, WA, TLE, RTE, ...)
        - `exec_time`: Execution time of contestant's solution (à la executable) in miliseconds.
        - `comment`: Comment on contestant's output from checker.
        - `output`: Contestant's output.
    """

    path: Path
    status: ContestantExecutionStatus
    exec_time: int
    comment: str
    output: bytes


@dataclass
class WorkerResult:
    """
    Result of the Worker class, returned by `perform_test()`. Fields are:
    - `input`: the test data
    - `answer`: the result from the judge
    - `contestant_results`: a list of `ContestantExecutionResult`.
    """

    input: bytes
    answer: bytes
    contestant_results: list[ContestantExecutionResult]


class TestExecutor:
    """
    Umbrella class for executing test cases. The process is usually:
    - generating test data (i.e. `input`) from a command;
    - run judge's solution using `input` as `stdin` to get `answer`, and:
    - run each contestant's solution using `input` as `stdin`, then determine the
    correctness of its `output`.

    In all cases the judge and contestants' solution are constant, and run without arguments; therefore
    their execution path can be retrieved and stored at the Worker's instantiation. The command used to
    generate test data is usually variable, and must be passed into `evaluate_test()`.
    """

    time_limit: int
    judge: Path
    contestants: list[Path]
    checker: type[Checker]  # Checker & its subclasses

    def __init__(
        self,
        judge: Path,
        contestants: list[Path],
        time_limit=5,
        checker_type="dummy",
        external_checker_path: Path | None = None,
    ):
        """Create a worker."""
        if checker_type not in DISCOVERED_CHECKERS:
            terminate_proc("Fatal error: Invalid checker type.")
        elif checker_type == "external":
            # only external checker requires an argument
            self.checker = DISCOVERED_CHECKERS[checker_type](external_checker_path)
        else:
            # other checkers (even user-created ones) have no argument mandatorily
            self.checker = DISCOVERED_CHECKERS[checker_type]()

        self.time_limit = time_limit
        self.judge = judge
        self.contestants = contestants

    def execute(self, testgen_command: str | list[str]) -> WorkerResult:
        """
        Execute a test case.
        """
        testgen_proc = anal_process(
            testgen_command, identity="test generator", timeout=self.time_limit
        )
        input = testgen_proc.stdout

        judge_proc = anal_process(
            self.judge,
            identity="main correct solution",
            input=input,
            timeout=self.time_limit,
        )
        answer = judge_proc.stdout

        worker_result = WorkerResult(input, answer, [])
        contestant_results = worker_result.contestant_results

        # This is because an upstream policy that include the judge's statistics
        # in the result report.
        if self.judge in self.contestants:
            contestant_results.append(
                ContestantExecutionResult(
                    self.judge,
                    ContestantExecutionStatus.JUDGE,
                    judge_proc.exec_time,
                    "This is the answer ordained by God.",
                    output=answer,
                )
            )
            self.contestants.remove(self.judge)

        for contestant in self.contestants:
            try:
                contestant_proc = anal_process(
                    contestant,
                    terminate_on_fault=False,
                    input=input,
                    timeout=self.time_limit,
                )
            except CalledProcessError as proc_error:  # RTE
                contestant_results.append(
                    ContestantExecutionResult(
                        contestant,
                        ContestantExecutionStatus.RTE,
                        float(proc_error.cmd),
                        "The solution terminated with code %d" % proc_error.returncode,
                    )
                )
                continue
            except TimeoutExpired:  # TLE
                contestant_results.append(
                    ContestantExecutionResult(
                        contestant,
                        ContestantExecutionStatus.TLE,
                        self.time_limit * 1000,
                        "Time limit exceeded.",
                    )
                )
                continue

            eval: CheckerResult = self.checker.check(input, answer, output=contestant_proc.stdout)
            contestant_results.append(
                ContestantExecutionResult(
                    contestant,
                    eval.status,
                    contestant_proc.exec_time,
                    eval.comment,
                    output=contestant_proc.stdout,
                )
            )

        return worker_result
