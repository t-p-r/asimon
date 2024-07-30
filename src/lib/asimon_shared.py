"""
Shared functions and data between .py files in the master directory.
"""

import random
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future

from lib.models import *
from lib.utils import *

# Below are common paths in asimon:

rootdir = Path(__file__).parent.parent
# The project's root directory, .../asimon/src/
workspace = rootdir / "workspace"
# C++ workspace.
bindir = rootdir / "bin"
# Where the C++ executables are dumped into.
logdir = rootdir / "log"
# Log folder.
result_file_location = logdir / "result.txt"
# Reports on generic informations about the run.
universal_problems_dir = rootdir / "problems"
# Where we store problems.
cache_dir = rootdir / "cache"
# Store pair of .c/.cpp files and its binary. Enables skipping of compilation.


def compile_source_codes(
    compiler: str, compiler_args: list[str], source_files: list[str]
):
    get_dir(bindir)
    send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        text_colors.GREEN,
    )

    for source_file in source_files:
        source_path = str(workspace / source_file) # extension already in config
        output_path = str(bindir / source_file)
        ret = subprocess.run(
            [compiler] + compiler_args + [source_path, "-o", output_path]
        )
        # e.g. g++ -O2 hello.cpp -o /bin/hello
        if ret.returncode != 0:
            raise Exception(
                wrap_message(
                    source_path + " cannot be compiled, or doesn't exist.",
                    text_colors.RED,
                )
            )


# Slated for future deprecation.
def perform_test_batch(
    worker_pool: ThreadPoolExecutor, worker_fns: list, *args, **kwargs
) -> list[Future]:
    """
    Submit to `worker_pool` calls with form `fn(*args, **kwargs)` for every functions in `worker_fns`. \\
    Returns a list of `Future` objects representing submitted calls.
    """
    return [worker_pool.submit(fn, *args, **kwargs) for fn in worker_fns]
