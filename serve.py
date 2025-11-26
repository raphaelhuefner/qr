#!/usr/bin/env python3
"""
Start a background HTTP server serving the `static` directory on 127.0.0.1:8080.

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


def start_server(host: str = "127.0.0.1", port: int = 8080, directory: str = "static"):
    """Start an HTTP server in a background daemon thread.

    Returns (server, thread). Call `server.shutdown()` and `server.server_close()`
    to stop the server, then `thread.join()` to wait for the thread to exit.
    """
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    server = ThreadingHTTPServer((host, port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True, name="http-server-thread")
    thread.start()
    return server, thread


def stop_server(server: ThreadingHTTPServer):
    """Gracefully stop the given server."""
    server.shutdown()
    server.server_close()


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
        default="static",
        help="Directory to serve (default: static)",
    )
    args = parser.parse_args()

    server, thread = start_server(
        host=args.bind, port=args.port, directory=args.directory
    )
    # server.server_address may be 2-tuple (host, port) for IPv4 or
    # 4-tuple for IPv6; pick the first two elements for printing.
    srv_addr = server.server_address
    host = srv_addr[0]
    port = srv_addr[1]
    url = f"http://{host}:{port}/"
    print(f"Serving directory 'static' at {url} (background thread)")

    # Open URL in default browser
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

    print("Press Enter to stop the server.")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass

    print("Shutting down server...")
    stop_server(server)
    thread.join()
    print("Server stopped.")
