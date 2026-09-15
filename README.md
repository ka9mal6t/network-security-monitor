# Network Security Monitor

A local terminal dashboard for inspecting active network connections, identifying connections that use commonly risky remote ports, and storing scan results in SQLite.

The application is built with Python, `psutil`, `Textual`, and SQLite. It runs locally and does not send connection data to an external service.

## Features

- Lists active IPv4 and IPv6 internet connections.
- Shows the time, process, local endpoint, remote endpoint, and status of each connection.
- Resolves the process name when permissions allow it.
- Flags remote connections that use ports commonly associated with insecure or administrative services.
- Refreshes the dashboard automatically at a configurable interval.
- Stores every scan result in `data/monitor.db`.
- Preserves the table's vertical scroll position when the table refreshes.
- Uses color-coded status indicators in the Textual interface.

## Detection Rules

A connection is marked `SUSPICIOUS` when its remote port is in the following list:

| Port | Service or reason |
| ---: | --- |
| 21 | FTP |
| 23 | Telnet |
| 445 | SMB |
| 1433 | Microsoft SQL Server |
| 1521 | Oracle Database |
| 3306 | MySQL |
| 3389 | RDP |
| 4444 | Common Metasploit port |
| 5900 | VNC |

All other connections with a known remote port are marked `NORMAL`.

## Requirements

- Python 3.10 or newer
- Permission to inspect local network connections and process information
- A terminal that supports the Textual interface

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/ka9mal6t/network-security-monitor
cd network-security-monitor
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux or macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```bash
python app/main.py
```

The default refresh interval is 5 seconds. To use a different interval, pass `--interval`:

```bash
python app/main.py --interval 10
```

The interval is clamped to a minimum of one second.

Press `q` to quit the dashboard.

On some systems, inspecting every process may require elevated permissions. When process information is unavailable, the application displays the process ID or `N/A` instead of stopping the scan.

## Data Storage

The application creates the SQLite database automatically at:

```text
data/monitor.db
```

The database contains an `events` table with the following information:

- Timestamp
- Process ID and process name
- Local and remote addresses
- Detection status and reason
- Protocol family
- Connection type

The database file is ignored by Git because it contains local monitoring data. Remove it when you want to start with an empty history; it will be recreated on the next launch.

## Project Structure

```text
network-security-monitor/
├── app/
│   ├── main.py                 # CLI entry point and refresh interval
│   ├── database.py             # SQLite initialization and event storage
│   ├── monitoring/
│   │   ├── monitor.py          # Reads active connections with psutil
│   │   └── detector.py         # Remote-port detection rules
│   ├── ui/
│   │   ├── screen.py           # Textual application and layout
│   │   └── widgets/
│   │       └── widget.py       # Live connection table
│   └── styles/
│       └── style.tcss          # Textual styles
├── data/                       # Local SQLite database files
├── requirements.txt            # Python dependencies
└── README.md
```

## Troubleshooting

### The application does not start

Make sure the virtual environment is active and dependencies are installed:

```bash
python -m pip install -r requirements.txt
```

Run the command from the repository root so that imports such as `database` and `ui.screen` resolve correctly.

### Some processes show as `N/A` or only a PID

The operating system may deny access to process information. Try running the terminal with appropriate permissions if you need full process names.

### The connection list is empty

The monitor only displays connections that have a remote address. Listening sockets and local-only connections are intentionally excluded.

## Scope and Limitations

This project is a local visibility and triage tool, not a complete intrusion detection system. A flagged port does not prove malicious activity, and a normal status does not guarantee that a connection is safe. Use the results as a starting point for further investigation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that the copyright notice and permission notice are included in all copies or substantial portions of the software.
