""" 
src/create_problem.py - Generate problem (create tests from workspace files and bundle them all into a folder).
"""

# USER PARAMETERS ------------------------------------------------------------------------------------------



# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import shutil
import random

from lib.asimon_shared import *

bin_list = ["judge"]
workers = [TestGenerator()] * worker_count

total_test_count = sum(subtask_test_count)
subtask_count = len(subtask_test_count)
problem_rootdir = universal_problems_dir / task_name
problem_testdir = problem_rootdir / "tests"


def detect_generators():
    listgen = set()
    for script in subtask_script:
        bin = script_split(script)[0]  # first word of script is always the executable
        listgen.add(bin)

    send_message(
        "Test generators detected in subtask scripts:",
        text_colors.CYAN,
        " ",
    )

    for gen in listgen:
        send_message(gen, text_colors.PURPLE, " ")
        bin_list.append(gen)
    print(" ")


def user_argument_check():
    if len(subtask_script) != len(subtask_test_count):
        raise Exception(
            wrap_message(
                "Script count is diffrent from the number of subtasks.",
                text_colors.RED,
            )
        )


def generate_test(subtask_index: int, problem_test_dir: Path):
    print(
        "Generating subtask %s:"
        % (wrap_message(str(subtask_index + 1), text_colors.GREEN))
    )

    testgen_bin, testgen_args = script_split(subtask_script[subtask_index])
    test_count = subtask_test_count[subtask_index]
    batch_count = int(test_count / worker_count)
    if test_count % worker_count != 0:
        # Cover the case where e.g. there are 9 test and 4 workers (the batches are 1-4, 5-8 and 9).
        batch_count += 1

    with ThreadPoolExecutor(max_workers=worker_count) as worker_pool:
        for batch in range(0, batch_count):
            first_test_of_batch = batch * worker_count + 1
            last_test_of_batch = min(first_test_of_batch + worker_count - 1, test_count)
            send_message(
                "Executing batch %d (test %d - %d)"
                % (batch + 1, first_test_of_batch, last_test_of_batch),
                text_colors.BOLD,
            )

            for test_index in range(first_test_of_batch, last_test_of_batch + 1):
                testcase_dir = problem_test_dir / (
                    "sub%d-test%d"
                    % (
                        subtask_index + 1,
                        test_index,
                    )
                )
                testcase_dir.mkdir()

                test_seed = test_index
                if testlib_persistent == False:
                    test_seed = random.getrandbits(31)

                # Multithread variant, which somehow suppresses errors:
                worker_pool.submit(
                    workers[(test_index - 1) % worker_count].generate_test,
                    testgen_command=[bindir / testgen_bin]
                    + testgen_args
                    + ["--testlib_seed %d" % test_seed],
                    judge_command=bindir / "judge",
                    export_input_at=problem_test_dir
                    / ("%s/%s.inp" % (testcase_dir, task_name)),
                    export_answer_at=problem_test_dir
                    / ("%s/%s.out" % (testcase_dir, task_name)),
                )

                # Non-multithread variant for debugging:
                # workers[(test_index - 1) % worker_count].generate_test(
                #     testgen_command=[bin_dir / testgen_bin] + testgen_args,
                #     judge_command=bin_dir / "judge",
                #     export_input_at=problem_test_dir
                #     / ("%s/%s.inp" % (testcase_dir, task_name)),
                #     export_answer_at=problem_test_dir
                #     / ("%s/%s.out" % (testcase_dir, task_name)),
                # )


def generate_tests():
    delete_folder(problem_testdir)
    delete_file(platform_test_dir / ("%s.zip" % task_name))
    get_dir(problem_testdir)

    if bundle_source == True:
        for bin in bin_list:
            shutil.copyfile(
                "%s/%s.cpp" % (workspace, bin), "%s/%s.cpp" % (problem_testdir, bin)
            )

    print(
        "\nGenerator will generate %s subtasks for a total of %s tests:"
        % (
            wrap_message(str(subtask_count), text_colors.GREEN),
            wrap_message(str(total_test_count), text_colors.CYAN),
        )
    )

    for subtask_index in range(0, subtask_count):
        generate_test(subtask_index, problem_testdir)


def do_compress():
    send_message("\nNow compressing:", text_colors.YELLOW)
    os.chdir(platform_test_dir)
    shutil.make_archive(base_name=task_name, format="zip", root_dir=task_name)


if __name__ == "__main__":
    user_argument_check()
    detect_generators()
    compile_source_codes(compiler, compiler_args, bin_list)
    generate_tests()
    do_compress()
    send_message(
        "\nGeneration completed succesfully. Test file can be found at: %s/%s.zip."
        % (platform_test_dir, task_name),
        text_colors.CYAN,
    )
