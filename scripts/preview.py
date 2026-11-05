#!/usr/bin/env python3
"""Preview the website from its actual root, regardless of the working directory."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8080, help="local port (default: 8080)")
    args = parser.parse_args()
    handler = partial(SimpleHTTPRequestHandler, directory=str(SITE_ROOT))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        parser.exit(1, f"Cannot start preview: {error}\nStop the existing server or choose --port 8081.\n")

    with server:
        print(f"Serving {SITE_ROOT}", flush=True)
        print(f"Open http://127.0.0.1:{server.server_port}/team/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
