from enum import Enum


class ContestantExecutionStatus(Enum):
    """
    Represents the correctness of the contestant's solution.

    Note that, for `TLE` and `RTE`, the contestant's solution's output is ignored,
    and thus the Worker doesn't need to invoke the checker.
    """

    # Cases where the solution produces output, which is then checked for correctness by a checker.
    # Adopted from testlib:
    AC = 0  # The output is correct, follows the output format and represents an optimal answer (if applicable in this problem).
    WA = 1  # The output is wrong or incorrect.
    PE = 2  # The output doesn't follow output format specification of the task. Possible deprecation in the future.
    FAIL = 3  # Critical internal error from checker, requires investigation from judge.
    DIRT = 4
    POINTS = 5
    UNEXPECTED_EOF = 8
    PARTIALLY = 16  # Partial point awarded (not yet supported).
    """Codes 16-216 are partial points. Code `i` means that the solution receives `(i-16)/200` percent of point(s)."""

    JUDGE = 300  # The output is correct simply because we marked it the main correct one.

    # Cases where the solution doesn't produce meaningful output:
    TLE = 400  # Contestant's solution timed out ...
    MLE = 401  # ... or used too much memory (not yet supported) ...
    RTE = 402  # ... or exited with an error code.

    def pc(self, point: int) -> int:
        """Partial point (between 0 and 200)."""
        return self.PARTIALLY + point

    def __str__(self):
        CES_to_string = {
            self.AC: "accepted",
            self.WA: "wrong answer",
            self.PE: "presentation error",
            self.FAIL: "internal critical error: checker failure",
            self.UNEXPECTED_EOF: "unexpected end-of-file found in output",
            self.PARTIALLY: "partial point awarded",
            self.JUDGE: "main correct solution",
            self.TLE: "time limit exceeded",
            self.MLE: "memory limit exceeded",
            self.RTE: "runtime error",
        }
        return CES_to_string[self]
