from lib.utils import wrap_message, text_colors


class InvalidConfig(Exception):
    def __init__(self, invalid_arg: str) -> None:
        super().__init__(self)
        self.invalid_arg = invalid_arg

    def __str__(self):
        return wrap_message(
            "Invalid format found in config file (argument \'%s\')." % self.invalid_arg,
            text_colors.RED,
        )
