"""
Shared functions and data between .py files in the master directory.
"""

import os
import shutil
import subprocess
from pathlib import Path
from concurrent.futures import Future, ThreadPoolExecutor, wait
from lib.worker import Worker
from lib.text_colors import text_colors

# Common paths in asimon:
root_dir = Path(__file__).parent.parent
# The project's absolute root directory, .../asimon/src/
bin_dir = root_dir / "bin"
# Where the C++ executables are dumped into.
universal_test_dir = root_dir / "tests"
# Test folder. Each platform has its own subfolder (e.g. /tests/vnoj, /tests/polygon).
log_output_stream = open(root_dir / "log.txt", "w")
# Will be closed when the tools exit anyway.


def compile_source_codes(compiler: str, compiler_args: list[str], bin_list: list[str]):
    bin_dir.mkdir(parents=True, exist_ok=True)
    send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        text_colors.OK_GREEN,
    )
    for bin in bin_list:
        # should these be Paths?
        source = "%s/%s.cpp" % (root_dir, bin)
        output = "%s/%s" % (bin_dir, bin)
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
    batch_size: int,
    worker_pool: ThreadPoolExecutor,
    testgen_command: str | list[str],
    judge_command: str,  # judge and contestant has no args
    contestant_command: str,
    workers: list[Worker],
) -> list[Future]:
    """Perform a batch of tests by pushing workers from `workers` to `worker_pool`."""

    procs = []
    for i in range(0, batch_size):
        procs.append(
            worker_pool.submit(
                workers[i].evaluate_test,
                testgen_command,
                judge_command,
                contestant_command,
            )
        )

    # Somehow the code only reaches this part after all jobs in `worker_pool` finishes.
    # Truly a mystery of the ages.
    return procs


# Miscellanous helpers:


def delete_file(s: Path):
    "Silently deletes a file, suppressing any `OSError` raised."
    try:
        os.remove(s)
    except OSError:
        pass


def delete_folder(p: Path):
    "Silently deletes a folder, suppressing any `OSError` raised."
    try:
        shutil.rmtree(p)
    except OSError:
        pass


def wrap_message(message_text: str, color: text_colors) -> str:
    """Wraps `color` around `message_text`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + message_text + text_colors.END_COLOR


def send_message(message_text: str, color: text_colors, message_end="\n"):
    """Print a message with colors and/or other attributes. See `text_colors` for some examples."""
    print(wrap_message(message_text, color), end=message_end)


def script_split(script: str) -> tuple[str, list]:
    """Split an execution script into the executable (first token) and its arguments (the other tokens).."""
    tokens = script.split()
    return (tokens[0], tokens[1:])


# Deprecated functions which should only be used for debugging:


def clear_previous_runs(bin_list: list[str]):
    """Deprecated."""
    send_message("Deleting executable files from previous runs...", text_colors.YELLOW)
    for bin in bin_list:
        delete_file("%s/bin/%s" % (root_dir, bin))
