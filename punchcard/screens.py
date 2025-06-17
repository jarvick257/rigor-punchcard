from datetime import timedelta
from .state import PunchcardState

from rigor import Content, Module, Timer
from rigor.screens import MenuScreen


def _td(t: timedelta) -> str:
    hours, seconds = divmod(int(t.total_seconds()), 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    seconds = int(seconds)
    if hours < 10:
        return f"{minutes:02d}m {seconds:02d}s"
    return f"{hours}h {minutes:02d}m"


class MainScreen(MenuScreen[PunchcardState]):
    def __init__(self):
        super().__init__(
            "MainScreen", ["Session", "Day", "Week", "Month", "Total", "Back"]
        )
        self._timer = Timer(1, self.on_timeout)

    def on_attach(self):
        self._timer.start()

    def on_detach(self):
        self._timer.stop()

    def on_client_disconnected(self):
        self.state.punch_out()
        self.refresh()

    def on_timeout(self):
        if self.state.punched_in:
            self.refresh()

    def _render_home(self):
        return Content(self.state.title, self.selection)

    def _render_toggle(self):
        return Content(self.state.title, self.selection)

    def render(self):
        if self.selection == "Back":
            return Content(self.state.title, self.selection)
        if self.selection == "Session" and self.state.punched_in:
            return Content(self.state.title, _td(self.state.punched_in_since()))
        if self.selection == "Session" and not self.state.punched_in:
            return Content(self.state.title, "Punched out")
        if self.selection == "Day":
            return Content(self.state.title, f"D: {_td(self.state.time_today())}")
        if self.selection == "Week":
            return Content(self.state.title, f"W: {_td(self.state.time_this_week())}")
        if self.selection == "Month":
            return Content(self.state.title, f"M: {_td(self.state.time_this_month())}")
        if self.selection == "Total":
            return Content(self.state.title, f"T: {_td(self.state.time_total())}")

    def on_enter(self):
        if self.selection == "Back":
            self.pop()
        else:
            self.state.toggle()
            self.refresh()
