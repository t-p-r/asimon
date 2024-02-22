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
    start_time=time.time()
    os.system(command)
    return time.time()-start_time

def perform_test():
    os.system(test_generation_command_line)
    print((str)(running_time("./contestant")))
    shutil.copyfile(output_dump, temp_output_dump)
    print((str)(running_time("./checker")))


def perform_tests(iterations):
    passed_tests = 0.0
    for i in range(1, iterations + 1):
        asutils.send_message("Executing test: " + str(i), asutils.text_colors.BOLD)
        perform_test()

        if filecmp.cmp(output_dump, temp_output_dump) == False:
            log_output_stream.write("Test " + str(i) + ":\n")
            log_output_stream.write("Input:\n" + open(input_dump, "r").read() + "\n")
            log_output_stream.write(
                "Contestant's output:\n" + open(temp_output_dump, "r").read() + "\n"
            )
            log_output_stream.write(
                "Judge's output:\n" + open(output_dump, "r").read() + "\n"
            )
            log_output_stream.write("\n")
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
        "Progress: "
        + str(passed_tests)
        + "/"
        + str(number_of_tests)
        + " ("
        + str(100.0 * passed_tests / number_of_tests)
        + "%)"
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
    compile_source_codes()
    perform_tests(number_of_tests)
