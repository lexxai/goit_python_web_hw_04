from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse

BASE_ROOT_DIR = Path("../www-data")


class WWWHandler(BaseHTTPRequestHandler):

    def get_file(self, filename, state=200):
        self.send_response(state)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        filename = "index.html"
        with open(BASE_ROOT_DIR / filename, "rb") as fp:
            self.wfile.write(fp.read())         

    def do_GET(self):
        req_path = urllib.parse.urlparse(self.path).path
        match req_path:
            case '/':
                filename = 'index.html'
                self.get_file(filename)
            case _:
                filename = BASE_ROOT_DIR / req_path[1:]
                if  filename.exists():
                    self.get_file(filename)
                else:
                    filename = BASE_ROOT_DIR / 'error.html'
                    self.get_file(filename, 404)




def run(server=HTTPServer, handeler=WWWHandler):
    address = ('', 3000)
    http_server = server(address, handeler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == "__main__":
    run()



