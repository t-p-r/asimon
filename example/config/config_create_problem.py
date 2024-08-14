problem_name = "aplusb"

# These files are search in the workspace folder:
main_correct_solution = "judge.cpp"
other_solutions = ["contestant.cpp"]
external_checker = "checker.cpp"

subtasks = [
    "testgen 0 100",
    (4, "testgen_testlib --lo 1e3 testgen_testlib --hi 1e4"),  # testlib accepts scientific notation
    (8, f"testgen --lo 0 --hi {10**9}"),  # Python 3 string formatting
    [f"testgen --lo {i} --hi {j}" for i in range(10, 15) for j in range(i, 15)],  # template trick
]
"""
Each item in this list contains information about one subtask. They can be
- A single script (e.g. `testgen 1 2 3`). In this case this subtask has exactly one test case.
- A list [] of scripts.
- A pair `(test_count, test_script)`. In this case:
    - the subtask will have `test_count` tests;
    - each script will possibly be appended with `--seed X` (see `testlib_seed` below).

Each script should have a form `generator-name [params]`.
DO NOT use extensions, like ".exe" in the script.
"""

testlib_seed = "from0"
"""
For testlib.h users.
If this option is not "none", each script will be appended with `--seed X`
in order to make outputs unique.

Possible options (other than "none") are:
- `"from0"`: this will gradually increases X from 0 for each subtask. For example,
    if a subtask is  `(8, "testgen")` then the actual sequence of commands invoked would be
    `testgen --seed 0`, `testgen --seed 1`, ..., `testgen --seed 7`.
- `"random"`: this will instead randomizes X, which will also makes it impossible to
    reproduce the tests except by directly loading the file `/test/script.json` inside
    the problem folder.
"""

testdir_format = "sub%S-test%T"
"""
Format for test case folders.

- %C: cumulative test index
- %S: subtask index
- %T: test index within subtask

All indexes are 1-based.
"""

make_test_folders = False
"""
Whether to create folders containing test cases' data in the `test` folder.
"""

make_zip = True
"""
Whether to create a zip file containing those folders.
"""

bundle_source = True
"""
Whether to also include test generators, solutions, checkers ... 
(in general every file in the `workspace` folder) in the zip file above.
"""

time_limit = 1
"""
In seconds, can be decimal (e.g. 0.25).
If the test generator of the main correct solution runs past this duration, the entire program will terminate.
"""

cpu_workers = 4
"""
The number of CPUs used to execute tests concurrently. \\
For the best balance between various CPU and IO factors (see documentation for more details), 
this number should be HALF your CPU's physical core count.
"""

compilation_command = "$default"
"""
config_stress.py - Configuration for stress.py.
"""

problem_name = ""
"""
Name of the saved problem, or `$workspace` if you want to source your C++ files directly from the `workspace` folder.
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

compilation_command = "cl $default"
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
