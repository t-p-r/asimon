"""
config_stress.py - Configuration for stress.py.
"""

problem_name = "$workspace"
"""
Name of the saved problem, or `$workspace` if you want to source your C++ files directly from the `workspace` folder.
"""

if problem_name == "$workspace":
    main_correct_solution = "judge.cpp"

    other_solutions = [
        "judge.cpp",
        "contestant.cpp",
    ]
    """Includes the main correct solution here if you want to see results on its execution time."""

    checker = "token"
    """Result checker. Must be one of:
        - "token"   : Check if the outputs' token sequences match.
        - "line"    : Check if every line of the outputs match (whitespace ignored).
        - "double4" : Like "token", but corresponding number tokens must be within 1E-4 of each other.
        - "double6" : Like double4, but the epsilon is 1E-6.
        - "double9" : Like double4, but the epsilon is 1E-9.
        - "custom"  : Custom checker.
        - "dummy"   : Always returns True.
    """

    custom_checker = ""
    """If `checker` is `custom`, this is the name of the C++ checker."""

testgen_script = "testgen 0 1000"
"""
For testlib.h users: each time this script is run, it will have been appended with "--seed X" (where X is a random unsigned 31-bit integer).
This will make outputs unique even though there is only one script. 
"""

testlib_persistent = False
"""
For testlib.h users: this will not randomizes X but would instead increments it from 1.
So, if `testgen_script` is "abc -n 10", the actual scripts invoked would be 
"abc -n 10 --seed 1", "abc -n 10 --seed 2", "abc -n 10 --seed 3", etc.
"""

time_limit = 1
"""In seconds."""

test_count = 32

failed_test_data = True
"""
If set to True, no test data of failed tests will be given in the `log` directory.
"""

cpu_count = 4
"""
The number of CPUs used to execute tests concurrently. \\
For the best balance between various CPU and IO factors (see documentation for more details), 
this number should be HALF your CPU's physical core count.
"""

compiler = "g++"
"""C++ compiler. Only `g++` has been tested and used extensively. `clangd++` should also work."""

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20 -H"
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have any precompiled header (e.g. `stdc++.h`), use the exact argument set you compiled it with to save time.
"""
