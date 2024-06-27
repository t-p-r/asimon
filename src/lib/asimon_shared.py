"""
lib/asimon_shared.py - Shared functions and data between .py files in the master directory.
"""

import lib.asimon_utils as asutils
from pathlib import Path
import subprocess


root_dir = __file__[:-20]  # .../asimon/src/, without the "lib/asimon_shared.py" part
"""this is scrubbed, i know, but works for now"""

dump_dir = root_dir + "/dump/"
universal_test_dir = root_dir + "/tests/"

log_output_stream = open(root_dir + "log.txt", "w")
input_dump = dump_dir + "input.txt"
contestant_output = dump_dir + "output_contestant.txt"
judge_output = dump_dir + "output_judge.txt"

exec_list = []


def clear_previous_run():
    asutils.send_message(
        "Deleting executable files from previous run...", asutils.text_colors.YELLOW
    )
    for exec in exec_list:
        asutils.delete_file("%s/dump/%s" % (root_dir, exec))


def compile_source_codes(compiler_args, compiler="g++"):
    Path(root_dir + "/dump").mkdir(parents=True, exist_ok=True)
    asutils.send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        asutils.text_colors.OK_GREEN,
    )
    for exec in exec_list:
        source = "%s/%s.cpp" % (root_dir, exec)
        output = "%s/dump/%s" % (root_dir, exec)
        ret = subprocess.run([compiler] + compiler_args + [source, "-o", output])
        if ret.returncode != 0:
            raise Exception(
                asutils.wrap_message(
                    source + " cannot be compiled, or doesn't exist.",
                    asutils.text_colors.RED,
                )
            )
