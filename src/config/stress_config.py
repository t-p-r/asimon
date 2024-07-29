problem = "$workspace"

if problem == "$workspace":
    main_correct_solution = "judge"
    other_solutions = [
        "contestant",
        "contestant1",
        "contestant2",
        "contestant3",
    ]
    checker = "token"
    custom_checker = ""

testgen_script = "testgen --lo=-1000 --hi=1000"

testlib_persistent = False

time_limit = 0.1

test_count = 1024

status_only = True

cpu_count = 4

compiler = "g++"

compiler_args = "-pipe -O2 -D_TPR_ -std=c++20"
