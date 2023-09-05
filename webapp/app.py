from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes
import json


class WWWHandler(BaseHTTPRequestHandler):
    BASE_ROOT_DIR = Path()
    BASE_STORAGE_DIR = Path()

    @staticmethod
    def set_root(path: Path, storage_path: Path = None):
        WWWHandler.BASE_ROOT_DIR = path
        if storage_path:
            WWWHandler.BASE_STORAGE_DIR = storage_path


    def save_data(self, data):
        filename = self.BASE_STORAGE_DIR / "data.json"
        try:
            with open(filename, "a", encoding="utf-8") as fp:
                fp.write(str(data))
                fp.write("\n")
        except OSError as e:
            print(e)

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
            with open(filename, "rb") as fp:
                self.wfile.write(fp.read())
        except FileNotFoundError as e:
            print(e)

    def do_POST(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/message":
                cont_len = int(self.headers["Content-Length"])
                data = self.rfile.read(cont_len).decode()
                data_parse = { 
                    key: urllib.parse.unquote_plus(val) for key, val in [ el.split("=") for el in data.split("&")]
                }
                try:
                    # print(data_parse)
                    json_data = json.dumps(data_parse, ensure_ascii=False)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    result = json_data
                    self.wfile.write(result.encode())
                    print(f"{result}")
                    self.save_data(json_data)
                except Exception as e:
                     print(e)
            case _:
                self.send_response(301)
                self.send_header("Location", "/error.html")
                self.end_headers()


    def do_GET(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/":
                filename = self.BASE_ROOT_DIR / "index.html"
                self.get_file(filename)
            case _:
                filename = self.BASE_ROOT_DIR / route_path.path[1:]
                if filename.exists():
                    self.get_file(filename)
                else:
                    filename = self.BASE_ROOT_DIR / "error.html"
                    self.get_file(filename, 404)

def init_storage(storage: Path):
    storage.mkdir(parents=True, exist_ok=True)
    data_file = storage / "data.json"
    data_file.touch(exist_ok=True)


def run(server=HTTPServer, handler=WWWHandler):
    address = ("", 3000)
    storage = Path("storage/")
    init_storage(storage)
    handler.set_root(Path("www-data/"), storage)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == "__main__":
    run()
