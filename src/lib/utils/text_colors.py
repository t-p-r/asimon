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
