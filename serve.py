#!/usr/bin/env python3
"""
Start a background HTTP server serving the `docs` directory on 127.0.0.1:8080.

Provides `start_server()` which returns `(server, thread)` so the caller
can continue executing Python code while the server runs in a daemon thread.

Usage:
    from serve import start_server, stop_server
    server, thread = start_server()
    # do other work here
    input("Press Enter to stop server...\n")
    stop_server(server)
    thread.join()
"""

from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
import os
import sys
import argparse


class BackgroundServer:
    """An HTTP server running in a background daemon thread for serving files from a directory."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080, directory: str = "docs"):
        """Start an HTTP server in a background daemon thread.

        Args:
            host: Address to bind to (default: 127.0.0.1)
            port: Port to bind to (default: 8080)
            directory: Directory to serve (default: docs)
        """
        handler = partial(SimpleHTTPRequestHandler, directory=directory)
        self.server = ThreadingHTTPServer((host, port), handler)
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True, name="http-server-thread"
        )
        self.thread.start()

    def stop(self):
        """Gracefully stop the server and wait for the thread to finish."""
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    @property
    def url(self) -> str:
        """Get the URL of the running server.

        Returns the full URL (e.g., http://127.0.0.1:8080/).
        """
        # server.server_address may be 2-tuple (host, port) for IPv4 or
        # 4-tuple for IPv6; pick the first two elements.
        srv_addr = self.server.server_address
        host = srv_addr[0]
        port = srv_addr[1]
        return f"http://{host}:{port}/"


def open_in_browser(url: str):
    """Open the given URL in the default web browser, if possible."""
    match sys.platform:
        case "win32":
            # getattr() to avoid AttributeError on non-Windows platforms
            startfile = getattr(os, "startfile", None)
            if startfile is not None:
                startfile(url)
            else:
                print(
                    f"Cannot open URL automatically on this platform. Please visit {url} manually."
                )
        case "darwin":
            os.system(f"open {url}")
        case "linux":
            os.system(f"xdg-open {url}")
        case x:
            print(f"Unsupported platform: {x}. Please visit {url} manually.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start a background HTTP server serving a directory"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind to (default: 8080)",
    )
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="Address to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--directory",
        default="docs",
        help="Directory to serve (default: docs)",
    )
    args = parser.parse_args()

    bg_server = BackgroundServer(
        host=args.bind, port=args.port, directory=args.directory
    )
    url = bg_server.url
    print(f"Serving directory '{args.directory}' at {url} (background thread)")

    open_in_browser(url)

    print("Press Enter to stop the server.")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass

    print("Shutting down server...")
    bg_server.stop()
    print("Server stopped.")
