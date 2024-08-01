"""
Shared functions and data between .py files in the master directory.
This file is gradually being stripped of code; when this is done it will be renamed __init__.py
"""

import random
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future

from .models import *
from .utils import *
from .exceptions import *
from .paths import *


# Will be moved to utils/compiler.py soon.
def compile_source_codes(
    compiler: str, compiler_args: list[str], source_files: list[str]
):
    get_dir(bindir)
    send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        text_colors.GREEN,
    )

    for source_file in source_files:
        source_path = str(workspace / source_file)  # extension already in config
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


# Slated for deprecation.
def perform_test_batch(
    worker_pool: ThreadPoolExecutor, worker_fns: list, *args, **kwargs
) -> list[Future]:
    """
    Submit to `worker_pool` calls with form `fn(*args, **kwargs)` for every functions in `worker_fns`. \\
    Returns a list of `Future` objects representing submitted calls.
    """
    return [worker_pool.submit(fn, *args, **kwargs) for fn in worker_fns]
