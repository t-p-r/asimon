"""
lib/asimon_base.py - Functions shared between .py files in the master directory.
"""

import lib.asimon_utils as asutils
import os


def clear_previous_run(exec_list, current_dir):
    asutils.send_message(
        "Deleting executable files from previous run...", asutils.text_colors.YELLOW
    )
    for exec in exec_list:
        asutils.delete_file("%s/dump/%s" % (current_dir, exec))


def compile_source_codes(exec_list, dir, compiler_args, compiler="g++"):
    if os.path.exists(dir + "/dump") == False:
        os.mkdir(dir + "/dump")
    # need current directory because this context will otherwise not be provided to g++
    asutils.send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        asutils.text_colors.OK_GREEN,
    )
    for exec in exec_list:
        source = "%s/%s.cpp" % (dir, exec)
        output = "%s/dump/%s" % (dir, exec)
        asutils.compile(compiler, compiler_args, source, output)
        asutils.seek_file(output, source)
