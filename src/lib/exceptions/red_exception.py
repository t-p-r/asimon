from lib.utils.formatting import wrap_message, text_colors


class RedException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(self)
        self.message = message

    def __str__(self):
        return wrap_message(self.message, text_colors.RED)
