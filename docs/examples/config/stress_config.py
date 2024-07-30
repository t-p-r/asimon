"""
configuration/stress.py - Configuration for stress.py.
"""

problem = "$workspace"
"""
Name of the saved problem, or `$workspace` if you want to source your C++ files directly from the `workspace` folder.
"""

if problem == "$workspace":
    main_correct_solution = "judge.cpp"

    other_solutions = ["contestant.cpp"]
    """These are to be compared against the MCS."""

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

testgen_script = "testgen --lo=-1000 --hi=1000"
"""
Additional arguments are passed to the test generators as `argc` (num. of arguments) and `argv` (list of arguments).
For testlib.h users: each time the script is run, it will be appended with `--seed X` (where `X` is a random unsigned 31-bit integer), 
so that outputs are unique even though there is only one script. 
"""

testlib_persistent = True
"""
For testlib.h users: this will not randomizes `X` but would gradually increments it from 1.
So, if `testgen_script` is "abc -n 10", the actual scripts invoked would be 
`abc -n 10 --seed 1`, `abc -n 10 --seed 2`, `abc -n 10 --seed 3` etc.
"""

time_limit = 1
"""In seconds."""

test_count = 64

status_only = True
"""
If set to True, the `log` directory will only contains the general status of each solution (e.g. `sol1.cpp: time limit exceeded (test 17).`).
No test data will be given.
"""

cpu_count = 4
"""
The number of CPUs used to execute tests concurrently. \\
For the best balance between various CPU/IO factors (see documentation for more details), 
this number should be HALF your CPU's physical core count.
"""

compiler = "g++"
"""C++ compiler. Only `g++` has been tested and used extensively."""

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20 -H"
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have any precompiled header (e.g. `stdc++.h`), use the exact argument set you compiled it with to save time.
"""
