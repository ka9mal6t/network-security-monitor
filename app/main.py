import argparse
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Header, Static

from database import init_db, save_event
from monitor import get_connections


class NetworkMonitor(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    #status {
        height: 3;
        padding: 1;
    }

    #connections {
        height: 1fr;
    }

    DataTable {
        height: 1fr;
    }
    """

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

        yield DataTable(
            id="connections",
            cursor_type="row",
            zebra_stripes=True,
        )

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(
            "#connections",
            DataTable
        )

        table.add_columns(
            "TIME",
            "PROCESS",
            "LOCAL",
            "REMOTE",
            "STATUS",
        )

        self.update_connections()

        self.set_interval(
            self.interval,
            self.update_connections
        )

    def update_connections(self) -> None:
        rows = get_connections()

        for row in rows:
            save_event(row)

        table = self.query_one(
            "#connections",
            DataTable
        )

        # Сохраняем текущую позицию прокрутки
        scroll_y = table.scroll_y

        table.clear()

        suspicious = 0

        for row in rows:

            status = row["status"]

            if status == "SUSPICIOUS":
                suspicious += 1
                status_text = f"⚠ {status}"
            else:
                status_text = status

            table.add_row(
                row["time"],
                row["process"][:20],
                row["local"][:19],
                row["remote"][:20],
                status_text,
            )

        status_widget = self.query_one(
            "#status",
            Static
        )

        status_widget.update(
            f"Active remote connections: {len(rows)}    "
            f"Suspicious connections: {suspicious}    "
            f"Update interval: {self.interval}s"
        )

        # Возвращаем пользователя туда, где он был
        table.scroll_y = scroll_y


def main():
    parser = argparse.ArgumentParser(
        description="Local Network Security Monitor"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between scans. Default: 60",
    )

    args = parser.parse_args()

    init_db()

    app = NetworkMonitor(
        interval=max(1, args.interval)
    )

    app.run()


if __name__ == "__main__":
    main()