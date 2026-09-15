from textual.widgets import DataTable

from database import save_event
from monitoring.monitor import get_connections


class ConnectionTable(DataTable):

    def __init__(self, interval: int, **kwargs):
        super().__init__(**kwargs)

        self.interval = interval

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True

        self.add_columns(
            "TIME",
            "PROCESS",
            "LOCAL",
            "REMOTE",
            "STATUS",
        )

    def refresh_connections(self) -> None:
        rows = get_connections()

        for row in rows:
            save_event(row)

        scroll_y = self.scroll_y

        self.clear()

        suspicious = 0

        for row in rows:

            status = row["status"]

            if status == "SUSPICIOUS":
                suspicious += 1

                status_text = (
                    f"[bold red]⚠ {status}[/bold red]"
                )

            else:
                status_text = (
                    f"[bold green]● {status}[/bold green]"
                )

            self.add_row(
                row["time"],
                row["process"][:20],
                row["local"][:19],
                row["remote"][:20],
                status_text,
            )

        self.scroll_y = scroll_y

        self.app.query_one(
            "#status"
        ).update(
            f"[bold cyan]Active:[/bold cyan] {len(rows)}    "
            f"[bold red]Suspicious:[/bold red] {suspicious}    "
            f"[dim]Update: {self.interval}s[/dim]"
        )