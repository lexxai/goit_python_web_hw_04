from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

BASE_ROOT_DIR = Path("../www-data")


class WWWHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        filename = "index.html"
        with open(BASE_ROOT_DIR / filename, "rb") as fp:
            self.wfile.write(fp.read()) 



def run(server=HTTPServer, handeler=WWWHandler):
    address = ('', 3000)
    http_server = server(address, handeler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == "__main__":
    run()



