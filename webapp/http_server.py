from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes
import json
import logging
from datetime import datetime


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
            with open(filename, "r", encoding="utf-8") as fp:
                loaded_data: dict = json.load(fp)
        except OSError as e:
            logger.error(e)
      
        loaded_data.update(data)
        logger.debug(loaded_data)
        if loaded_data:
            try:
                with open(filename, "w", encoding="utf-8") as fp:
                    json.dump(loaded_data, fp)
            except OSError as e:
                logger.error(e)

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
        except Exception as e:
            logger.error(e)

    def do_POST(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/message":
                cont_len = int(self.headers["Content-Length"])
                data = self.rfile.read(cont_len).decode()
                data_parse = { 
                    key: urllib.parse.unquote_plus(val) for key, val in [ el.split("=") for el in data.split("&")]
                }
                timestamp = str(datetime.now())
                data_record = {
                    timestamp: data_parse
                }       

                try:
                    # print(data_parse)
                    json_data = json.dumps(data_record, ensure_ascii=False)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    result = json_data
                    self.wfile.write(result.encode())
                    logger.debug(f"{result}")
                    self.save_data(data_record)
                except Exception as e:
                     logger.error(e)
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
    if not storage.is_dir():
        logger.debug(f"init_storage : creating need folder: {storage}")
    storage.mkdir(parents=True, exist_ok=True)
    data_file = storage / "data.json"
    if not data_file.is_file():
        with open(data_file, "w", encoding="utf-8") as fp:
            json.dump({}, fp)


def run(server=HTTPServer, handler=WWWHandler):
    global logger
    logger = logging.getLogger(__name__)
    address = ("", 3000)
    www_root = Path("www-data/")
    storage = Path("storage/")
    init_storage(storage)
    handler.set_root(www_root, storage)
    http_server = server(address, handler)
    logger.info(f"Start HTTP server at port: {address[1]}")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
    except Exception as e:
        logger.error(e)
        http_server.server_close()

logger: logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    run()