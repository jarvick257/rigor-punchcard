from .state import PunchcardState
from .screens import MainScreen

from rigor import Content, Module, Timer
from rigor.screens import (
    InputNumberScreen,
    MenuScreen,
    TimedScreen,
)


class Punchcard(Module[PunchcardState]):
    def __init__(self, title: str, log_file_path: str = "punchcard.csv"):
        super().__init__(PunchcardState(title, log_file_path), MainScreen())
