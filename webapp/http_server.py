from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes
import json
import logging
from datetime import datetime
import socket


class SocketClient():

    def __init__(self, ip = socket.gethostname(), port = 3001) -> None:
        self.UDP_IP = ip
        self.UDP_PORT = port

    def run_socket_client(self, message: str) -> bool:
        result = False
        try:
            sock = socket.socket(type=socket.SOCK_DGRAM)
            server = self.UDP_IP, self.UDP_PORT
            if message:
                data = message.encode()
                sock.sendto(data, server)
                # logger.info(f'Send data: {data.decode()} to server: {server}')
                response, address = sock.recvfrom(1024)
                status = json.loads(response)
                if status.get("STATUS") == "OK":
                    logger.info(f'SAVED OK')
                    result = True
                else:
                    logger.error(f'ERROR ON SAVING')
        except Exception as e:
             logger.error(e)
        finally:
            sock.close()
        return result



class WWWHandler(BaseHTTPRequestHandler):
    BASE_ROOT_DIR = Path()
    socket_client = None

    @staticmethod
    def set_root(path: Path, socket_client: SocketClient = None):
        WWWHandler.BASE_ROOT_DIR = path
        if socket_client:
            WWWHandler.socket_client = socket_client


    def save_data(self, data: dict) -> bool:
        json_data = json.dumps(data, ensure_ascii=False)
        result = self.socket_client.run_socket_client(json_data)
        return result



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

    def parse_message(self, data: str) -> bool:
        result = None
        data_parse = { 
            key: urllib.parse.unquote_plus(val) for key, val in [ el.split("=") for el in data.split("&")]
        }
        timestamp = str(datetime.now())
        data_record = {
            timestamp: data_parse
        }       
        try:
            json_data = json.dumps(data_record, ensure_ascii=False)
            logger.debug(f"parse_message: {json_data}")
            result = self.save_data(data_record)
        except Exception as e:
                logger.error(e)
        return result


    def do_POST(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/message":
                cont_len = int(self.headers["Content-Length"])
                data = self.rfile.read(cont_len).decode()
                result = self.parse_message(data)
                location = "/message_done.html" if result else "/error.html"
                self.send_response(301)
                self.send_header("Location", location)
                self.end_headers()

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


def run(server=HTTPServer, handler=WWWHandler):
    global logger
    logger = logging.getLogger(__name__)
    address = ("", 3000)
    www_root = Path("www-data/")
    socket_client = SocketClient()
    handler.set_root(www_root, socket_client)
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
