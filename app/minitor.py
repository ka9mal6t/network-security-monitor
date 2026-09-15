import psutil
from datetime import datetime

from detector import analyze_remote_port


def get_connections():
    rows = []

    for conn in psutil.net_connections(kind="inet"):

        # Only connections with a remote address are relevant.
        if not conn.raddr:
            continue

        remote_ip = conn.raddr.ip
        remote_port = conn.raddr.port

        if conn.laddr:
            local = f"{conn.laddr.ip}:{conn.laddr.port}"
        else:
            local = "-"

        remote = f"{remote_ip}:{remote_port}"

        # Determine which process is using the connection.
        process = "N/A"

        if conn.pid:
            try:
                process = psutil.Process(conn.pid).name()

            except psutil.NoSuchProcess:
                process = f"PID {conn.pid}"

            except psutil.AccessDenied:
                process = f"PID {conn.pid}"

        # Pass the remote port to our Security Detector.
        finding = analyze_remote_port(remote_port)

        rows.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "pid": conn.pid,
            "process": process,
            "local": local,
            "remote": remote,
            "status": finding.status,
            "reason": finding.reason or "",
            "family": str(conn.family).split(".")[-1],
            "type": str(conn.type).split(".")[-1],
        })

    return rows
