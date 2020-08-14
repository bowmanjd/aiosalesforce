import importlib.resources
import webbrowser
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# javascript:(() => {let apipath='/services/data/'; if (location.pathname === apipath) {let sessid = (';' + document.cookie).split("; sid=")[1].split("; ")[0]; let domain = location.host; let output = JSON.stringify([domain,sessid]); navigator.clipboard.writeText(output);} else {window.open(location.origin + apipath, "_blank");}})();

HTML = ()


def bookmarklet():
    js = importlib.resources.read_text(__package__, "bookmarklet.js")
    return f"javascript:{js}"


def html():
    return importlib.resources.read_text(__package__, "bookmarklet.html")


class Marklet(BaseHTTPRequestHandler):
    def do_GET(s):
        js = bookmarklet()
        # marklet = "".join(js.split())
        marklet = js.replace("\n", "").replace("  ", "")
        content = html().format(marklet=marklet, js=js)
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(content.encode())


def run():
    if len(sys.argv) > 1:
        address, port = sys.argv[1].split(":")
        port = int(port)
    else:
        address = "localhost"
        port = 8888
    server = HTTPServer((address, port), Marklet)
    print(f"Go to\nhttp://{address}:{port}\nto install bookmarklet")
    server.handle_request()
