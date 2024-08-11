"""
src/stress.py - Stress testing a problem's implementations.
"""

import sys

sys.dont_write_bytecode = True  # disables the creation of __pycache__ folders

import random
from concurrent.futures import ProcessPoolExecutor, Future
from tabulate import tabulate
from pathlib import Path
from io import TextIOWrapper

from lib.models.workers.test_executor import (
    TestExecutor,
    WorkerResult,
    ContestantExecutionResult,
)
from lib.models.ces import ContestantExecutionStatus
from lib.models.problem import Problem
from lib.models.compiler import Compiler

from lib.utils.formatting import send_message, script_split, write_prefix
from lib.utils.system import find_file_with_name, get_dir, delete_folder, terminate_proc
from lib.utils.numeric_aggregator import aggregate
from lib.utils.formatting import text_colors

from lib.config.paths import *
import config_stress as config


class Stresser:
    """
    To call this class, first configurates the file `config_stress.py`.
    """

    def __init__(self):
        # pair of C++ source files and its executable's location
        self.source_output: list[tuple[Path, Path]] = []
        self.workers: list[TestExecutor] = []
        self.batch_count: int = config.test_count // config.cpu_workers
        self.general_status = []
        self.exec_times = {}
        self.testgen_name_noext, self.testgen_args = script_split(config.testgen_script)

        if config.problem_name != "$workspace":
            current_problem = Problem(problems_dir / config.problem_name)
            if not current_problem.exists():
                terminate_proc(f"Fatal error: There is no problem with name {config.problem_name}.")

            # TODO: dynamic import for these:
            self.checker_pol = "token"  # stub
            self.compiler = Compiler("$default")

            # Internal (within __init__ only), temporary variables
            self._judge_path = current_problem.main_correct_solution()
            self._contestant_paths = current_problem.other_solutions()
            self._testgen_path = find_file_with_name(
                self.testgen_name_noext, current_problem.testgen_dir
            )
            if config.checker == "external":
                self._external_checker_path = None  # Path, stub
        else:
            self.checker_pol = config.checker

            self._judge_path = workspace / config.main_correct_solution
            self._contestant_paths = [workspace / solution for solution in config.other_solutions]
            self._testgen_path = find_file_with_name(self.testgen_name_noext, workspace)
            if config.checker == "external":
                self._external_checker_path = workspace / config.external_checker

            self.compiler = Compiler(config.compilation_command, config.cpu_workers)

        def _queue_compilation(p: Path):
            self.source_output.append((p, bindir / p.name))
            # .../solution.cpp -> /bin/solution.cpp.exe

        _queue_compilation(self._testgen_path)
        _queue_compilation(self._judge_path)
        for solution in self._contestant_paths:
            _queue_compilation(solution)
        if self.checker_pol == "external":
            _queue_compilation(self._external_checker_path)

        # add some more variables
        self.judge_name = self._judge_path.name
        self.testgen_name = self._testgen_path.name
        self.all_source_paths = self._contestant_paths + [self._judge_path]
        self.exec_times = {contestant.name: [] for contestant in self.all_source_paths}

        if self.checker_pol == "external":
            self.external_checker_name = self._external_checker_path.name

    def init_workers(self):
        for _ in range(config.cpu_workers):
            self.workers.append(
                TestExecutor(
                    judge=bindir / self.judge_name,
                    contestants=[bindir / contestant.name for contestant in self.all_source_paths],
                    time_limit=config.time_limit,
                    checker_pol=self.checker_pol,
                    external_checker_path=(
                        bindir / self.external_checker_name if self.checker_pol == "external" else None
                    ),
                )
            )

    def run_tests(self):
        """Run the number of tests specified by dividing them into batches \
        the size of at most `cpu_workers`."""
        if config.test_count % config.cpu_workers != 0:
            self.batch_count += 1

        with ProcessPoolExecutor(max_workers=config.cpu_workers) as worker_pool:
            batch = 0
            processed_tests = 0
            for batch_first in range(0, config.test_count, config.cpu_workers):
                if not self.workers[0].contestants or (
                    len(self.workers[0].contestants) == 1
                    and self.workers[0].contestants[0].name == config.main_correct_solution
                ):
                    send_message(
                        "All solutions have failed, aborting execution...",
                        text_colors.YELLOW,
                    )
                    break

                batch_last = min(batch_first + config.cpu_workers, config.test_count) - 1
                batch_size = batch_last - batch_first + 1
                send_message(
                    f"Executing batch {batch+1} (test {batch_first+1} - {batch_last+1})",
                    text_colors.BOLD,
                )

                procs: list[Future[WorkerResult]] = []
                for i in range(batch_size):
                    test_seed = random.getrandbits(31)
                    procs.append(
                        worker_pool.submit(
                            self.workers[i].execute,
                            [bindir / self.testgen_name]
                            + self.testgen_args
                            + [f"--seed {test_seed}"],
                        )
                    )

                for proc in procs:
                    # calling result() propagates the child process's terminate_proc() call, if any
                    test_result = proc.result()
                    processed_tests += 1
                    self.handle_test_result(test_result, test_index=processed_tests)

                batch += 1

    def handle_test_result(self, test_result: WorkerResult, test_index: int):
        for contestant_result in test_result.contestant_results:
            contestant = contestant_result.path.name
            self.exec_times[contestant].append(contestant_result.exec_time)

            if (
                contestant_result.status != ContestantExecutionStatus.AC
                and contestant_result.path in self.workers[0].contestants
            ):
                for worker in self.workers:
                    worker.contestants.remove(contestant_result.path)

                send_message(
                    f"Solution {contestant} failed ({contestant_result.status}, test {test_index})",
                    text_colors.RED,
                )
                self.general_status.append(
                    [
                        contestant,
                        f"{contestant_result.status} (test {test_index})",
                    ]
                )

                if config.failed_test_data:
                    self.log_failed_test_data(contestant, test_result, contestant_result)

    def log_failed_test_data(
        self,
        contestant: str,
        test_result: WorkerResult,
        contestant_result: ContestantExecutionResult,
    ):
        contestant_logdir = get_dir(logdir / contestant)
        with open(contestant_logdir / "status.txt", "w") as status, open(
            contestant_logdir / "input.txt", "w"
        ) as input_file, open(contestant_logdir / "answer.txt", "w") as answer, open(
            contestant_logdir / "output.txt", "w"
        ) as output:

            def write_to_log(ostream: TextIOWrapper, headline: str, content: bytes, limit=256):
                # Note: bytes are decoded back to string using UTF-8.
                status.write(headline)
                write_prefix(status, content.decode(), limit, "\n\n")
                ostream.write(content.decode())

            write_to_log(input_file, "Input:\n", test_result.input)
            write_to_log(answer, "Answer:\n", test_result.answer)
            write_to_log(output, "Output:\n", contestant_result.output)
            status.write(f"Comment:\n{contestant_result.comment}\n\n")

    def print_final_verdict(self):
        for contestant in self.workers[0].contestants:
            contestant_name = contestant.name
            self.general_status.append(
                [
                    contestant_name,
                    f"{ContestantExecutionStatus.AC} ({config.test_count} tests)",
                ]
            )
        self.general_status.sort()

        exec_time_stats = []
        for contestant, times in self.exec_times.items():
            min_time, max_time, avg_time, median_time = aggregate(times)
            exec_time_stats.append([contestant, min_time, max_time, avg_time, median_time])
        exec_time_stats.sort()

        with open(result_file_location, "w") as result_file:
            result_file.write("General status:\n\n")
            result_file.write(
                tabulate(
                    self.general_status,
                    headers=["solution", "status"],
                    tablefmt="simple",
                )
            )
            result_file.write("\n\n\nExecution time statistics:\n\n")
            result_file.write(
                tabulate(
                    exec_time_stats,
                    headers=[
                        "solution",
                        "min (ms)",
                        "max (ms)",
                        "average (ms)",
                        "median (ms)",
                    ],
                    tablefmt="simple",
                    numalign="right",
                )
            )

        send_message(
            f"Execution completed. Information about the result can be found at: {result_file_location}",
            text_colors.CYAN,
        )
        send_message("Press any key to close...", color=text_colors.BOLD, end="")
        input()

    def __call__(self):
        delete_folder(logdir)
        get_dir(logdir)
        self.compiler.compile(self.source_output)
        self.init_workers()
        self.run_tests()
        self.print_final_verdict()


if __name__ == "__main__":
    Stresser()()
