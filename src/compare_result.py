"""
src/compare_result.py - Fuzz testing.

This tool will repeat the following process:
    - Generate test data from command line;
    - Pipe the data to "judge.cpp" (the reference program) and "contestant.cpp"'s stdin and run these files;
    - Evaluate the results, either by comparing the output of "judge.cpp" and "contestant.cpp" against each other, 
    or by using a custom C++ or Python checker to evaluate "contestant.cpp"'s output.
until either all test are run or a test which doesn't pass the evaluation process is found.

In the latter case, the input, both outputs, and the checker's comment shall be wrote down the file `status`.
The C++ files specified above must stay in the same folder as this Python file, must reads from stdin and writes to stdout.
"""

# USER PARAMETERS ------------------------------------------------------------------------------------------

testgen_script = "testgen --lo=-1000 --hi=1000"
"""
Script used to generate tests. Additional arguments, if any, must be configured by the user.
"""

test_count = 32
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

verbose = False
"""Whether to log passed tests's input, output and answer."""

worker_count = 8
"""
The number of workers (i.e. tests to be executed at the same time).\\
For best performance, this number should not exceed your CPU's thread count. \\
Multiple workers work best for computationally intensive problems; for IO-intensize problems (e.g. 10^5 integers or more), 1 or 2 workers yields the best performance. 
"""

compiler = "g++"
"""C++ compiler. Only `g++` has been tested and used extensively."""

compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20", "-H"]
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
passed_tests = 0


def perform_tests() -> bool:
    """Perform the number of tests specified by dividing them into batches the size of at most `worker_count`. \\
    Returns whether all the batches/tests passes."""

    # coming from C++ these lines are stupid to say the least
    global batch_count
    global passed_tests

    if test_count % worker_count != 0:
        # Cover the case where e.g. there are 9 test and 4 workers (the batches are 1-4, 5-8 and 9).
        batch_count += 1

    with ThreadPoolExecutor(max_workers=worker_count) as worker_pool:
        for batch in range(0, batch_count):
            first_test_of_batch = passed_tests + 1
            last_test_of_batch = min(passed_tests + worker_count, test_count)
            batch_size = last_test_of_batch - first_test_of_batch + 1
            send_message(
                "Executing batch %d (test %d - %d)"
                % (batch, first_test_of_batch, last_test_of_batch),
                text_colors.BOLD,
            )

            procs = []
            for i in range(0, batch_size):
                test_seed = random.getrandbits(31)
                procs.append(
                    worker_pool.submit(
                        workers[i].evaluate_test,
                        [bindir / testgen_bin]
                        + testgen_args
                        + ["--testlib_seed %d" % test_seed],
                        bindir / "judge",
                        bindir / "contestant",
                    )
                )

            for proc in procs:
                test_result = proc.result()
                test_index = passed_tests + 1

                if test_result.status != True or verbose == True:
                    test_logdir = get_dir(
                        logdir
                        / (
                            "test"
                            + str(test_index)
                            + ("-failed" if test_result.status != True else "")
                        )
                    )
                    status = open(test_logdir / "status.txt", "w")
                    input = open(test_logdir / "input.txt", "w")
                    output = open(test_logdir / "output.txt", "w")
                    answer = open(test_logdir / "answer.txt", "w")

                    def write_to_log(ostream, headline, content, limit=256):
                        status.write(headline)
                        write_prefix(status, content, limit, "\n\n")
                        ostream.write(content)

                    write_to_log(input, "Input:\n", test_result.input)
                    status.write("Comment:\n%s\n\n" % test_result.comment)
                    write_to_log(output, "Output:\n", test_result.output)
                    write_to_log(answer, "Answer:\n", test_result.answer)

                    status.close()
                    input.close()
                    output.close()
                    answer.close()

                    if test_result.status != True:
                        send_message(
                            "Disparity found, aborting execution...",
                            text_colors.RED + text_colors.BOLD,
                        )
                        return False

                passed_tests += 1

    return True


def print_final_verdict():
    percentage = passed_tests / test_count
    message = "Progress: %d/%d (%s)" % (
        passed_tests,
        test_count,
        str(100.0 * percentage)[:5] + "%",
    )
    if percentage == 1:  # all test passed
        send_message(message, text_colors.OK_GREEN)
    elif percentage == 0:  # the first test failed
        send_message(message, text_colors.RED)
    else:  # failed somewhere in between
        send_message(message, text_colors.YELLOW)


if __name__ == "__main__":
    delete_folder(logdir)
    compile_source_codes(compiler, compiler_args, bin_list)
    perform_tests()
    print_final_verdict()
