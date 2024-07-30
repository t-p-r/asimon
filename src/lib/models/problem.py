"""Class to manage problems."""

from pathlib import Path
import os
import json
from lib.utils import text_colors, send_message


class Problem:
    def __init__(self, problem_dir: Path):
        self.problem_dir = problem_dir
        self.testdir = problem_dir / "tests"
        self.testgen_dir = problem_dir / "testgens"

        self.solution_dir = problem_dir / "solutions"
        self.solution_other_dir = self.solution_dir / "other_solutions"

    def exists(self) -> bool:
        return self.problem_dir.exists()

    def create(self):
        if self.problem_dir.exists():
            raise Exception("Problem already existed.")
        Path.mkdir(self.problem_dir, parents=True)
        for p in (self.testdir, self.testgen_dir, self.solution_dir):
            Path.mkdir(p)
        for p in (self.solution_mc_dir, self.solution_other_dir):
            Path.mkdir(p)

    def main_correct_solution(self) -> Path:
        files = []
        for _, __, filename in self.solution_dir.walk():
            files += filename

        if len(files) == 0:
            raise Exception(
                "No main correct solution found. This file may have been manually deleted."
            )
        else:
            if len(files) > 1:
                send_message(
                    "More than one main correct solution found, automatically chose the first one.\n \
                    This is not the behaviour ASIMON expected, and usually results from manual tampering of the problem directory.",
                    text_colors.YELLOW,
                )
            return self.solution_dir / files[0]

    def other_solutions(self) -> Path:
        files = []
        for _, __, filename in self.solution_other_dir.walk():
            files += self.solution_other_dir / filename
        if len(files) == 0:
            raise Warning("No solution other than the main correct one found.")
        return files

    def test_script(self) -> list:
        return []
