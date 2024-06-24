"""
lib/asimon_shared.py - Functions shared between .py files in the master directory.
"""

import lib.asimon_utils as asutils
from pathlib import Path


root_dir = __file__[:-21] # .../asimon/src
"""this is scrubbed, i know, but works for now"""

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
        asutils.compile(compiler, compiler_args, source, output)
        asutils.seek_file(output, source)
