"""
Umbrella class for running tests.
"""

from subprocess import run, PIPE, TimeoutExpired, CalledProcessError
from pathlib import Path
from enum import Enum
from lib.models.checkers import *
from lib.utils import text_colors, send_message
import time

__all__ = [
    "ContestantResultStatus",
    "ContestantExecutionResult",
    "WorkerResult",
    "Worker",
]


class _ProcessResult:
    """
    Represents a completed process, returned by `Worker.anal_process()`.
    Do note that `exec_time` is in miliseconds.
    """

    def __init__(self, returncode, exec_time, stdout):
        self.returncode = returncode
        self.exec_time = exec_time
        self.stdout = stdout


class ContestantExecutionResult:
    """
    Result of contestant running the test. Fields are:
        - `path` : Path to the contestant's solution' executable.
        - `status`: Status of the process.
        - `exec_time`: Execution time of contestant's solution (à la executable) in miliseconds.
        - `comment`: Comment on contestant's output from checker.
        - `output`: Contestant's output.
    """

    def __init__(
        self,
        path: Path,
        status: ContestantResultStatus,
        exec_time: int | None,
        comment: str,
        output: bytes = None,
    ):
        self.path = path
        self.status = status
        self.exec_time = exec_time
        self.comment = comment
        self.output = output


class WorkerResult:
    """Result of the Worker class, returned by `perform_test()`. Fields are:
    - `input`: the test data
    - `answer`: the result from the judge
    - `contestant_results`: a list of `ContestantExecutionResult`.
    """

    def __init__(
        self,
        input: str,
        answer: bytes,
        contestant_results: list[ContestantExecutionResult],
    ) -> None:
        self.input = input
        self.answer = answer
        self.contestant_results = contestant_results


class Worker:
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
        custom_checker_path=None,
    ):
        """Create a worker."""
        if checker == "token":
            self.checker = TokenChecker()
        elif checker == "dummy":
            self.checker = DummyChecker()
        elif checker == "custom":
            self.checker = CustomChecker(custom_checker_path)
        else:
            raise Exception("Invalid checker name.")

        self.time_limit = time_limit
        self.judge = judge
        self.contestants = contestants

    def anal_process(
        self,
        command: str | list[str],
        timeout_message: str | None = None,
        kill_message: str | None = None,
        stdout=PIPE,
        check: bool = True,
        encoding: str | None = "UTF-8",
        input: str | None = None,
    ) -> _ProcessResult:
        """
        Run a subprocess and returns a ProcessResult representing its result.
        If `kill_message` and the process exited with an error code,
        or if `timeout_message` is set and the process timed out, raise an Exception with those messages.
        Some `subprocess.run()`/`Popen()` arguments are set by default: `stdout`, `check`, `encoding` and `input`.
        """

        try:
            start = time.perf_counter()
            proc = run(
                command,
                stdout=stdout,
                check=check,
                encoding=encoding,
                input=input,
                timeout=self.time_limit,
            )
            end = time.perf_counter()
        except TimeoutExpired as timeout:
            if timeout_message != None:
                send_message(timeout_message, text_colors.YELLOW)
                exit(0)
            else:
                raise timeout
        except CalledProcessError as proc_error:
            if kill_message != None:
                send_message(kill_message, text_colors.RED)
                exit(0)
            else:
                raise proc_error

        return _ProcessResult(
            returncode=proc.returncode,
            exec_time=(end - start) * 1000,
            stdout=proc.stdout,
        )

    def perform_test(self, testgen_command: str | list[str]) -> WorkerResult:
        """
        Perform a test case.
        """

        input = self.anal_process(
            testgen_command,
            timeout_message="Critical error: test generator timed out.",
            kill_message="Critical error: test generator exited with an error code.",
        ).stdout

        answer = self.anal_process(
            self.judge,
            timeout_message="Critical error: judge's solution timed out.",
            kill_message="Critical error: judge's solution exited with an error code.",
            input=input,
        ).stdout

        worker_result = WorkerResult(input, answer, [])
        contestant_results = worker_result.contestant_results

        for contestant in self.contestants:
            try:
                contestant_proc = self.anal_process(contestant, input=input)
            except CalledProcessError as proc_error:  # RTE
                contestant_results.append(
                    ContestantExecutionResult(
                        contestant,
                        ContestantResultStatus.RTE,
                        contestant_proc.exec_time,
                        "The solution terminated with code %d" % proc_error.returncode,
                    )
                )
                continue
            except TimeoutExpired as timeout:  # TLE
                contestant_results.append(
                    ContestantExecutionResult(
                        contestant,
                        ContestantResultStatus.TLE,
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
