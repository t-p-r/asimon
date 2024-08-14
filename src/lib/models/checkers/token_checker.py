from .base import *


class TokenChecker(Checker):
    """Test whether the token list of `answer` and `output` is the same."""

    def __str__():
        return "token"

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
        answer_tokens = answer.split()  # not much perf overhead somehow?
        output_tokens = output.split()

        if len(answer_tokens) != len(output_tokens):
            return CheckerResult(
                status=ContestantExecutionStatus.WA,
                comment="The answer contains %d tokens while the contestant's output contains %d tokens."
                % (len(answer_tokens), len(output_tokens)),
            )

        ltokens = len(answer_tokens)
        for i in range(ltokens):
            if answer_tokens[i] != output_tokens[i]:
                return CheckerResult(
                    status=ContestantExecutionStatus.WA,
                    comment="%s token is different: answer is: '%s', contestant outputs: '%s'."
                    % (self.ordinal(i + 1), answer_tokens[i], output_tokens[i]),
                )

        return CheckerResult(
            status=ContestantExecutionStatus.AC,
            comment="%d token(s) all matches." % len(answer_tokens),
        )
