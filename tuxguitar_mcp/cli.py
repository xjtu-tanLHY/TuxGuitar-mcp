from __future__ import annotations
import sys
import argparse
import json

from .server import mcp
from .song_editor import SongEditor
from .app_launcher import open_in_tuxguitar, get_tuxguitar_status


def main():
    parser = argparse.ArgumentParser(description="TuxGuitar AI MCP Tool CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the MCP server (stdio mode)")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Display score summary")
    summary_parser.add_argument("file", help="Path to score file (.tg or .gp5)")

    # Tab command
    tab_parser = subparsers.add_parser("tab", help="Render ASCII tablature")
    tab_parser.add_argument("file", help="Path to score file")
    tab_parser.add_argument("--track", type=int, default=1, help="Track number (1-based)")
    tab_parser.add_argument("--start", type=int, default=1, help="Start measure")
    tab_parser.add_argument("--end", type=int, default=4, help="End measure")

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert score file format")
    convert_parser.add_argument("input", help="Source score file")
    convert_parser.add_argument("output", help="Target score file (.tg or .gp5)")

    # Open command
    open_parser = subparsers.add_parser("open", help="Open score in TuxGuitar desktop")
    open_parser.add_argument("file", help="Path to score file")

    # Status command
    status_parser = subparsers.add_parser("status", help="Check TuxGuitar application status")

    args = parser.parse_args()

    if args.command is None or args.command == "serve":
        # Run FastMCP server
        mcp.run()
    elif args.command == "summary":
        ed = SongEditor(args.file)
        print(json.dumps(ed.get_summary(), indent=2, ensure_ascii=False))
    elif args.command == "tab":
        ed = SongEditor(args.file)
        print(ed.render_ascii(args.track, args.start, args.end))
    elif args.command == "convert":
        ed = SongEditor(args.input)
        out = ed.save(args.output, backup=False)
        print(f"Successfully converted: {args.input} -> {out}")
    elif args.command == "open":
        res = open_in_tuxguitar(args.file)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.command == "status":
        res = get_tuxguitar_status()
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
