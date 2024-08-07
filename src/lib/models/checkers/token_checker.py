from .base import *


__all__ = ["TokenChecker"]


class TokenChecker(Checker):
    """Test whether the token list of `answer` and `output` is the same."""

    def __init__(self) -> None:
        pass

    def check(self, input: str, answer: str, output: str) -> CheckerResult:
        answer_tokens = answer.split()
        output_tokens = output.split()

        if len(answer_tokens) != len(output_tokens):
            return CheckerResult(
                status=ContestantResultStatus.WA,
                comment="The answer contains %d tokens while the contestant's output contains %d tokens."
                % (len(answer_tokens), len(output_tokens)),
                # input=input,
                # answer=answer,
                # output=output,
            )

        for i in range(0, len(answer_tokens)):
            if answer_tokens[i] != output_tokens[i]:
                return CheckerResult(
                    status=ContestantResultStatus.WA,
                    comment="%s token is different: answer is: '%s', contestant outputs: '%s'."
                    % (ordinal(i + 1), answer_tokens[i], output_tokens[i]),
                    # input=input,
                    # answer=answer,
                    # output=output,
                )

        return CheckerResult(
            status=ContestantResultStatus.AC,
            comment="%d token(s) all matches." % len(answer_tokens),
            # input=input,
            # answer=answer,
            # output=output,
        )


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
