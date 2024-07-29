"""Class to manage problems."""

from pathlib import Path
import os
import json


class Problem:
    def __init__(self, problem_dir: Path) -> None:
        self.problem_dir = problem_dir
        self.testdir = problem_dir / "tests"
        self.testgen_dir = problem_dir / "testgen"
        self.solution_dir = problem_dir / "solution"

        self.solution_judge_dir = self.solution_dir / "judge"
        self.solution_contestant_dir = self.solution_dir / "contestant"
        pass

    def exists(self) -> bool:
        return self.problem_dir.exists()

    def create(self):
        if self.problem_dir.exists():
            raise Exception("Problem already existed.")
        Path.mkdir(self.problem_dir, parents=True)
        for p in (self.testdir, self.testgen_dir, self.solution_dir):
            Path.mkdir(p)
        for p in (self.solution_judge_dir, self.solution_contestant_dir):
            Path.mkdir(p)

    def judge_solution(self) -> Path:
        files = []
        for _, __, filename in self.solution_judge_dir.walk():
            files += filename

        if len(files) == 0:
            raise Exception(
                "No judge's solution found. The file may have been manually deleted."
            )
        else:
            if len(files) > 1:
                raise Warning(
                    "More than one judge's solution found, automatically chose the first one."
                )
            return self.solution_judge_dir / files[0]

    def contestant_solutions(self) -> Path:
        files = []
        for _, __, filename in self.solution_contestant_dir.walk():
            files += self.solution_contestant_dir / filename
        if len(files) == 0:
            raise Warning("No contestant's solution found.")
        return files

    def test_script(self) -> list:
        return []
