from dataclasses import dataclass
from typing import Optional


SUSPICIOUS_PORTS = {
    21: "FTP",
    23: "Telnet",
    445: "SMB",
    1433: "MSSQL",
    1521: "Oracle DB",
    3306: "MySQL",
    3389: "RDP",
    4444: "Common Metasploit",
    5900: "VNC",
}


@dataclass
class Finding:
    status: str
    reason: Optional[str] = None


def analyze_remote_port(port: int | None) -> Finding:
    if port is None:
        return Finding(
            status="UNKNOWN",
            reason="Remote port unavailable",
        )

    if port in SUSPICIOUS_PORTS:
        service = SUSPICIOUS_PORTS[port]

        return Finding(
            status="SUSPICIOUS",
            reason=f"Port {port} ({service})",
        )

    return Finding(status="NORMAL")
