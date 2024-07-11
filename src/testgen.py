""" 
src/testgen.py - Generate tests.

This tool will repeat the following process:
    1. Use the commands stated in `subtask_script` to generate input
    2. Use "judge.cpp" to generate outputs
    3. Transfer them to "/tests/<platform_>/task_name"
    4. (Optional) Compress them into "/tests/<platform_>/task_name.zip"
"""

# USER PARAMETERS ------------------------------------------------------------------------------------------

task_name = "abc"
"""Name of the problem."""

generation_mode = "replace"
"""
Generation mode. Affect only the current problem. Must be one of:
    - "add" to add new tests while leaving old tests untouched;
    - "replace" to delete old tests before generating tests.
"""

platform = "vnoj"
"""
Target platform. For now only "vnoj" is supported.
"""

bundle_source = True
"""Whether to include test generation and solution files in the test folder."""

subtask_test_count = [60]
"""Number of tests for each subtasks."""

subtask_script = ["testgen -1000 1000"]
"""
Script used to generate tests for each subtasks.
Additional arguments, if any, must be configured by the user.
"""

worker_count = 4
"""
The number of workers (i.e. tests to be executed at the same time). \\
Since each CPU thread can only be occupied by one worker at a time, for best performance, this number should not exceed your CPU's thread count.
For IO-intensive problem, it's recommended to leave the number at 1.
"""

compress = True
"""
Whether to compress the test folder into a .zip file.
"""

compiler = "g++"

compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20"]
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have precompiled headers (e.g. `stdc++.h`), use the exact arguments you compiled them with to save time
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import shutil
from lib.asimon_shared import *
from datetime import datetime

bin_list = ["judge"]
workers = [Worker("dummy")] * worker_count


def detect_generators():
    listgen = set()
    for script in subtask_script:
        bin = script_split(script)[0]  # first word of script is always the executable
        listgen.add(bin)

    send_message(
        "Test generators detected in subtask scripts:",
        text_colors.OK_CYAN,
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
        % (wrap_message(str(subtask_index), text_colors.OK_GREEN),)
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
                % (batch, first_test_of_batch, last_test_of_batch),
                text_colors.BOLD,
            )
            
            for test_index in range(first_test_of_batch, last_test_of_batch + 1):
                testcase_dir = problem_test_dir / (
                    "%s-%s-%s"
                    % (
                        "sub" + str(subtask_index),
                        "test" + str(test_index),
                        datetime.now().strftime("%Y%m%d_%H%M%S"),
                    )
                )
                testcase_dir.mkdir()

                # Multithread variant, which somehow suppresses errors:
                perform_test_batch(
                    worker_pool=worker_pool,
                    worker_fns=[workers[(test_index - 1) % worker_count].generate_test],
                    testgen_command=[bindir / testgen_bin] + testgen_args,
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
    total_test_count = sum(subtask_test_count)
    subtask_count = len(subtask_test_count)
    platform_test_dir = universal_testdir / platform
    problem_test_dir = platform_test_dir / task_name

    if generation_mode == "replace":
        delete_folder(problem_test_dir)
        delete_file(platform_test_dir / ("%s.zip" % task_name))

    get_dir(problem_test_dir)

    if bundle_source == True:
        for bin in bin_list:
            shutil.copyfile(
                "%s/%s.cpp" % (rootdir, bin), "%s/%s.cpp" % (problem_test_dir, bin)
            )

    print(
        "\nGenerator will generate %s subtasks for a total of %s tests:"
        % (
            wrap_message(str(subtask_count), text_colors.OK_GREEN),
            wrap_message(str(total_test_count), text_colors.OK_CYAN),
        )
    )
    for subtask_index in range(0, subtask_count):
        generate_test(subtask_index, problem_test_dir)


def do_compress():
    send_message("\nNow compressing:", text_colors.YELLOW)
    os.chdir(universal_testdir / "vnoj")
    subprocess.run(["zip", "-r", ("%s.zip" % task_name), "."])


if __name__ == "__main__":
    user_argument_check()
    detect_generators()
    compile_source_codes(compiler, compiler_args, bin_list)
    generate_tests()
    if compress == True:
        do_compress()
    send_message("\nGeneration completed succesfully.", text_colors.OK_CYAN)
