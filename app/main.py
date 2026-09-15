import argparse

from database import init_db
from ui.screen import NetworkMonitorApp


def main():
    parser = argparse.ArgumentParser(
        description="Local Network Security Monitor"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Seconds between scans. Default: 5",
    )

    args = parser.parse_args()

    init_db()

    app = NetworkMonitorApp(
        interval=max(1, args.interval)
    )

    app.run()


if __name__ == "__main__":
    main()