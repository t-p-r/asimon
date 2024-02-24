import lib.asimon_utils as asutils


def clear_previous_run(exec_list):
    asutils.send_message(
        "Deleting executable files from previous run...", asutils.text_colors.YELLOW
    )
    for exec in exec_list:
        asutils.delete_file("./" + exec)


def compile_source_codes(exec_list, compiler_args):
    asutils.send_message(
        "Compiling source codes, warnings and/or errors may be shown below...",
        asutils.text_colors.OK_GREEN,
    )
    for exec in exec_list:
        asutils.compile(exec + ".cpp", "./dump/" + exec, "g++", compiler_args)
        asutils.seek_file("./dump/" + exec, exec + ".cpp")
