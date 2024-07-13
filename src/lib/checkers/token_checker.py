from lib.checkers.base import *


class TokenChecker(Checker):
    """Test whether the token list of `answer` and `output` is the same."""

    def __init__(self) -> None:
        pass

    def check(self, input: str, output: str, answer: str) -> CheckerResult:
        answer_tokens = answer.split()
        output_tokens = output.split()

        if len(answer_tokens) != len(output_tokens):
            return CheckerResult(
                False,
                "The answer contains %d tokens while the contestant's output contains %d tokens."
                % (len(answer_tokens), len(output_tokens)),
                input,
                output,
                answer,
            )

        for i in range(0, len(answer_tokens)):
            if answer_tokens[i] != output_tokens[i]:
                return CheckerResult(
                    False,
                    "%s token is different: contestant's output has '%s', answer has '%s'."
                    % (ordinal(i + 1), answer_tokens[i], output_tokens[i]),
                    input,
                    output,
                    answer,
                )

        return CheckerResult(
            True, "%d token(s) all matches." % len(answer_tokens), input, output, answer
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
