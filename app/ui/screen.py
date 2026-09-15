from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static

from ui.widgets.widget import ConnectionTable


class NetworkMonitorApp(App):

    CSS_PATH = "../styles/style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, interval: int):
        super().__init__()
        self.interval = interval

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True
        )

        yield Static(
            "Starting network monitor...",
            id="status"
        )

        yield ConnectionTable(
            interval=self.interval,
            id="connections"
        )

        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(
            self.interval,
            self.update_connections
        )

        self.update_connections()

    def update_connections(self) -> None:
        table = self.query_one(
            "#connections",
            ConnectionTable
        )

        table.refresh_connections()