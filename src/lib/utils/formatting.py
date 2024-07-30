"""Formatting utilities."""

from io import TextIOWrapper
from lib.utils import text_colors


def wrap_message(content: str, color: text_colors) -> str:
    """Wraps `color` around `content`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + content + text_colors.END_COLOR


def send_message(content: str, color: text_colors, end="\n"):
    """Print to the terminal a message with colors and/or other attributes. See `text_colors` for some examples."""
    print(wrap_message(content, color), end=end)


def script_split(script: str) -> tuple[str, list]:
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
        ostream.write(" ...\n(%d character(s) remains)" % (len(content) - limit))
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
