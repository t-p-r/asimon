from pathlib import Path
from .anal_process import ProcessResult, anal_process


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
        """Generate a test case. Returns True if nothing critically awry happens."""
        with open(export_input_to, "w") as input_file:
            anal_process(
                testgen_command,
                identity="test generator",
                stdout=input_file,
                timeout=self.timeout,
            )

        with open(export_input_to, "r") as input_file, open(
            export_answer_to, "w"
        ) as output_file:
            anal_process(
                judge_command,
                identity="main correct solution",
                stdin=input_file,
                stdout=output_file,
                timeout=self.timeout,
            )
