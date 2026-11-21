from __future__ import annotations

import argparse

import uvicorn

from pyquest.api.app import create_app
from pyquest.config import Settings


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pyquest", description="Python Terminal Quest CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="Start the PyQuest API and web server")
    serve_parser.add_argument("--host", default=None, help="Bind host")
    serve_parser.add_argument("--port", type=int, default=None, help="Bind port")

    args = parser.parse_args(argv)
    if args.command == "serve":
        settings = Settings()
        host = args.host or settings.host
        port = args.port or settings.port
        app = create_app(settings)
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
