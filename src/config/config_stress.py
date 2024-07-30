problem = "$workspace"

if problem == "$workspace":
    main_correct_solution = "iostream"
    other_solutions = ["iostream", "buffer_scan", "stdio"]
    checker = "token"
    custom_checker = ""

testgen_script = "testgen 1000000 1000000000"
testlib_persistent = False
time_limit = 5
test_count = 32
status_only = False
cpu_count = 2
compiler = "g++"
compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
