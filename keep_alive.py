from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot calisıyor!")

    def log_message(self, format, *args):
        pass


def keep_alive():
    server = HTTPServer(("0.0.0.0", 5000), PingHandler)
    t = Thread(target=server.serve_forever)
    t.daemon = True
    t.start()
