# Fuzz testing by:
#   1. Using "testgen.cpp" to generate tests.
#   2. Using "judge.cpp" and "contestant.cpp" to run these tests and compare their outputs, where "judge.cpp" is the reference program.

# Stop either when the desired number of tests have been run, or if there is a difference between the outputs of "judge.cpp" and "contestant.cpp", in which case the test and both outputs shall be wrote down the file "log.txt".

# The three files above must stay in the same folder as this Python file, must reads from stdin and writes to stdout (so e.g. no freopen()).

# TODO: add multiple output comparing modes including a custom checker.


# USER VARIABLES ------------------------------------------------------------------------------------------

test_generation_command_line = "testgen"
# often, just "testgen" should be enough; additional arguments (those passed to argv[]) can be customized.

number_of_tests = 16
# what you think it is

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
# note that some arguments are specific to either Unix or Windows (e.g. "-Wl,--stack=<desired_stack_size>")


# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import filecmp
import lib.asimon_utils as asutils
from lib.asimon_base import *

# not in lib file (for easier understanding)
PASS_ALL = 1
PASS_NONE = 0

master_dir = os.path.dirname(__file__)
log_output_stream = open(master_dir + "/log.txt", "w")

input_dump = master_dir + "/dump/input.txt"
contestant_output = master_dir + "/dump/output_contestant.txt"
judge_output = master_dir + "/dump/output_judge.txt"

exec_list = ["testgen", "judge", "contestant"]


def perform_test():
    os.system(
        "%s > %s" % (master_dir + "/dump/" + test_generation_command_line, input_dump)
    )
    os.system(
        "%s < %s > %s"
        % (master_dir + "/dump/contestant", input_dump, contestant_output)
    )
    os.system("%s < %s > %s" % (master_dir + "/dump/judge", input_dump, judge_output))


def perform_tests(iterations):
    passed_tests = 0
    for i in range(1, iterations + 1):
        asutils.send_message("Executing test: %d" % i, asutils.text_colors.BOLD)
        perform_test()

        if filecmp.cmp(contestant_output, judge_output) == False:
            log_output_stream.write("Test %d of %d: \n" % (i, iterations))
            log_output_stream.write("Input:\n%s \n" % open(input_dump, "r").read())
            log_output_stream.write(
                "Contestant's output:\n%s \n" % open(contestant_output, "r").read()
            )
            log_output_stream.write(
                "Judge's output:\n%s \n\n" % open(judge_output, "r").read()
            )
            asutils.send_message(
                "Disparity found, aborting execution...",
                asutils.text_colors.RED + asutils.text_colors.BOLD,
            )
            break

        passed_tests += 1

    print_final_verdict(passed_tests)


def print_final_verdict(passed_tests):
    percentage = passed_tests / number_of_tests
    message = (
        "Progress: %d/%d (%s"
        % (
            passed_tests,
            number_of_tests,
            100.0 * passed_tests / number_of_tests,
        )
        + " %)"
    )

    if percentage == PASS_ALL:
        asutils.send_message(message, asutils.text_colors.OK_GREEN)
    elif percentage == PASS_NONE:
        asutils.send_message(message, asutils.text_colors.RED)
    else:
        asutils.send_message(message, asutils.text_colors.YELLOW)

    log_output_stream.write(message)


if __name__ == "__main__":
    clear_previous_run(exec_list)
    compile_source_codes(exec_list, compiler_args, master_dir)
    perform_tests(number_of_tests)
