# Compares the output of two C++ programs: checker.cpp and contestant.cpp.
# Also, there is a program used to generate inputs: test.cpp.
# It is HIGHLY RECOMMENDED that test.cpp outputs to the file input_dump, while the other two programs both take input and output to the files input_dump and output_dump, respectively.

# This program will stop either when the desired number of tests have been run, or if there is a difference between the outputs of checker.cpp and contestant.cpp, in which case the input and both outputs shall be wrote down the file "log.txt".

# All the files above must stay in the same folder as this Python file.


# USER VARIABLES ------------------------------------------------------------------------------------------

test_generation_command_line = "./dump/testgen"
# often, just "./test" should be enough; additional arguments (i.e. those passed to argv[]) are the choice of the user

number_of_tests = 16
# what you think it is

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
# note that some arguments are specific to either Unix or Windows (e.g. "-Wl,--stack=<desired_stack_size>")


# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import filecmp
import lib.asimon_utils as asutils
from asimon_base import *

# not in lib file (for easier understanding)
PASS_ALL = 1
PASS_NONE = 0

log_output_stream = open("log.txt", "w")
input_dump = "./dump/input.txt"
contestant_output = "./dump/output_contestant.txt"
judge_output = "./dump/output_judge.txt"

exec_list = ["testgen", "judge", "contestant"]


def perform_test():
    os.system("%s > %s" % (test_generation_command_line, input_dump))
    os.system("%s < %s > %s" % ("./dump/contestant", input_dump, contestant_output))
    os.system("%s < %s > %s" % ("./dump/judge", input_dump, judge_output))


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
    compile_source_codes(exec_list, compiler_args)
    perform_tests(number_of_tests)
