"""
src/create_problem.py - Generate problem (create tests from workspace files and bundle them into a folder).
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import sys

sys.dont_write_bytecode = True  # disables the creation of __pycache__ folders

from concurrent.futures import ProcessPoolExecutor
import os
import shutil
import random
import re
import json

from lib.exceptions import InvalidConfig

from lib.models.compiler import Compiler
from lib.models.workers.test_generator import TestGenerator
from lib.models.problem import Problem

from lib.utils.formatting import (
    send_message,
    script_split,
    text_colors,
    wrap_message,
)
from lib.utils.system import find_file_with_name, get_dir, terminate

from lib.config.paths import *
import config_create_problem as config


class ProblemCreator:
    def __init__(self):
        self.source_paths: list[Path] = [workspace / config.main_correct_solution]
        self.generators: list[TestGenerator] = []
        self.total_test_count = 0
        self.subtask_count = 0
        self.current_problem = Problem(problems_dir / config.problem_name)
        self.subtasks = []
        self.cumulative = 0
        self.compiler = Compiler(config.compilation_command)

        for _ in range(config.cpu_workers):
            self.generators.append(TestGenerator(timeout=config.time_limit))

    def format_subtasks(self):
        """Format subtasks into [list of commands]"""
        for subtask in config.subtasks:
            if isinstance(subtask, str):  # a single command
                self.subtasks.append([subtask])
            elif isinstance(subtask, list):  # list[str] containing commands
                for script in subtask:
                    if not isinstance(script, str):
                        raise InvalidConfig("subtasks")
                self.subtasks.append(subtask)
            elif isinstance(subtask, tuple):  # tuple(int, str):
                if isinstance(subtask[0], int) and isinstance(subtask[1], str):
                    self.subtasks.append([subtask[1]] * subtask[0])
                else:
                    raise InvalidConfig("subtasks")
            else:
                raise InvalidConfig("subtasks")

    def detect_generators(self):
        self.subtask_count = len(self.subtasks)
        self.total_test_count = sum(len(subtask) for subtask in self.subtasks)

        listgen = set()
        for subtask in self.subtasks:
            for script in subtask:
                bin = script_split(script)[0]
                listgen.add(bin)  # first word of script is always the executable

        send_message(
            "Test generators detected in subtask scripts:",
            text_colors.CYAN,
            " ",
        )
        for gen in listgen:
            send_message(gen, text_colors.PURPLE, " ")
        print("")

        for gen in listgen:
            self.source_paths.append(find_file_with_name(gen, workspace))

    def append_testlib_seeds(self):
        """Append seed per `testlib_persistent`."""
        if config.testlib_seed == "none":
            return

        for subtask in self.subtasks:
            for idx in range(len(subtask)):
                if config.testlib_seed == "from0":
                    seed = idx
                elif config.testlib_seed == "random":
                    seed = random.getrandbits(31)  # limit of C++'s 32-bit signed ints
                else:
                    raise InvalidConfig("testlib_persistent")
                subtask[idx] += f" --seed {seed}"

    def create_problem(self):
        def check_existence():
            if self.current_problem.exists():
                print(
                    f'A problem with the current name "{config.problem_name}" already existed.\n'
                    + 'Enter a selection:'
                )
                print("    1: Override the existing problem.")
                print("    2: Rename the current problem.")

                choice = input()
                if choice == "1":
                    shutil.rmtree(self.current_problem.problem_dir)
                elif choice == "2":
                    print("Enter new name:", end=" ")
                    config.problem_name = input()
                    self.current_problem = Problem(problems_dir / config.problem_name)
                    if self.current_problem.exists():
                        terminate("Fatal error: Problem already existed.")
                else:
                    terminate("Fatal error: Invalid choice, aborting...")

        check_existence()
        self.current_problem.create()

        copied = set()
        # testgens and main solution
        for source_path in self.source_paths:
            destination = (
                self.current_problem.solution_dir
                if source_path.name == config.main_correct_solution
                else self.current_problem.testgen_dir
            )
            shutil.copy(source_path, destination)
            copied.add(source_path.name)

        # other solutions
        for other_solution in config.other_solutions:
            shutil.copy(workspace / other_solution, self.current_problem.solution_other_dir)
            copied.add(other_solution)

        # checker
        if config.custom_checker:
            shutil.copy(
                workspace / config.custom_checker,
                self.current_problem.checker_dir,
            )
            copied.add(config.custom_checker)

        # other files in /workspace
        filenames = list(workspace.walk())[0][2]
        for source_path in filenames:
            if source_path not in copied:
                shutil.copy(workspace / source_path, self.current_problem.misc_dir)

        shutil.copy(
            rootdir / "config_create_problem.py",
            self.current_problem.problem_dir,
        )

        with open(self.current_problem.test_dir / "script.json", "w") as json_script:
            json_script.write(json.dumps(self.subtasks, indent=4))

    def get_testcase_dir(self, test_index: int, subtask: int) -> Path:
        testdir = config.testdir_format
        testdir = re.sub("%C", str(self.cumulative + test_index + 1), testdir)
        testdir = re.sub("%S", str(subtask + 1), testdir)
        testdir = re.sub("%T", str(test_index + 1), testdir)
        testcase_dir = self.current_problem.test_dir / testdir
        testcase_dir.mkdir()
        return testcase_dir

    def generate_test(self, worker_pool: ProcessPoolExecutor, test_index: int, subtask: int):
        """Submit a test task to a worker pool."""
        testdir = self.get_testcase_dir(test_index, subtask)
        testgen, testgen_args = script_split(self.subtasks[subtask][test_index])
        testgen = find_file_with_name(testgen, workspace)

        worker_pool.submit(
            self.generators[(test_index - 1) % config.cpu_workers].generate,
            testgen_command=[bindir / testgen.name] + testgen_args,
            judge_command=bindir / config.main_correct_solution,
            export_input_to=testdir / f"{config.problem_name}.inp",
            export_answer_to=testdir / f"{config.problem_name}.out",
        )

    def generate_subtask(self, subtask: int):
        print(f"Generating subtask {wrap_message(str(subtask + 1), text_colors.GREEN)}:")
        test_count = len(self.subtasks[subtask])
        batch_count = test_count // config.cpu_workers
        if test_count % config.cpu_workers != 0:
            batch_count += 1

        with ProcessPoolExecutor(max_workers=config.cpu_workers) as worker_pool:
            for batch in range(batch_count):
                first_test_of_batch = batch * config.cpu_workers
                last_test_of_batch = min(first_test_of_batch + config.cpu_workers, test_count) - 1
                send_message(
                    f"Executing batch {batch + 1} (test {first_test_of_batch + 1} - {last_test_of_batch + 1})",
                    text_colors.BOLD,
                )

                for test_index in range(first_test_of_batch, last_test_of_batch + 1):
                    self.generate_test(worker_pool, test_index, subtask)

    def generate_tests(self):
        print(
            "\nGenerator will generate %s subtasks for a total of %s tests:"
            % (
                wrap_message(str(self.subtask_count), text_colors.GREEN),
                wrap_message(str(self.total_test_count), text_colors.CYAN),
            )
        )  # long string, py2 format fits better

        for subtask in range(self.subtask_count):
            self.generate_subtask(subtask)
            self.cumulative += len(self.subtasks[subtask])

    def do_compress(self):
        if config.bundle_source:
            source_dir = get_dir(self.current_problem.test_dir / "problem_source")
            folders = list(self.current_problem.problem_dir.walk())[0][1]
            # testgen, solution, checker, misc
            for folder in folders:
                if folder != self.current_problem.test_dir.name:  # prevents infinite recursion
                    shutil.copytree(
                        self.current_problem.problem_dir / folder,
                        source_dir / folder,
                    )
            shutil.copy(rootdir / "config_create_problem.py", source_dir)

        send_message("\nNow compressing:", text_colors.YELLOW)
        os.chdir(self.current_problem.test_dir)
        shutil.make_archive(base_name=config.problem_name, format="zip")
        shutil.rmtree(source_dir)

    def organize_test_folder(self):
        if config.make_zip:
            self.do_compress()

        if not config.make_test_folders:
            folders = list(self.current_problem.test_dir.walk())[0][1]
            for folder in folders:
                shutil.rmtree(self.current_problem.test_dir / folder)

    def __call__(self):
        self.format_subtasks()
        self.detect_generators()
        self.append_testlib_seeds()
        self.create_problem()
        self.compiler([(source, (bindir / source.name)) for source in self.source_paths])
        self.generate_tests()
        self.organize_test_folder()
        send_message(
            f"\nGeneration completed successfully. The problem can be found at: {self.current_problem.problem_dir}",
            text_colors.CYAN,
        )


if __name__ == "__main__":
    ProblemCreator()()
