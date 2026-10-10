import argparse
import json
from pathlib import Path
import sqlite3

from .store import Conflict, Store


def main():
    parser = argparse.ArgumentParser(description="Tiny Tasks: a local list with safe create retries")
    parser.add_argument("--db", type=Path, default=Path(".local/tasks.sqlite"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    add.add_argument("--request-id", required=True)
    commands.add_parser("list")
    args = parser.parse_args()
    try:
        store = Store(args.db)
        result = store.add(args.title, args.request_id) if args.command == "add" else {"tasks": store.list()}
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, sqlite3.Error, OSError) as error:
        code = "conflict" if isinstance(error, Conflict) else "invalid_input" if isinstance(error, ValueError) else "storage_error"
        print(json.dumps({"error": code, "message": str(error)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
