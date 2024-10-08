"""
config_stress.py - Configuration for stress.py.
"""

problem_name = ""
"""
Name of the saved problem, or `$workspace` if you want to source your C++ files from the `workspace` folder.
"""

if problem_name == "":
    main_correct_solution = "judge.cpp"

    other_solutions = [
        "contestant.cpp",
    ]

    checker_type = "external"
    """Result checker. Must be one of:
        - "token"       : Check if every tokens of the output matches the answer. Recommended for most use cases.
        - "byte"        : Check if the output is exactly the same (down to single bytes) as the answer.
        - "line"        : Check if every line of the output match. Lines with no content or just whitespaces are ignored.
        - "external"    : External checker using a C++ file from the `workspace` folder.
    """

    external_checker = "checker.cpp"
    """If `checker` is `external`, this is the name of the C++ file."""

# testgen_script = "testgen_testlib --lo 0 --hi 1000"
testgen_script = "testgen 0 1000"
"""
Each script should have a form `generator-name [params]`.

Do not use extensions, like ".exe" in the script.

For `testlib.h` users: each time this script is run, it will have been appended with "--seed X" (where X is a random unsigned 31-bit integer).
This will make outputs unique even though there is only one script.
"""

time_limit = 1
"""
In seconds, can be decimal (e.g. 0.25).
"""

test_count = 1024

failed_test_data = True
"""
If set to False, no test data of failed tests will be given in the `log` directory,
and that directory will only contains a file detailing the overall results.
"""

cpu_workers = 4
"""
The number of CPUs used to execute tests concurrently. \\
For the best balance between various CPU and IO factors (see documentation for more details), 
this number should be HALF your CPU's physical core count.
"""

compilation_command = "$default"
"""
This argument can be either:
- Empty string or `"$default"`: ASIMON will automatically detect the compiler 
and appends its default compilation args.
- `"g++ $default"`: ASIMON will attempts to use the G++ compiler and appends its
default compilation args.
- `"clang++ $default"`: same as above but for the Clang compiler.
- Any other string: ASIMON will interpret the first token as the compiler
and the rest as arguments.

For compiler arguments, see your C++ compiler's documentation. Do note that:
- some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
- if you have any precompiled header (e.g. `stdc++.h.gch`), use the exact set of arguments 
you compiled it with to save time.
"""
