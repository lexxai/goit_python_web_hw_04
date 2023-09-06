import logging
from pathlib import Path
import json
import socket


class DataStorage():
    BASE_STORAGE_DIR = Path()
    STORAGE_FILE = "data.json"

    def save_data(self, data: dict) -> bool:
        result = None
        filename = self.BASE_STORAGE_DIR / self.STORAGE_FILE
        if not data:
            logger.error("save_data: Empty data")
            return None
        if not filename.is_file():
            logger.error(f"save_data: json file is not exist - {filename}")
            return None 
        try:
            with open(filename, "r", encoding="utf-8") as fp:
                loaded_data: dict = json.load(fp)
        except OSError as e:
            logger.error(e)
      
        loaded_data.update(data)
        # logger.debug(loaded_data)
        if loaded_data:
            try:
                with open(filename, "w", encoding="utf-8") as fp:
                    json.dump(loaded_data, fp, ensure_ascii=False, indent=4)
                    result = True
            except OSError as e:
                logger.error(e)
        return result


    def init_storage(self, storage: Path):
        self.BASE_STORAGE_DIR = storage
        if not storage.is_dir():
            logger.debug(f"init_storage : creating need folder: {storage}")
        storage.mkdir(parents=True, exist_ok=True)
        data_file = storage / "data.json"
        if not data_file.is_file():
            with open(data_file, "w", encoding="utf-8") as fp:
                json.dump({}, fp)


## RUN SOCKET SERVER

def run_socket_server(ip, port, data_storage: DataStorage):
    sock = socket.socket(type=socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            decoded = json.loads(data)
            result = data_storage.save_data(decoded)
            if result:
                data = {"STATUS": "OK"}
            else:
                data = {"STATUS": "ERROR"}

            data = json.dumps(data, ensure_ascii=False)

            logger.info(f'Received data: {decoded} from: {address}')
            sock.sendto(data.encode(), address)
            logger.info(f'Send data: {data} to: {address}')

    except KeyboardInterrupt:
        logger.info(f'Destroy server')
    finally:
        sock.close()


def run(ip=socket.gethostname(), port=3001):
    global logger
    logger = logging.getLogger(__name__)
    storage = Path("storage/")
    data_storage = DataStorage()
    data_storage.init_storage(storage)
    logger.info("Start Socket server")

    run_socket_server(ip, port, data_storage)

    logger.info("Stop Socket server")


logger: logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    run()
