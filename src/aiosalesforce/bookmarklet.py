import importlib.resources
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
    server = HTTPServer(("", 8888), Marklet)
    print("Go to http://localhost:8888 to install bookmarklet")
    server.handle_request()
