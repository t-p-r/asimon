""" 
src/compare_time.py - Compare executing times of `judge.cpp` and `contestant.cpp` using test generated from command line.
Stop either when the desired number of tests have been run.
The files above must stay in the same folder as this Python file, and must reads from `stdin` and writes to `stdout`.
"""

# USER PARAMETERS ------------------------------------------------------------------------------------------

test_generation_command_line = "testgen"
"""
Script used to generate tests. Additional arguments, if any, must be configured by the user.
"""

test_count = 16
"""What you think it is."""

compiler = "g++"

compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20"]
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have precompiled headers (e.g. `stdc++.h`), use the exact arguments you compiled them with to save time
"""

# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import time
import lib.asimon_utils as asutils
from lib.asimon_shared import *

bin_list += ["testgen", "judge", "contestant"]


def running_time(command):
    start_time = time.time()
    os.system(command)
    return time.time() - start_time


def perform_tests(iterations):
    total_contestant_time = 0
    total_checker_time = 0

    for i in range(1, iterations + 1):
        send_message("Executing test:  %s" % i, text_colors.BOLD)
        os.system(
            "%s > %s" % (root_dir + "/bin/" + test_generation_command_line, input_dump)
        )
        contestant_test_runtime = running_time(
            "%s < %s > %s"
            % (root_dir + "/bin/contestant", input_dump, contestant_output)
        )
        judge_test_runtime = running_time(
            "%s < %s > %s" % (root_dir + "/bin/judge", input_dump, answer)
        )

        log_output_stream.write("Test %d:\n" % i)
        log_output_stream.write("Judge took:      %f (s)\n" % judge_test_runtime)
        log_output_stream.write("Contestant took: %f (s)\n\n" % contestant_test_runtime)

        total_contestant_time += contestant_test_runtime
        total_checker_time += judge_test_runtime

    print_final_verdict(total_contestant_time, total_checker_time)


def print_final_verdict(total_contestant_time, total_checker_time):
    send_message(
        "Judge took:      %f (s)" % total_checker_time,
        text_colors.OK_GREEN,
    )
    send_message(
        "Contestant took: %f (s)" % total_contestant_time,
        text_colors.OK_CYAN,
    )
    print("(see log.txt for details)")


if __name__ == "__main__":
    clear_previous_run()
    compile_source_codes(compiler_args, compiler)
    perform_tests(test_count)
