import importlib.resources
from http.server import HTTPServer, BaseHTTPRequestHandler


def bookmarklet():
    js = importlib.resources.read_text(__package__, "bookmarklet.js")
    return f"javascript:{js}"


class Marklet(BaseHTTPRequestHandler):
    def do_GET(s):
        js = bookmarklet()
        # marklet = "".join(js.split())
        marklet = js.replace("\n", "").replace("  ", "")
        content = (
            f'<a href="{marklet}">SF Session ID</a>\n'
            "<p>Drag the above to your bookmarks.</p>\n"
            "<p>To use, go to the relevant Salesforce org and click twice on the bookmarklet.</p>\n"
            f"<pre>{marklet}</pre>\n"
            f"<pre><code>{js}</code></pre>"
        )
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(content.encode())


def run():
    server = HTTPServer(("", 8888), Marklet)
    print("Go to http://localhost:8888 to install bookmarklet")
    server.serve_forever()
