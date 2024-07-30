task_name = "aplusb"
"""Name of the problem."""

platform = "vnoj"
"""
Target platform. For now only "vnoj" is supported.
"""

bundle_source = True
"""Whether to include test generation and solution files in the test folder."""

subtask_test_count = [4, 4]
"""Number of tests for each subtasks."""

subtask_script = [
    "testgen --lo -1000 --hi 1000",
    "testgen --lo -1000 --hi 1000",
]
"""
Script used to generate tests for each subtasks.
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