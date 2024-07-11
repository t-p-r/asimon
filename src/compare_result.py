"""
src/compare_result.py - Fuzz testing.

This tool will repeat the following process:
    - Generate test data from command line.
    - Pipe the data to "judge.cpp" (the reference program) and "contestant.cpp"'s stdin and run these files.
    - Evaluate the results, either by comparing the output of "judge.cpp" and "contestant.cpp" against each other, 
    or using a custom C++ checker to evaluate "contestant.cpp"'s output.
until either the desired number of tests or a test which doesn't pass the evaluation process is reached.

In the latter case, the input, both outputs, and the checker's comment shall be wrote down the file `log.txt`.
The C++ files specified above must stay in the same folder as this Python file, must reads from stdin and writes to stdout.
"""

# USER PARAMETERS ------------------------------------------------------------------------------------------

testgen_script = "testgen 100 100"
"""
Script used to generate tests. Additional arguments, if any, must be configured by the user.
"""

test_count = 60
"""What you think it is."""

checker = "token"
"""Result checker. Must be one of:
    - "token"   : Check if the outputs' token sequences match.
    - "line"    : Check if every line of the outputs match (whitespace ignored).
    - "double4" : Like "token", but corresponding number tokens must be within 1E-4 of each other.
    - "double6" : Like double4, but the epsilon is 1E-6.
    - "double9" : Like double4, but the epsilon is 1E-9.
    - "custom"  : Custom checker. The file "checker.cpp" shall be feeded the test data and the contestant's output.
                  Evaluating them is the user's responsibility.
    - "noeval"   : Always returns True. The default checker for `testgen.py` as no evaluation happens there 
                  except when custom checkers are involved.
"""

worker_count = 8
"""
The number of workers (i.e. tests to be executed at the same time). \\
Since each CPU thread can only be occupied by one worker at a time, for best performance, this number should not exceed your CPU's thread count.
"""

compiler = "g++"
"""C++ compiler. Only `g++` has been tested and used extensively."""

compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20"]
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have precompiled headers (e.g. `stdc++.h`), use the exact argument list you compiled them with to save time
"""


# HIC SUNT DRACONES ---------------------------------------------------------------------------------------

from lib.asimon_shared import *

testgen_bin, testgen_args = script_split(testgen_script)
bin_list = [testgen_bin, "judge", "contestant"]
workers = [Worker(checker)] * worker_count

batch_count = int(test_count / worker_count)
passed_batches = 0


def perform_tests() -> bool:
    """Perform the number of tests specified by dividing them into batches the size of at most `worker_count`. \\
    Returns whether all the batches/tests passes."""

    # coming from C++ these lines are stupid to say the least
    global batch_count
    global passed_batches

    if test_count % worker_count != 0:
        # Cover the case where e.g. there are 9 test and 4 workers (the batches are 1-4, 5-8 and 9).
        batch_count += 1

    with ThreadPoolExecutor(max_workers=worker_count) as worker_pool:
        for batch in range(0, batch_count):
            first_test_of_batch = batch * worker_count + 1
            last_test_of_batch = min(first_test_of_batch + worker_count - 1, test_count)
            batch_size = last_test_of_batch - first_test_of_batch + 1
            send_message(
                "Executing batch %d (test %d - %d)"
                % (batch, first_test_of_batch, last_test_of_batch),
                text_colors.BOLD,
            )

            procs = perform_test_batch(
                batch_size=batch_size,
                worker_pool=worker_pool,
                testgen_command=[bin_dir / testgen_bin] + testgen_args,
                judge_command=bin_dir / "judge",
                contestant_command=bin_dir / "contestant",
                workers=workers,
            )

            for proc in procs:
                test_result = proc.result()
                if test_result.status != True:
                    log_output_stream.write(
                        ("Input:\n%s\n" "Comment:\n%s\n")
                        % (test_result.testdata, test_result.comment)
                    )
                    if test_result.answer != None:
                        log_output_stream.write(
                            "Judge's output:\n%s\n" % (test_result.answer)
                        )

                    if test_result.contestant_output != None:
                        log_output_stream.write(
                            "Contestant's output:\n%s\n"
                            % (test_result.contestant_output)
                        )
                    send_message(
                        "Disparity found, aborting execution...",
                        text_colors.RED + text_colors.BOLD,
                    )
                    return False
            passed_batches += 1

    return True


def print_final_verdict(passed_batches):
    percentage = passed_batches / batch_count
    message = "Progress: %d/%d (%s)" % (
        passed_batches,
        batch_count,
        str(100.0 * percentage) + "%",
    )
    if percentage == 1:  # all test passed
        send_message(message, text_colors.OK_GREEN)
    elif percentage == 0:  # the first test failed
        send_message(message, text_colors.RED)
    else:  # failed somewhere in between
        send_message(message, text_colors.YELLOW)
    log_output_stream.write(message)


if __name__ == "__main__":
    compile_source_codes(compiler, compiler_args, bin_list)
    perform_tests()
    print_final_verdict(passed_batches)
