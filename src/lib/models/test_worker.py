"""
Umbrella class for running tests.
"""

from subprocess import run, PIPE, TimeoutExpired, CalledProcessError
from pathlib import Path
from lib.models.checkers import *
from lib.models.ces import ContestantExecutionStatus
from lib.utils.system import terminate
from lib.utils.formatting import send_message, text_colors
from dataclasses import dataclass
import time

__all__ = [
    "ContestantExecutionResult",
    "WorkerResult",
    "TestWorker",
]


@dataclass
class _ProcessResult:
    """
    Represents a completed process, returned by `Worker.anal_process()`.
    Do note that `exec_time` is in miliseconds.
    """

    returncode: int
    exec_time: float
    stdout: str


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
    exec_time: int | None
    comment: str
    output: bytes = None


@dataclass
class WorkerResult:
    """
    Result of the Worker class, returned by `perform_test()`. Fields are:
    - `input`: the test data
    - `answer`: the result from the judge
    - `contestant_results`: a list of `ContestantExecutionResult`.
    """

    input: str
    answer: bytes
    contestant_results: list[ContestantExecutionResult]


class TestWorker:
    """
    Umbrella class for executing test cases. The process is usually:
        - generating test data (i.e. `input`) from a command;
        - run judge's solution using `input` as `stdin` to get `answer`, and:
        - run each contestant's solution using `input` as stdin, then comparing the `output`
        with the judge's `answer` to determine its correctness.

    In all cases the judge and contestants' solution are constant, and run without arguments; therefore
    their execution path can be retrieved and stored at the Worker's instantiation. The command used to
    generate test data is usually variable, and must be passed into `evaluate_test()`.
    """

    time_limit: int
    judge: Path
    contestants: list[Path]

    def __init__(
        self,
        judge: Path,
        contestants: list[Path],
        time_limit=5,
        checker="dummy",
        custom_checker_path: Path | None = None,
    ):
        """Create a worker."""
        if checker == "token":
            self.checker = TokenChecker()
        elif checker == "dummy":
            self.checker = DummyChecker()
        elif checker == "custom":
            self.checker = CustomChecker(custom_checker_path)
        else:
            terminate("Fatal error: Invalid checker name.")

        self.time_limit = time_limit
        self.judge = judge
        self.contestants = contestants

    def anal_process(
        self,
        command: str | list[str],
        identity: str = "program",
        raise_error: bool = False,
        stdout=PIPE,
        stderr=PIPE,
        check: bool = True,
        encoding: str | None = "UTF-8",
        input: str | None = None,
    ) -> _ProcessResult:
        """
        Run a subprocess and returns a ProcessResult representing its result.

        `id_string` is the user-friendly identifier of the process (e.g. "test generator", "user's solution", ...).

        If the process timed out or exited with an error code, raise an Exception with messages.
        Some `subprocess.run()`/`Popen()` arguments are set by default: `stdout`, `stderr`, `check`, `encoding` and `input`.
        """

        try:
            start = time.perf_counter()
            proc = run(
                command,
                stdout=stdout,
                stderr=stderr,
                check=check,
                encoding=encoding,
                input=input,
                timeout=self.time_limit,
            )
            end = time.perf_counter()
        except TimeoutExpired as timeout:
            if raise_error:
                raise timeout
            else:
                terminate(
                    f"Fatal error: {identity} timed out after {timeout.timeout} seconds.",
                    text_colors.RED,
                )
        except CalledProcessError as proc_error:
            if raise_error:
                end = time.perf_counter()  # the `end`` above will never be reached
                proc_error.cmd = str((end - start) * 1000)
                # little cheat here: exec_time is smuggled out through error message
                raise proc_error
            else:
                terminate(
                    f"Fatal error: {identity} exited with code {proc_error.returncode}.",
                    text_colors.RED,
                )

        return _ProcessResult(
            returncode=proc.returncode,
            exec_time=(end - start) * 1000,
            stdout=proc.stdout,
        )

    def __call__(self, testgen_command: str | list[str]) -> WorkerResult:
        """
        Perform a test case.
        """

        input = self.anal_process(testgen_command, identity="test generator").stdout
        answer = self.anal_process(self.judge, identity="main correct solution", input=input).stdout

        worker_result = WorkerResult(input, answer, [])
        contestant_results = worker_result.contestant_results

        for contestant in self.contestants:
            try:
                contestant_proc = self.anal_process(contestant, raise_error=True, input=input)
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

            output = contestant_proc.stdout
            eval = self.checker.check(input, answer, output)
            contestant_results.append(
                ContestantExecutionResult(
                    contestant,
                    eval.status,
                    contestant_proc.exec_time,
                    eval.comment,
                    output,
                )
            )

        return worker_result
