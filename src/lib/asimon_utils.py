"""
lib/asimon_utils.py - Helper functions and classes for asimon.
"""

from pathlib import Path
import os


class text_colors:
    OK_BLUE = "\033[94m"
    OK_CYAN = "\033[96m"
    OK_GREEN = "\033[92m"
    PURPLE = "\033[95m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    HEADER = "\033[95m"
    END_COLOR = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def delete_file(s):
    if Path(s).exists():
        os.remove(s)


def seek_file(output, source):
    if Path(output).exists() == False:
        raise Exception(
            wrap_message(
                source + " cannot be compiled, or doesn't exist.",
                text_colors.RED,
            )
        )


def wrap_message(message_text, color):
    """Wraps `color` around `message_text`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + message_text + text_colors.END_COLOR


def send_message(message_text, color, message_end="\n"):
    print(wrap_message(message_text, color), end=message_end)


def compile(compiler, args, source, output):
    os.system("%s %s %s -o %s" % (compiler, args, source, output))
