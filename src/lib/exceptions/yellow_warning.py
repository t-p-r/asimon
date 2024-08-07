from lib.utils.formatting import wrap_message, text_colors

# TODO: fix issue where the program terminates after raising this Warning


class YellowWarning(Warning):
    def __init__(self, message: str) -> None:
        super().__init__(self)
        self.message = message

    def __str__(self):
        return wrap_message(self.message, text_colors.YELLOW)
