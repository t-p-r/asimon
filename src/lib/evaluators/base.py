""" 
Evaluator abstract class and EvaluatorResult
"""

from abc import ABC, abstractmethod
from collections import namedtuple

EvaluatorResult = namedtuple(
    "EvaluatorResult",
    ["status", "comment", "testdata", "answer", "contestant_output"],
)
"""The result of the evaluation process."""


class Evaluator(ABC):
    def __init__(self, policy: str) -> None:
        pass

    @abstractmethod
    def evaluate(
        self, testdata: str, answer: str, contestant_output: str
    ) -> EvaluatorResult:
        """Evaluate the test. Returns an `EvaluatorResult`, being one of:
        - `(True,  comment, testdata, answer, contestant_output)` if the evaluating process is succesful;
        - `(False, comment, testdata)` if the evaluator policy is "custom";
        - `(False, comment, testdata, answer, contestant_output)` for any other policy.
        See concrete `Evaluator` classes for the specific comments.
        """
        pass
