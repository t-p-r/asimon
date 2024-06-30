from lib.evaluators.base import *


class DummyEvaluator(Evaluator):
    """Does no evaluation and returns all data as-is."""

    def __init__(self) -> None:
        pass

    def evaluate(
        self, testdata: str, answer: str, contestant_output: str
    ) -> EvaluatorResult:
        return EvaluatorResult(
            True, "All seems well.", testdata, answer, contestant_output
        )
