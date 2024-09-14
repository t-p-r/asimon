from .base import *


class LineChecker(Checker):
    """Divide `answer` and `output` into lines. Ignore empty lines in both."""

    def __str__():
        return "line"

    @staticmethod
    def ordinal(n: int) -> str:
        """
        Returns `n` in ordinal form.
        Source: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement.
        """
        if 11 <= (n % 100) <= 13:
            suffix = "th"
        else:
            suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
        return str(n) + suffix

    def check(self, input: bytes, answer: bytes, output: bytes) -> CheckerResult:
        answer_tokens = answer.splitlines()
        output_tokens = output.splitlines()

        lanswer = len(answer_tokens)
        loutput = len(output_tokens)
        answer_lines = []
        output_lines = []

        for i in range(lanswer):
            if not answer_tokens[i].isspace():
                answer_lines.append(i)

        for j in range(loutput):
            if not output_tokens[j].isspace():
                output_lines.append(j)

        if len(answer_lines) != len(output_lines):
            return CheckerResult(
                status=ContestantExecutionStatus.WA,
                comment="The answer contains %d non-empty lines while the contestant's output contains %d non-empty lines."
                % (len(answer_lines), len(output_lines)),
            )

        llines = len(answer_lines)
        for i in range(llines):
            if answer_tokens[answer_lines[i]] != output_tokens[output_lines[i]]:
                return CheckerResult(
                    status=ContestantExecutionStatus.WA,
                    comment=f"{self.ordinal(i + 1)} line is different.",
                )

        return CheckerResult(
            status=ContestantExecutionStatus.AC,
            comment=f"{llines} line(s) all match.",
        )
