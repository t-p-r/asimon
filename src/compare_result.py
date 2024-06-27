"""
src/compare_result.py - Fuzz testing by:
    1. Generate tests from command line.
    2. Use "judge.cpp" and "contestant.cpp" to run these tests and compare their outputs, where "judge.cpp" is the reference code.

Stop either when the desired number of tests have been run, or if a test where the outputs of "judge.cpp" and "contestant.cpp" differs is found.
In that case, the test data and both outputs shall be wrote down the file `log.txt`.
The three files above must stay in the same folder as this Python file, must reads from stdin and writes to stdout.

# TODO: add multiple output comparing modes including a custom checker.
"""

# USER VARIABLES ------------------------------------------------------------------------------------------

script = "testgen"
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

import lib.asimon_utils as asutils
from lib.asimon_shared import *

exec_list += ["testgen", "judge", "contestant"]

# result status (whether all or none of the tests passed)
PASS_ALL = 1
PASS_NONE = 0


def perform_tests(iterations):
    passed_tests = 0
    for i in range(1, iterations + 1):
        asutils.send_message("Executing test: %d" % i, asutils.text_colors.BOLD)

        subprocess.run(dump_dir + script, stdout=subprocess.PIPE)

        contestant_output = subprocess.run(
            dump_dir + "/contestant",
            stdin=subprocess.PIPE,
            capture_output=True,
            encoding="UTF-8",
        ).stdout

        judge_output = subprocess.run(
            dump_dir + "/judge",
            stdin=subprocess.PIPE,
            capture_output=True,
            encoding="UTF-8",
        ).stdout

        # The only mode for comparing outputs is to check whether they differs in any characters.
        # Should be replaced by comparision modules in the future.
        if contestant_output != judge_output:
            log_output_stream.write("Test %d of %d: \n" % (i, iterations))
            log_output_stream.write("Input:\n%s \n" % input_dump)
            log_output_stream.write("Contestant's output:\n%s \n" % contestant_output)
            log_output_stream.write("Judge's output:\n%s \n\n" % judge_output)
            asutils.send_message(
                "Disparity found, aborting execution...",
                asutils.text_colors.RED + asutils.text_colors.BOLD,
            )
            break
        passed_tests += 1
    print_final_verdict(passed_tests)


def print_final_verdict(passed_tests):
    percentage = passed_tests / test_count
    message = (
        "Progress: %d/%d (%s"
        % (
            passed_tests,
            test_count,
            100.0 * passed_tests / test_count,
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
    clear_previous_run()
    compile_source_codes(compiler_args, compiler)
    perform_tests(test_count)
