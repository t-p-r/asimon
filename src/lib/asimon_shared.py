"""
Shared functions and data between .py files in the master directory.
"""

import subprocess
import multiprocessing
from concurrent.futures import *
from lib.worker import Worker
from lib.asimon_utils import *

# Common paths in asimon:
rootdir = Path(__file__).parent.parent
# The project's absolute root directory, .../asimon/src/
bindir = rootdir / "bin"
# Where the C++ executables are dumped into.
universal_testdir = rootdir / "tests"
# Test folder. Each platform has its own subfolder (e.g. /tests/vnoj, /tests/polygon).
logdir = rootdir / "log"
# Log folder.


def compile_source_codes(compiler: str, compiler_args: list[str], bin_list: list[str]):
    get_dir(bindir)
    send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        text_colors.OK_GREEN,
    )
    for bin in bin_list:
        # TODO: Should these be Paths?
        source = str(rootdir / bin) + ".cpp"
        output = str(bindir / bin)
        ret = subprocess.run([compiler] + compiler_args + [source, "-o", output])
        # e.g. g++ -O2 hello.cpp -o /bin/hello
        if ret.returncode != 0:
            raise Exception(
                wrap_message(
                    source + " cannot be compiled, or doesn't exist.",
                    text_colors.RED,
                )
            )


def perform_test_batch(
    worker_pool: ThreadPoolExecutor, worker_fns: list, *args, **kwargs
) -> list[Future]:
    """
    Submit to `worker_pool` calls with form `fn(*args, **kwargs)` for every functions in `worker_fns`. \\
    Returns a list of `Future` objects representing submitted calls.
    """
    return [worker_pool.submit(fn, *args, **kwargs) for fn in worker_fns]
