from lib.checkers.base import *


class TokenChecker(Checker):
    """Test whether the token list of `answer` and `contestant_output` is the same."""

    def __init__(self) -> None:
        pass

    def check(
        self, testdata: str, answer: str, contestant_output: str
    ) -> CheckerResult:
        answer_tokens = answer.split()
        contestant_tokens = contestant_output.split()

        if len(answer_tokens) != len(contestant_tokens):
            return CheckerResult(
                False,
                "The answer contains %d tokens while the contestant's output contains %d tokens."
                % (len(answer_tokens), len(contestant_tokens)),
                testdata,
                answer,
                contestant_output,
            )

        for i in range(0, len(answer_tokens)):
            if answer_tokens[i] != contestant_tokens[i]:
                return CheckerResult(
                    False,
                    "%s token is different: answer has '%s', contestant's output has '%s'."
                    % (ordinal(i+1), answer_tokens[i], contestant_tokens[i]),
                    testdata,
                    answer,
                    contestant_output,
                )

        return CheckerResult(
            True, testdata, "All token matches.", answer, contestant_output
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
