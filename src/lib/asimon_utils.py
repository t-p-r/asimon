# boilerplates
import os


class text_colors:
    OK_BLUE = "\033[94m"
    OK_CYAN = "\033[96m"
    OK_GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    HEADER = "\033[95m"
    END_COLOR = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def delete_file(s):
    if os.path.exists(s):
        os.remove(s)


def seek_file(output, source):
    if os.path.exists(output) == False:
        raise Exception(source + " cannot be compiled")


def wrap_message(message_text, color):
    """Wraps `color` around `message_text`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + message_text + text_colors.END_COLOR


def send_message(message_text, color):
    print(wrap_message(message_text, color))


def compile(source, output, compiler, args):
    """Tested for `g++` and `gcc`."""
    os.system(compiler + " " + args + " " + source + " -o " + output)
