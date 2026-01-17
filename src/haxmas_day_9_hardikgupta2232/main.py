from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Grid, Vertical, Center
from textual.screen import Screen
import datetime


class DayScreen(Screen):

    CSS = """
    DayScreen {
        align: center middle;
        background: rgb(18,18,28);
    }

    #dialog {
        width: 50;
        border: thick cyan;
        background: rgb(30,30,40);
        padding: 2;
        align: center middle;
    }

    #dialog Label {
        text-align: center;
        color: white;
        margin-bottom: 1;
    }
    """

    gifts = {
        1: "React Workshop",
        2: "Fusion Workshop",
        3: "Onshape Keyring",
        4: "Hono Backend",
        5: "Flask Full Stack",
        6: "3D Printable Ruler",
        7: "Interactive Tree",
        8: "Cookie Clicker Bot",
        9: "Textual TUI",
        10: "No leeks",
        11: "Still no leeks",
        12: "Absolutely no leeks",
    }

    def __init__(self, day: int):
        self.day = day
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Day {self.day}")
            yield Label(self.gifts.get(self.day, "Surprise"))
            with Center():
                yield Button("Close", id="close")

    def on_button_pressed(self, event: Button.Pressed):
        self.dismiss()
        event.stop()


class AdventCalendarApp(App):

    CSS = """
    Screen {
        background: rgb(12,12,20);
    }

    Grid {
        grid-size: 6 2;
        grid-gutter: 1 1;
        padding: 2;
    }

    Grid Button {
        width: 100%;
        height: 100%;
        color: black;
    }

    Button.day1 { background: red; }
    Button.day2 { background: orange; }
    Button.day3 { background: yellow; }
    Button.day4 { background: green; }
    Button.day5 { background: cyan; }
    Button.day6 { background: blue; }
    Button.day7 { background: purple; }
    Button.day8 { background: pink; }
    Button.day9 { background: lime; }
    Button.day10 { background: gold; }
    Button.day11 { background: teal; }
    Button.day12 { background: violet; }

    Button.opened {
        background: rgb(0,180,110);
        color: white;
    }

    #counter {
        text-align: center;
        color: white;
        padding: 1;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark"),
        ("r", "reset_days", "Reset days"),
    ]

    START_DATE = datetime.date(2025, 12, 13)

    def compose(self) -> ComposeResult:
        yield Header()
        self.counter = Label("Opened days 0 / 12", id="counter")
        yield self.counter

        with Grid():
            for day in range(1, 13):
                btn = Button(str(day), id=f"day-{day}")
                btn.add_class(f"day{day}")
                yield btn

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        button = event.button
        day = int(button.id.split("-")[1])

        unlock_day = self.START_DATE + datetime.timedelta(days=day - 1)
        if datetime.date.today() < unlock_day:
            self.notify(f"Day {day} unlocks on {unlock_day}")
            return

        if not button.has_class("opened"):
            button.add_class("opened")
            self.update_counter()

        self.push_screen(DayScreen(day))

    def update_counter(self):
        opened = len(self.query("Button.opened"))
        self.counter.update(f"Opened days {opened} / 12")

    def action_reset_days(self):
        for button in self.query(Button):
            button.remove_class("opened")
        self.counter.update("Opened days 0 / 12")
        self.notify("All days reset")

    def action_toggle_dark(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"


def main():
    app = AdventCalendarApp()
    app.run()


if __name__ == "__main__":
    main()
#https://test.pypi.org/project/haxmas-day-9-hardikgupta2232/0.0.1/