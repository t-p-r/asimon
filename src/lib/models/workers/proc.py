"""
Internal wrapper around subprocess's run() method.
"""

from subprocess import run, PIPE, TimeoutExpired, CalledProcessError
from dataclasses import dataclass

import time

from lib.utils.system import terminate


@dataclass
class ProcessResult:
    """
    Represents a completed process, returned by `Worker.anal_process()`.
    Do note that `exec_time` is in miliseconds.
    """

    returncode: int
    exec_time: float
    stdout: str | None


def anal_process(
    command: str | list[str],
    identity: str = "a program",
    terminate_on_fault: bool = True,
    stdout=PIPE,
    stderr=PIPE,
    encoding: str | None = "UTF-8",
    input: str | None = None,
    timeout=None,
) -> ProcessResult:
    """
    Run a subprocess and returns a ProcessResult representing its result.

    `id_string` is the user-friendly identifier of the process (e.g. "test generator", "user's solution", ...).

    If the process timed out or exited with an error code and if `terminate_on_fault` is True, attempts to terminate the entire program.

    Especially, if the process timed out and if `terminate_on_fault` is False, raise the pending TimeoutExpired error.

    Some `subprocess.run()`/`Popen()` arguments are set by default: `stdout`, `stderr`, `check`, `encoding` and `input`.
    """

    try:
        start = time.perf_counter()
        proc = run(
            command,
            stdout=stdout,
            stderr=stderr,
            encoding=encoding,
            input=input,
            timeout=timeout,
        )
        end = time.perf_counter()
    except TimeoutExpired as timeout:
        if terminate_on_fault:
            terminate(f"Fatal error: {identity} timed out after {timeout.timeout} seconds.")
        else:
            raise timeout

    if proc.returncode != 0 and terminate_on_fault:
        terminate(f"Fatal error: {identity} exited with code {proc.returncode}.")

    return ProcessResult(
        returncode=proc.returncode,
        exec_time=(end - start) * 1000,
        stdout=proc.stdout,
    )
