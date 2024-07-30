problem = "aplusb"
bundle_source = True

subtasks = [
    (1, "testgen 10 10"),
    ["gentest %d" % i for i in range(2, 9)],
    "gentest 10",
    "formatttttttttttttttt",
]

testlib_persistent = True
worker_count = 16
compiler = "g++"
compiler_args = ["-pipe", "-O2", "-D_TPR_", "-std=c++20", "-H"]
