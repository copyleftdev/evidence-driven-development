"""Deliberately broken controls. Never used by the real CLI."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tiny_tasks.store import validate

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("volatile", "duplicates"), required=True)
parser.add_argument("--db", required=True)
commands = parser.add_subparsers(dest="command", required=True)
add = commands.add_parser("add")
add.add_argument("title")
add.add_argument("--request-id", required=True)
commands.add_parser("list")
args = parser.parse_args()
try:
    if args.command == "add":
        title = validate(args.title, args.request_id)
    if args.mode == "volatile":
        result = {"tasks": []} if args.command == "list" else {"task": {"id": 1, "title": title}, "created": True}
    else:
        # This persists each request but deliberately has no duplicate-request guard.
        with sqlite3.connect(args.db, timeout=10) as db:
            db.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT)")
            if args.command == "list":
                result = {"tasks": [{"id": row[0], "title": row[1]} for row in db.execute("SELECT id,title FROM tasks ORDER BY id")]}
            else:
                cursor = db.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
                result = {"task": {"id": cursor.lastrowid, "title": title}, "created": True}
    print(json.dumps(result, sort_keys=True))
except ValueError as error:
    print(json.dumps({"error": "invalid_input", "message": str(error)}, sort_keys=True))
    raise SystemExit(2)
