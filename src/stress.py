"""
src/stress.py - Stress testing a problem's implementations.
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import sys

sys.dont_write_bytecode = True  # disables the creation of __pycache__ folders

from lib.asimon_shared import *
from config.config_stress import *
from tabulate import tabulate

testgen_source, testgen_args = script_split(testgen_script)
testgen_source = find_file_with_name(testgen_source, workspace)

if problem == "$workspace":
    source_files = [testgen_source, main_correct_solution] + other_solutions
    if checker == "custom":
        source_files.append(custom_checker)
else:
    # TODO: implement this (after create_problem.py)
    pass

workers: list[Worker] = []
batch_count = int(test_count / cpu_count)
processed_tests = 0
general_status: list[list] = []
exec_times = {contestant: [] for contestant in other_solutions}


def init_workers():
    global workers
    for i in range(cpu_count):
        workers.append(
            Worker(
                judge=bindir / main_correct_solution,
                contestants=[bindir / contestant for contestant in other_solutions],
                time_limit=time_limit,
                checker=checker,
                custom_checker_path=bindir / custom_checker,
            )
        )


def run_tests():
    """Run the number of tests specified by dividing them into batches the size of at most `worker_count`."""

    # coming from C++ these lines are stupid af
    global batch_count
    global processed_tests

    if test_count % cpu_count != 0:
        # Cover the case where e.g. there are 9 test and 4 workers (the batches are 1-4, 5-8 and 9).
        batch_count += 1

    worker_pool = ProcessPoolExecutor(max_workers=cpu_count)

    for batch in range(0, batch_count):
        if len(workers[0].contestants) == 0:
            send_message(
                "All solutions have failed, aborting execution...",
                text_colors.YELLOW,
            )
            break

        first_test_of_batch = processed_tests + 1
        last_test_of_batch = min(processed_tests + cpu_count, test_count)
        batch_size = last_test_of_batch - first_test_of_batch + 1
        send_message(
            "Executing batch %d (test %d - %d)"
            % (batch, first_test_of_batch, last_test_of_batch),
            text_colors.BOLD,
        )

        procs: list[Future] = []
        for i in range(0, batch_size):
            test_seed = random.getrandbits(31)
            procs.append(
                worker_pool.submit(
                    workers[i].perform_test,
                    [bindir / testgen_source]
                    + testgen_args
                    + ["--seed %d" % test_seed],
                )
            )

        for proc in procs:
            test_result: WorkerResult = proc.result()
            test_index = processed_tests + 1

            for contestant_result in test_result.contestant_results:
                contestant = str(contestant_result.path).removeprefix(
                    str(bindir) + PATH_DELIMITER
                )
                exec_times[contestant].append(contestant_result.exec_time)

                if (
                    contestant_result.status != ContestantResultStatus.AC
                    and contestant_result.path in workers[0].contestants
                ):
                    for worker in workers:
                        worker.contestants.remove(contestant_result.path)

                    send_message(
                        "Solution %s failed (%s, test %d)"
                        % (contestant, contestant_result.status, test_index),
                        text_colors.RED,
                    )
                    general_status.append(
                        [
                            contestant,
                            "%s (test %d)" % (contestant_result.status, test_index),
                        ]
                    )

                    if status_only == False:
                        contestant_logdir = get_dir(logdir / contestant)
                        status = open(contestant_logdir / "status.txt", "w")
                        input = open(contestant_logdir / "input.txt", "w")
                        answer = open(contestant_logdir / "answer.txt", "w")
                        output = open(contestant_logdir / "output.txt", "w")

                        def write_to_log(ostream, headline, content, limit=256):
                            if content is None:  # e.g. when the solution TLE
                                content = ""
                            status.write(headline)
                            write_prefix(status, content, limit, "\n\n")
                            ostream.write(content)

                        write_to_log(input, "Input:\n", test_result.input)
                        write_to_log(answer, "Answer:\n", test_result.answer)
                        write_to_log(output, "Output:\n", contestant_result.output)
                        status.write("Comment:\n%s\n\n" % contestant_result.comment)

                        status.close()
                        input.close()
                        output.close()
                        answer.close()

            processed_tests += 1

    worker_pool.shutdown()


def print_final_verdict():
    for contestant in workers[0].contestants:
        contestant_name = str(contestant).removeprefix(str(bindir) + PATH_DELIMITER)
        general_status.append(
            [
                contestant_name,
                "%s (%d tests)" % (ContestantResultStatus.AC, test_count),
            ]
        )
    general_status.sort()

    exec_time_stats = []
    for contestant, times in exec_times.items():
        min, max, avg, median = aggregate(times)
        exec_time_stats.append([contestant, min, max, avg, median])
    exec_time_stats.sort()

    result_file = open(result_file_location, "w+")
    result_file.write("General status:\n\n")
    result_file.write(
        tabulate(general_status, headers=["solution", "status"], tablefmt="simple")
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

    result_file.close()
    send_message(
        "Execution completed. general status can be found at: %s"
        % result_file_location,
        text_colors.CYAN,
    )
    send_message("Press any key to close...", color=text_colors.BOLD, end="")
    input()


if __name__ == "__main__":
    delete_folder(logdir)
    get_dir(logdir)
    compile_source_codes(compiler, compiler_args.split(), source_files)
    init_workers()
    run_tests()
    print_final_verdict()
