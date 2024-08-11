from .red_exception import RedException


class InvalidConfig(RedException):
    def __init__(self, invalid_arg: str) -> None:
        super().__init__(
            self,
            f"Invalid format found in config file (argument '{invalid_arg}').",
        )
