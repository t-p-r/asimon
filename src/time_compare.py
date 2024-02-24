# USER VARIABLES ------------------------------------------------------------------------------------------

test_generation_command_line = "./dump/testgen"
# often, just "./test" should be enough; additional arguments (i.e. those passed to argv[]) are the choice of the user

number_of_tests = 16
# what you think it is

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
# note that some arguments are specific to either Unix or Windows (e.g. "-Wl,--stack=<desired_stack_size>")


# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import time
import lib.asimon_utils as asutils
from asimon_base import *

log_output_stream = open("log.txt", "w")
input_dump = "./dump/input.txt"
contestant_output = "./dump/output_contestant.txt"
judge_output = "./dump/output_judge.txt"

exec_list = ["testgen", "judge", "contestant"]


def running_time(command):
    start_time = time.time()
    os.system(command)
    return time.time() - start_time


def perform_tests(iterations):
    total_contestant_time = 0
    total_checker_time = 0

    for i in range(1, iterations + 1):
        asutils.send_message("Executing test:  %s" % i, asutils.text_colors.BOLD)

        os.system("%s > %s" % (test_generation_command_line, input_dump))
        contestant_test_runtime = running_time(
            "%s < %s > %s" % ("./dump/contestant", input_dump, contestant_output)
        )
        judge_test_runtime = running_time(
            "%s < %s > %s" % ("./dump/judge", input_dump, judge_output)
        )

        log_output_stream.write("Test %d:\n" % i)
        log_output_stream.write("Judge took:      %f (s)\n" % judge_test_runtime)
        log_output_stream.write("Contestant took: %f (s)\n\n" % contestant_test_runtime)

        total_contestant_time += contestant_test_runtime
        total_checker_time += judge_test_runtime

    print_final_verdict(total_contestant_time, total_checker_time)


def print_final_verdict(total_contestant_time, total_checker_time):
    asutils.send_message(
        "Judge took:      %f (s)" % total_checker_time,
        asutils.text_colors.OK_GREEN,
    )
    asutils.send_message(
        "Contestant took: %f (s)" % total_contestant_time,
        asutils.text_colors.OK_CYAN,
    )
    print("(see log.txt for details)")


if __name__ == "__main__":
    clear_previous_run(exec_list)
    compile_source_codes(exec_list, compiler_args)
    perform_tests(number_of_tests)
