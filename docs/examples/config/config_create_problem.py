problem = "io"
"""Name of the problem."""

bundle_source = True
"""Whether to include test generator, solutions, ... (in general every files in the `workspace` folder) in the `tests` folder."""

subtasks = [
    (1, "testgen 10 10"),
    ["gentest %d" % i for i in range(2, 9)],
    "gentest 10",
    "formatttttttttttttttt",
]
"""
Each item in this list contains information about one subtask.
An item can be:
    - a single command line (e.g. `testgen.exe):
"""

testlib_persistent = True
"""
Testlib-specific. \\
Each script is used by testlib to hash a specific seed. Therefore, to generate distinct test cases from one script, each test case
will have its script appended by `--testlib_seed i` (`i` being the index of the test case within the subtask) before being ran. \\
Disabling this option will instead randomizes `i`, which will also makes it impossible to reproduce the tests.
"""

worker_count = 16
"""
The number of workers (i.e. tests to be executed at the same time).\\
For best performance, this number should not exceed your CPU's thread count. \\
Multiple workers work best for computationally intensive problems; for IO-intensize problems (e.g. 10^5 integers or more), 
1 or 2 workers yields the best performance. 
"""

compiler = "g++"

compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20", "-H"]
"""
Compiler arguments. See your C++ compiler for documentation. Do note that:
    - some arguments are platform-specific (e.g. `-Wl,--stack=<windows_stack_size>`)
    - if you have precompiled headers (e.g. `stdc++.h`), use the exact set of arguments you compiled them with to save time.
"""