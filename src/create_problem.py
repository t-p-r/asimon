""" 
src/create_problem.py - Generate problem (create tests from workspace files and bundle them into a folder).
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import sys

sys.dont_write_bytecode = True  # disables the creation of __pycache__ folders

import os
import shutil
import random
import re

from lib.asimon_shared import *
from config_create_problem import *

source_files = [main_correct_solution]
generators: list[TestGenerator] = []

total_test_count = 0
subtask_count = 0

current_problem = Problem(universal_problems_dir / problem_name)
# problem_rootdir = universal_problems_dir / task_name
# problem_testdir = problem_rootdir / "tests"

problem_scripts = []
# each index is a list [subtask_scripts]


def format_subtasks():
    """Format subtasks into (count, [list of commands])"""
    for subtask in subtasks:
        if type(subtask) is str:  # a single command
            problem_scripts.append([subtask])
        elif type(subtask) is list:  # list[str] containing commands
            for script in subtask:
                if type(script) is not str:
                    raise InvalidConfig("subtasks")
            problem_scripts.append(subtask)
        elif type(subtask) is tuple:  # tuple(int, str):
            if type(subtask[0]) is int and type(subtask[1]) is str:
                problem_scripts.append([subtask[1]] * subtask[0])
            else:
                raise InvalidConfig("subtasks")
        else:
            raise InvalidConfig("subtasks")


def detect_generators():
    global subtask_count
    global total_test_count

    listgen = set()
    for subtask_scripts in problem_scripts:
        subtask_count += 1
        total_test_count += len(subtask_scripts)
        for script in subtask_scripts:
            bin = script_split(script)[0]
            # first word of script is always the executable
            listgen.add(bin)

    send_message(
        "Test generators detected in subtask scripts:",
        text_colors.CYAN,
        " ",
    )
    for gen in listgen:
        send_message(gen, text_colors.PURPLE, " ")
    print("")

    for gen in listgen:
        source_files.append(find_file_with_name(gen, workspace))


def append_testlib_seeds():
    """Append seed per `testlib_persistent`."""
    if testlib_seed == "none":
        return

    for subtask_scripts in problem_scripts:
        for idx in range(len(subtask_scripts)):
            if testlib_seed == "from0":
                seed = idx
            elif testlib_seed == "random":
                seed = random.getrandbits(31)  # limit of C++'s 32-bit signed ints
            else:
                raise InvalidConfig("testlib_persistent")
            subtask_scripts[idx] += " --seed %s" % seed


def init_generators():
    for i in range(cpu_count):
        generators.append(TestGenerator(timeout=time_limit))


def create_problem():
    if current_problem.exists():
        print("Overriding...")
        shutil.rmtree(current_problem.problem_dir)

    current_problem.create()


cumulative = 0
# number of tests processed to date


def generate_test(subtask: int):
    print(
        "Generating subtask %s:" % (wrap_message(str(subtask + 1), text_colors.GREEN))
    )
    test_count = len(problem_scripts[subtask])
    batch_count = int(test_count / cpu_count)
    if test_count % cpu_count != 0:
        # Cover the case where e.g. there are 9 test and 4 workers (the batches are 1-4, 5-8 and 9).
        batch_count += 1

    with ProcessPoolExecutor(max_workers=cpu_count) as worker_pool:
        for batch in range(0, batch_count):
            first_test_of_batch = batch * cpu_count
            last_test_of_batch = min(first_test_of_batch + cpu_count, test_count) - 1
            send_message(
                "Executing batch %d (test %d - %d)"
                % (batch + 1, first_test_of_batch + 1, last_test_of_batch + 1),
                text_colors.BOLD,
            )

            for test_index in range(first_test_of_batch, last_test_of_batch + 1):
                testdir = testdir_format
                testdir = re.sub("%C", str(cumulative + test_index), testdir)
                testdir = re.sub("%S", str(subtask), testdir)
                testdir = re.sub("%T", str(test_index), testdir)

                testcase_dir = current_problem.testdir / testdir
                testcase_dir.mkdir()

                # Multithread variant, which somehow suppresses errors:
                # worker_pool.submit(
                #     workers[(test_index - 1) % worker_count].generate_test,
                #     testgen_command=problem_scripts[subtask][test_index],
                #     judge_command=bindir / main_correct_solution,
                #     export_input_at=testcase_dir / ("%s.inp" % problem_name),
                #     export_answer_at=testcase_dir / ("%s.out" % problem_name),
                # )

                # Non-multithread variant for debugging:

                testgen_exec, testgen_args = script_split(
                    problem_scripts[subtask][test_index]
                )
                testgen_exec = find_file_with_name(testgen_exec, workspace)

                generators[(test_index - 1) % cpu_count].generate_test(
                    testgen_command=[bindir / testgen_exec] + testgen_args,
                    judge_command=bindir / main_correct_solution,
                    export_input_to=testcase_dir / ("%s.inp" % problem_name),
                    export_answer_to=testcase_dir / ("%s.out" % problem_name),
                )


def generate_tests():
    # These are to be handled in create_problem().
    # delete_folder(problem_testdir)
    # delete_file(platform_test_dir / ("%s.zip" % task_name))
    # get_dir(problem_testdir)

    # if bundle_source == True:
    #     for bin in source_files:
    #         shutil.copyfile(
    #             "%s/%s.cpp" % (workspace, bin), "%s/%s.cpp" % (problem_testdir, bin)
    #         )
    global cumulative

    print(
        "\nGenerator will generate %s subtasks for a total of %s tests:"
        % (
            wrap_message(str(subtask_count), text_colors.GREEN),
            wrap_message(str(total_test_count), text_colors.CYAN),
        )
    )

    for subtask in range(subtask_count):
        generate_test(subtask)
        cumulative += len(problem_scripts[subtask])


def do_compress():
    send_message("\nNow compressing:", text_colors.YELLOW)
    os.chdir(current_problem.testdir)
    shutil.make_archive(
        base_name=problem_name, format="zip", root_dir=current_problem.testdir
    )


if __name__ == "__main__":
    format_subtasks()
    detect_generators()
    append_testlib_seeds()
    compile_source_codes(compiler, compiler_args.split(), source_files)
    create_problem()
    init_generators()
    generate_tests()
    do_compress()
    # send_message(
    #     "\nGeneration completed succesfully. Test file can be found at: %s/%s.zip."
    #     % (platform_test_dir, task_name),
    #     text_colors.CYAN,
    # )
