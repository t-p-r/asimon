# USER VARIABLES ------------------------------------------------------------------------------------------

test_generation_command_line = "./test"
# often, just "./test" should be enough; additional arguments (i.e. those passed to argv[]) are the choice of the user

number_of_tests = 16
# what you think it is

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
# note that some arguments are specific to either Unix or Windows (e.g. "-Wl,--stack=<desired_stack_size>")


# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

import os
import filecmp
import shutil
import time
import lib.asimon_utils as asutils

# not in lib file (for easier understanding)
PASS_ALL = 1
PASS_NONE = 0

log_output_stream = open("log.txt", "w")
input_dump = "./dump/input_dump.txt"
output_dump = "./dump/output_dump.txt"
temp_output_dump = "./dump/output_dump.txt.temp"


def clear_previous_run():
    asutils.send_message(
        "Deleting executable files from previous run...", asutils.text_colors.YELLOW
    )
    asutils.delete_file("./test")
    asutils.delete_file("./contestant")
    asutils.delete_file("./checker")


def compile_source_codes():
    asutils.send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        asutils.text_colors.OK_GREEN,
    )
    asutils.compile("test.cpp", "./test", "g++", compiler_args)
    asutils.compile("contestant.cpp", "./contestant", "g++", compiler_args)
    asutils.compile("checker.cpp", "./checker", "g++", compiler_args)

    # throw error if source codes wasn't compiled
    asutils.seek_file("./test", "test.cpp")
    asutils.seek_file("./contestant", "contestant.cpp")
    asutils.seek_file("./checker", "checker.cpp")


def running_time(command):
    start_time = time.time()
    os.system(command)
    return time.time() - start_time


total_contestant = 0
total_checker = 0


def perform_tests(iterations):
    global total_contestant
    global total_checker

    passed_tests = 0.0
    for i in range(1, iterations + 1):
        asutils.send_message("Executing test: " + str(i), asutils.text_colors.BOLD)

        os.system(test_generation_command_line)
        t1 = running_time("./contestant")
        t2 = running_time("./checker")

        log_output_stream.write("Test " + str(i) + ":\n")
        log_output_stream.write("Judge took:      " + str(t2) + "(s)\n")
        log_output_stream.write("Contestant took: " + str(t1) + "(s)\n\n")

        total_contestant += t1
        total_checker += t2
        passed_tests += 1


def print_final_verdict():
    asutils.send_message(
        "Judge took:      " + str(total_checker) + "(s)", asutils.text_colors.OK_GREEN
    )
    asutils.send_message(
        "Contestant took: " + str(total_contestant) + "(s)", asutils.text_colors.OK_CYAN
    )
    print("See log.txt for details.")

if __name__ == "__main__":
    clear_previous_run()
    compile_source_codes()
    perform_tests(number_of_tests)
    print_final_verdict()
