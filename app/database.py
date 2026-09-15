import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "monitor.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                pid INTEGER,
                process TEXT,
                local_address TEXT,
                remote_address TEXT,
                status TEXT NOT NULL,
                reason TEXT,
                protocol_family TEXT,
                connection_type TEXT
            )
        """)


def save_event(event):
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            INSERT INTO events (
                timestamp,
                pid,
                process,
                local_address,
                remote_address,
                status,
                reason,
                protocol_family,
                connection_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["time"],
            event["pid"],
            event["process"],
            event["local"],
            event["remote"],
            event["status"],
            event["reason"],
            event["family"],
            event["type"],
        ))


def get_recent_events(limit=50):
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row

        rows = db.execute("""
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]