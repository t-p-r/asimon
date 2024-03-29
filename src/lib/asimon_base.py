# Functions that most/all .py files in the master directory uses.
import lib.asimon_utils as asutils
import os


def clear_previous_run(exec_list, current_dir):
    asutils.send_message(
        "Deleting executable files from previous run...", asutils.text_colors.YELLOW
    )
    for exec in exec_list:
        asutils.delete_file("%s/dump/%s" % (current_dir, exec))


def compile_source_codes(exec_list, compiler_args, current_dir):
    if os.path.exists(current_dir + "/dump") == False:
        os.mkdir(current_dir + "/dump")
    # need current directory because this context will otherwise not be provided to g++
    asutils.send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        asutils.text_colors.OK_GREEN,
    )
    for exec in exec_list:
        source = "%s/%s.cpp" % (current_dir, exec)
        output = "%s/dump/%s" % (current_dir, exec)
        asutils.compile(
            source,
            output,
            "g++",
            compiler_args,
        )
        asutils.seek_file(output, source)
