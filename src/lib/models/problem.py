"""Class to manage problems."""

from pathlib import Path
import json
from lib.exceptions import *
from lib.utils.system import terminate_proc


class Problem:
    def __init__(self, problem_dir: Path):
        self.problem_dir        = problem_dir
        self.resource_dir       = problem_dir       / "resources"

        self.testgen_dir        = self.resource_dir / "testgen"
        self.checker_dir        = self.resource_dir / "checker"
        self.misc_dir           = self.resource_dir / "misc"
        self.solution_dir       = self.resource_dir / "solution"

        self.solution_other_dir = self.solution_dir / "other_solutions"

    def create(self):
        """This will actually initialize the problem directories on disk."""
        if self.problem_dir.exists():
            terminate_proc("Fatal error: Problem already existed.")

        Path.mkdir(self.problem_dir, parents=True)
        Path.mkdir(self.resource_dir)
        
        for p in [
            self.testgen_dir,
            self.solution_dir,
            self.checker_dir,
            self.misc_dir,
        ]:
            Path.mkdir(p)

        Path.mkdir(self.solution_other_dir)

    def exists(self) -> bool:
        """
        Returns whether the problem directory exists. Doesn't check for internal corruption.
        """
        return self.problem_dir.exists()

    def rename(self, new_name: str):
        new_problem_dir = Path(self.problem_dir.parent / new_name)
        if new_problem_dir.exists():
            terminate_proc("Fatal error: A problem with this name already exists.")

        self.problem_dir.rename(new_problem_dir)
        self.__init__(new_problem_dir)

    def main_correct_solution(self) -> Path:
        files = list(self.solution_dir.walk())[0][2]

        if len(files) == 0:
            terminate_proc(
                "Fatal error: No main correct solution found. "
                + "The file may have been manually deleted."
            )
        else:
            if len(files) > 1:
                raise YellowWarning(
                    "More than one main correct solution found, automatically chose the first one. "
                    + "This is not the behaviour ASIMON expected, and should "
                    + "result from manual tampering of the problem directory."
                )
            return self.solution_dir / files[0]

    def other_solutions(self) -> list[Path]:
        files = list(self.solution_other_dir.walk())[0][2]
        if len(files) == 0:
            raise Warning("No solution other than the main correct one is found.")
        return [self.solution_other_dir / file for file in files]

    def subtasks(self) -> list:
        return json.load(self.problem_dir / "script.json")
