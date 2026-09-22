from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .core import TYPES, compose, validate

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="commit-helper", description="Compose and validate Conventional Commit messages offline.")
    p.add_argument("--version", action="version", version="commit-helper 1.0.0 — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("compose", help="compose a commit message")
    c.add_argument("type", choices=TYPES); c.add_argument("description")
    c.add_argument("--scope"); c.add_argument("--breaking", action="store_true"); c.add_argument("--body")
    c.add_argument("--footer", action="append", default=[]); c.add_argument("--json", action="store_true")
    v = sub.add_parser("validate", help="validate a commit message")
    src = v.add_mutually_exclusive_group(required=True); src.add_argument("--message"); src.add_argument("--file", type=Path); src.add_argument("--stdin", action="store_true")
    v.add_argument("--max-header", type=int, default=72); v.add_argument("--strict", action="store_true"); v.add_argument("--json", action="store_true")
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "compose":
            msg = compose(args.type, args.description, scope=args.scope, breaking=args.breaking, body=args.body, footers=args.footer)
            print(json.dumps(msg.to_dict(), ensure_ascii=False, indent=2) if args.json else msg.render())
            return 0
        if args.max_header < 20 or args.max_header > 200:
            raise ValueError("--max-header must be between 20 and 200")
        if args.message is not None: text = args.message
        elif args.file is not None: text = args.file.read_text(encoding="utf-8")
        else: text = sys.stdin.read()
        result = validate(text, max_header=args.max_header, strict=args.strict)
        if args.json: print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("valid" if result.valid else "invalid")
            for item in result.errors: print(f"ERROR: {item}")
            for item in result.warnings: print(f"WARN: {item}")
        return 0 if result.valid else 1
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"commit-helper: {exc}", file=sys.stderr); return 2

if __name__ == "__main__": raise SystemExit(main())
