from pathlib import Path
from subprocess import run


class TestGenerator:
    """Umbrella class for generating test data."""

    def __init__(self, timeout: int = 5) -> None:
        self.timeout = timeout
        pass

    def generate_test(
        self,
        testgen_command: str | Path | list[str | Path],
        judge_command: Path,
        export_input_to: Path,
        export_answer_to: Path,
    ) -> None:
        """Generate a test case."""
        input_file = open(export_input_to, "w")
        output_file = open(export_answer_to, "w")
        run(testgen_command, stdout=input_file, timeout=self.timeout)

        # `input_file` must be reopen because even if its open mode is set to be w+,
        # the next run() command wouldn't be able to fetch any data from it.
        input_file.close()
        input_file = open(export_input_to, "r")
        run(judge_command, stdin=input_file, stdout=output_file, timeout=self.timeout)

        input_file.close()
        output_file.close()
