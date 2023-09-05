from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes


class WWWHandler(BaseHTTPRequestHandler):
    BASE_ROOT_DIR = Path()

    @staticmethod
    def set_root(path: Path):
        WWWHandler.BASE_ROOT_DIR = path

    def get_file(self, filename, state=200):
        # print(f"{self.BASE_ROOT_DIR=}")
        self.send_response(state)
        mmtype, _ = mimetypes.guess_type(filename)
        if mmtype:
            self.send_header("Content-Type", mmtype)
        else:
            self.send_header("Content-Type", "plain/text")
        self.end_headers()
        try:
            with open(self.BASE_ROOT_DIR / filename, "rb") as fp:
                self.wfile.write(fp.read())
        except FileNotFoundError as e:
            print(e)

    def do_GET(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/":
                filename = "index.html"
                self.get_file(filename)
            case _:
                filename = self.BASE_ROOT_DIR / route_path.pat[1:]
                if filename.exists():
                    self.get_file(filename)
                else:
                    filename = self.BASE_ROOT_DIR / "error.html"
                    self.get_file(filename, 404)


def run(server=HTTPServer, handler=WWWHandler):
    address = ("", 3000)
    handler.set_root(Path("../www-data"))
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == "__main__":
    run()
