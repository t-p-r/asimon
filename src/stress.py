"""
src/stress.py - Stress testing a problem's implementations.
"""

import sys

sys.dont_write_bytecode = True  # disables the creation of __pycache__ folders

import random
from concurrent.futures import ProcessPoolExecutor, Future
from tabulate import tabulate
from pathlib import Path

from lib.models.test_worker import (
    TestWorker,
    WorkerResult,
    ContestantExecutionResult,
)
from lib.models.ces import ContestantExecutionStatus
from lib.models.problem import Problem
from lib.models.compiler import Compiler

from lib.utils.formatting import send_message, script_split, write_prefix
from lib.utils.system import find_file_with_name, get_dir, delete_folder, terminate
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
        self.workers: list[TestWorker] = []
        self.batch_count: int = config.test_count // config.cpu_workers
        self.processed_tests: int = 0
        self.general_status = []
        self.exec_times = {}
        self.testgen_path, self.testgen_args = script_split(config.testgen_script)

        if config.problem_name != "$workspace":
            current_problem = Problem(problems_dir / config.problem_name)
            if not current_problem.exists():
                terminate(f"Fatal error: There is no problem with name {config.problem_name}.")

            self.mcs_path = current_problem.main_correct_solution()
            self.others_path = current_problem.other_solutions()
            self.testgen_path = find_file_with_name(self.testgen_path, current_problem.testgen_dir)

            # TODO: dynamic import for these:
            self.checker_pol = "token"  # stub
            self.custom_checker_path = None  # Path, stub
            self.compiler = Compiler("$default")

        else:
            self.mcs_path = workspace / config.main_correct_solution
            self.others_path = [workspace / solution for solution in config.other_solutions]
            self.testgen_path = find_file_with_name(self.testgen_path, workspace)
            self.checker_pol = config.checker

            if config.checker == "custom":
                self.custom_checker_path = workspace / config.custom_checker
            self.compiler = Compiler(config.compilation_command)

        def _queue_compilation(p: Path):
            self.source_output.append((p, bindir / p.name))
            # .../solution.cpp -> /bin/solution.cpp.exe

        _queue_compilation(self.testgen_path)
        _queue_compilation(self.mcs_path)
        for solution in self.others_path:
            _queue_compilation(solution)
        if self.checker_pol == "custom":
            _queue_compilation(self.custom_checker_path)

        self.all_source_paths = self.others_path + [self.mcs_path]
        self.exec_times = {contestant.name: [] for contestant in self.all_source_paths}

    def init_workers(self):
        for _ in range(config.cpu_workers):
            self.workers.append(
                TestWorker(
                    judge=bindir / self.mcs_path.name,
                    contestants=[bindir / contestant.name for contestant in self.all_source_paths],
                    time_limit=config.time_limit,
                    checker=self.checker_pol,
                    custom_checker_path=(
                        bindir / self.custom_checker_path if self.checker_pol == "custom" else None
                    ),
                )
            )

    def run_tests(self):
        """Run the number of tests specified by dividing them into batches \
        the size of at most `worker_count`."""
        if config.test_count % config.cpu_workers != 0:
            self.batch_count += 1

        worker_pool = ProcessPoolExecutor(max_workers=config.cpu_workers)

        for batch in range(self.batch_count):
            if not self.workers[0].contestants or (
                len(self.workers[0].contestants) == 1
                and self.workers[0].contestants[0].name == config.main_correct_solution
            ):
                send_message(
                    "All solutions have failed, aborting execution...",
                    text_colors.YELLOW,
                )
                break

            first_test_of_batch = self.processed_tests + 1
            last_test_of_batch = min(self.processed_tests + config.cpu_workers, config.test_count)
            batch_size = last_test_of_batch - first_test_of_batch + 1
            send_message(
                f"Executing batch {batch+1} (test {first_test_of_batch} - {last_test_of_batch})",
                text_colors.BOLD,
            )

            procs: list[Future[WorkerResult]] = []
            for i in range(batch_size):
                test_seed = random.getrandbits(31)
                procs.append(
                    worker_pool.submit(
                        self.workers[i],
                        [bindir / self.testgen_path.name]
                        + self.testgen_args
                        + [f"--seed {test_seed}"],
                    )
                )

            for proc in procs:
                test_result = proc.result()
                test_index = self.processed_tests + 1
                self.handle_test_result(test_result, test_index)
                self.processed_tests += 1

        worker_pool.shutdown()

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

            def write_to_log(ostream, headline, content, limit=256):
                content = content or ""  # e.g. when the solution TLE
                status.write(headline)
                write_prefix(status, content, limit, "\n\n")
                ostream.write(content)

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
        self.compiler(self.source_output)
        self.init_workers()
        self.run_tests()
        self.print_final_verdict()


if __name__ == "__main__":
    Stresser()()
