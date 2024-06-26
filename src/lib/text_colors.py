"""
A list of colors and attributes to be wrapped around  texts. Supported terminals only.
Some attributes can be combined (e.g. `PURPLE` + `BOLD` + `UNDERLINE`).
"""


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
