"""Task creation with durable, payload-bound request IDs."""
from contextlib import closing
from pathlib import Path
import re
import sqlite3


class Conflict(ValueError):
    pass


def validate(title, request_id):
    title = title.strip()
    if not title or len(title) > 120 or "\x00" in title:
        raise ValueError("title must contain 1 to 120 non-NUL characters")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", request_id):
        raise ValueError("request ID must contain 1 to 80 letters, digits, underscores or hyphens")
    return title


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL
            )""")

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA synchronous=FULL")
        return db

    def add(self, title, request_id):
        title = validate(title, request_id)
        with closing(self.connect()) as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                old = db.execute("SELECT id, title FROM tasks WHERE request_id = ?", (request_id,)).fetchone()
                if old:
                    if old["title"] != title:
                        raise Conflict("request ID was already used with another title")
                    result = {"task": dict(old), "created": False}
                else:
                    cursor = db.execute("INSERT INTO tasks(request_id, title) VALUES (?, ?)", (request_id, title))
                    result = {"task": {"id": cursor.lastrowid, "title": title}, "created": True}
                db.execute("COMMIT")
                return result
            except BaseException:
                db.execute("ROLLBACK")
                raise

    def list(self):
        with closing(self.connect()) as db:
            return [dict(row) for row in db.execute("SELECT id, title FROM tasks ORDER BY id")]
