"""
Internal wrapper around subprocess's run() method.
"""

from subprocess import run, PIPE, TimeoutExpired, CompletedProcess, CalledProcessError
from dataclasses import dataclass

import time

from lib.utils.system import terminate_proc


@dataclass
class ProcessResult:
    """
    Represents a completed process, returned by `Worker.anal_process()`.
    Do note that `exec_time` is in miliseconds.
    """

    returncode: int
    exec_time: float
    stdout: bytes | None


def anal_process(
    command: str | list[str],
    identity: str = "a program",
    terminate_on_fault: bool = True,
    stdout=PIPE,
    stderr=PIPE,
    timeout=None,
    **other_subprocess_args,
) -> ProcessResult:
    """
    Run a subprocess and returns a ProcessResult representing its result.

    `id_string` is the user-friendly identifier of the process (e.g. "test generator", "user's solution", ...).

    If the process timed out or exited with an error code and if `terminate_on_fault` is True,
    attempts to terminate the entire Python interpreter.

    Especially, if the process timed out and if `terminate_on_fault` is False, raise the pending `TimeoutExpired` error.

    Some `subprocess.run()`/`Popen()` arguments are set by default: `stdout`, `stderr`, `encoding`.
    """

    try:
        start = time.perf_counter()
        proc: CompletedProcess = run(
            command,
            stdout=stdout,
            stderr=stderr,
            timeout=timeout,
            **other_subprocess_args,
            check=True
        )
        end = time.perf_counter()
    except CalledProcessError as proc_error:
        if terminate_on_fault:
            terminate_proc(f"Fatal error: {identity} exited with code {proc.returncode}.\nError message: {proc.stderr.decode()}")
        else:
            raise proc_error
    except TimeoutExpired as timeout_error:
        if terminate_on_fault:
            terminate_proc(f"Fatal error: {identity} timed out after {timeout} seconds.")
        else:
            raise timeout_error
        

    return ProcessResult(
        returncode=proc.returncode,
        exec_time=(end - start) * 1000,
        stdout=proc.stdout,
    )
