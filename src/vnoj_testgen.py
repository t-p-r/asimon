""" 
src/vnoj_testgen.py - Generate tests for VNOJ by:
    1. Use the commands stated in `subtask_script` to generate input
    2. Use "judge.cpp" to generate outputs
    3. Transfer them to "/vnoj_tests/task_name"
    4. Compress them into "/vnoj_tests/task_name.zip"
"""

# USER VARIABLES ------------------------------------------------------------------------------------------

task_name = "add"
"""Name of the problem."""

generation_mode = "replace"
"""
Generation mode. Affect only the current problem. Must be one of:
    - "add" to add new tests while leaving old tests untouched;
    - "replace" to delete old tests before generating tests.
"""

subtask_test_count = [10]
"""Number of tests for each subtasks."""

subtask_script = ["testgen"]
"""
Script used to generate tests for each subtasks.
Additional arguments, if any, must be configured by the user.
"""

compiler = "g++"

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have precompiled headers (e.g. `stdc++.h`), use the exact arguments you compiled them with to save time
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import shutil
import lib.asimon_utils as asutils
from lib.asimon_base import *
from datetime import datetime

master_dir = os.path.dirname(__file__)  # .../asimon/src

input_dump = master_dir + "/dump/input.txt"
judge_output = master_dir + "/dump/output_judge.txt"

exec_list = ["judge"]


def list_generators():
    listgen = set()
    for script in subtask_script:
        first_word_end = script.find(" ")
        if first_word_end == -1:
            first_word_end = len(script)
        gen_name = script[
            0:first_word_end
        ]  # first word of string, the rest should be args
        listgen.add(gen_name)

    asutils.send_message(
        "Test generators detected in subtask scripts:",
        asutils.text_colors.OK_CYAN,
        " ",
    )
    for gen in listgen:
        asutils.send_message(gen, asutils.text_colors.PURPLE, " ")
        exec_list.append(gen)
    print()


def user_argument_check():
    if len(subtask_script) != len(subtask_test_count):
        raise Exception(
            asutils.wrap_message(
                "Script count is diffrent from the number of subtasks.",
                asutils.text_colors.RED,
            )
        )


def generate_test(subtask_index, test_index, tests_folder):
    print(
        "Generating test %s of subtask %s."
        % (
            asutils.wrap_message(str(test_index), asutils.text_colors.OK_CYAN),
            asutils.wrap_message(str(subtask_index), asutils.text_colors.OK_GREEN),
        )
    )
    os.system(
        "%s > %s" % (master_dir + "/dump/" + subtask_script[subtask_index], input_dump)
    )
    os.system("%s < %s > %s" % (master_dir + "/dump/judge", input_dump, judge_output))

    test_dir = "%s-%s-%s" % (
        tests_folder + "/" + "sub" + str(subtask_index),
        "test" + str(test_index),
        datetime.now().strftime("%Y%m%d_%H%M%S"),
    )
    os.mkdir(test_dir)
    shutil.copyfile(input_dump, "%s/%s.inp" % (test_dir, task_name))
    shutil.copyfile(judge_output, "%s/%s.out" % (test_dir, task_name))


def generate_tests():
    total_test_count = sum(subtask_test_count)
    subtask_count = len(subtask_test_count)

    tests_folder = master_dir + "/vnoj_tests/"
    if os.path.exists(tests_folder) == False:
        os.mkdir(tests_folder)

    tests_folder += task_name
    if generation_mode == "replace" and os.path.exists(tests_folder):
        shutil.rmtree(tests_folder)
        if os.path.exists(tests_folder + ".zip"):
            os.remove(tests_folder + ".zip")

    if os.path.exists(tests_folder) == False:
        os.mkdir(tests_folder)

    print(
        "\nGenerator will generate %s subtasks for a total of %s tests:"
        % (
            asutils.wrap_message(str(subtask_count), asutils.text_colors.OK_GREEN),
            asutils.wrap_message(str(total_test_count), asutils.text_colors.OK_CYAN),
        )
    )

    for subtask_index in range(0, subtask_count):
        for test_index in range(1, subtask_test_count[subtask_index] + 1):
            generate_test(subtask_index, test_index, tests_folder)


def compress():
    asutils.send_message("\nNow compressing:", asutils.text_colors.YELLOW)
    os.chdir(master_dir + "/vnoj_tests/")
    os.system("zip -r %s.zip ." % (task_name))


if __name__ == "__main__":
    user_argument_check()
    clear_previous_run(exec_list, master_dir)
    list_generators()
    compile_source_codes(exec_list, master_dir, compiler_args, compiler)
    generate_tests()
    compress()
    asutils.send_message(
        "\nGeneration completed succesfully.", asutils.text_colors.OK_CYAN
    )
