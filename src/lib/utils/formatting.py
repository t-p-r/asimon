"""Formatting utilities."""

from io import TextIOWrapper


class text_colors:
    """
    A list of ANSI escape sequences that can be used as colors and other attributes for texts.
    Supported by UNIX terminals and the new Windows Terminal.
    Some attributes can be combined (e.g. `PURPLE` + `BOLD` + `UNDERLINE`).
    More at: https://www.embedded.pub/linux/misc/escape-codes.html.
    """

    # colors
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    PURPLE = "\033[95m"
    YELLOW = "\033[93m"
    RED = "\033[91m"

    # other attributes
    HEADER = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # remove any attributes above
    END_COLOR = "\033[0m"


def wrap_message(content: str, color: text_colors) -> str:
    """Wraps `color` around `content`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + content + text_colors.END_COLOR


def send_message(content: str, color: text_colors, end="\n"):
    """Print to the terminal a message with colors and/or other attributes. See `text_colors` for some examples."""
    print(wrap_message(content, color), end=end)


def script_split(script: str) -> tuple[str, list[str]]:
    """Split an execution script into the executable (first token) and its arguments (the other tokens).."""
    tokens = script.split()
    return (tokens[0], tokens[1:])


def write_prefix(ostream: TextIOWrapper, content: str, limit: int, end: str) -> None:
    """
    Write at most `limit` first characters of `content` to `ostream`.
    """
    if content is None:
        content = ""
    if len(content) <= limit:
        ostream.write(content)
    else:
        ostream.write(content[: (limit + 1)])
        ostream.write(f" ...\n({len(content) - limit} character(s) remains)")
    ostream.write(end)


def remove_ext(args: list[str]):
    """
    Remove extensions from all items in `args` (i.e. all character including and after the last `.`).
    """
    result = []
    for arg in args:
        pos = arg.rfind(".")  # also works for .cpp
        result.append(arg[:pos] if pos != -1 else arg)
    return result
