from .base import *
from pathlib import Path
from uuid import uuid4
from os import access, X_OK
from subprocess import Popen, run, PIPE, CompletedProcess
from io import BytesIO

from lib.utils.system import terminate_proc


class ExternalChecker(Checker):
    """
    Checker using an external binary file.
    """

    def __str__():
        return "external"

    def __init__(self, checker_path: Path, timeout=5) -> None:
        """
        Initialize the checker. `checker_path` is the path to the external binary checker.

        Will check for the path's executability; will terminate the entire Python interpreter
        if this check fails.
        """
        self.path = checker_path
        self.timeout = timeout

        if not access(self.path, X_OK):
            terminate_proc(
                f"Fatal error: external checker {self.path} is not an executable file."
            )

    def check(self, input: bytes, answer: bytes, output: bytes) -> CheckerResult:
        """Check result using external checker in `checker_path`.
        Pass `input`, `output` and `answer` to checker's `stdin` in the format:
        ```js
            <input>uuid1<answer>uuid2<output>
        ```

        where `uuid1` and `uuid2` are two randomly generated Version 4 UUID. This means that
        all the bytes before the first character of `uuid1` are considered `input`; the bytes between
        `uuid1` and `uuid2` are `answer`, and the bytes from after the last character of `uuid2` to EOF
        are `output`.

        The C++ checker, when executed, will be supplemented with the following arguments (in `argv[]`):
        - `--_asimon_uuid1 uuid1`
        - `--_asimon_uuid2 uuid2`

        Using these arguments, the checker or one of its included libraries must implement a function that decodes
        `stdin` back to the three aforementioned streams. An example can be seen in the ASIMON-testlib compatibility
        layer at /src/workspace/lib/testlib.h.

        Any message from the C++ checker must be passed to `stderr`; this method will not check `stdout`'s content.
        """
        uuid1 = str(uuid4())
        uuid2 = str(uuid4())

        input_buffer = b"".join(
            [
                input,
                bytearray(uuid1, "utf-8"),
                answer,
                bytearray(uuid2, "utf-8"),
                output,
            ]
        )

        proc: CompletedProcess = run(
            [
                self.path,
                "--asimon_uuid1",
                uuid1,
                "--asimon_uuid2",
                uuid2,
            ],
            input=input_buffer,
            stdout=PIPE,
            stderr=PIPE,
        )

        status = ContestantExecutionStatus(proc.returncode)
        if status == ContestantExecutionStatus.FAIL:
            terminate_proc(proc.stderr.decode())

        return CheckerResult(
            status,
            proc.stderr.decode(),  # testlib outputs its comment here
        )
