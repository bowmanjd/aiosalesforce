"""Salesforce Session ID Bookmarklet Helper."""
import importlib.resources
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


def bookmarklet():
    """Reads the Javascript file and returns the full bookmarklet.

    Returns:
        The contents of the bookmarklet, ready to be installed
    """
    snippet = importlib.resources.read_text(__package__, "bookmarklet.js")
    return f"javascript:{snippet}"


def html():
    return importlib.resources.read_text(__package__, "bookmarklet.html")


class BookmarkletServer(BaseHTTPRequestHandler):
    def do_GET(self):
        javascript = bookmarklet()
        marklet = javascript.replace("\n", "").replace("  ", "")
        content = html().format(marklet=marklet, javascript=javascript)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


def run():
    if len(sys.argv) > 1:
        address, port = sys.argv[1].split(":")
        port = int(port)
    else:
        address = "localhost"
        port = 8888
    server = HTTPServer((address, port), BookmarkletServer)
    print(f"Go to\nhttp://{address}:{port}\nto install bookmarklet")
    server.handle_request()
