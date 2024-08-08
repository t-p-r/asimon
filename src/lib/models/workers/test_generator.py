from pathlib import Path
from .proc import ProcessResult, anal_process


class TestGenerator:
    """Umbrella class for generating test data."""

    def __init__(self, timeout: int = 5) -> None:
        self.timeout = timeout
        pass

    def generate(
        self,
        testgen_command,
        judge_command: Path,
        export_input_to: Path,
        export_answer_to: Path,
    ) -> None:
        """Generate a test case."""
        input_file = open(export_input_to, "w")
        output_file = open(export_answer_to, "w")
        anal_process(testgen_command, identity="test generator", stdout=input_file, timeout=self.timeout)

        # `input_file` must be reopen because even if its open mode is set to be w+,
        # the next run() command wouldn't be able to fetch any data from it.
        input_file.close()
        input_file = open(export_input_to, "r")
        anal_process(
            judge_command,
            identity="main correct solution",
            stdin=input_file,
            stdout=output_file,
            timeout=self.timeout,
        )

        input_file.close()
        output_file.close()
