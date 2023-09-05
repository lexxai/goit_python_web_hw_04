import logging
import time
from pathlib import Path
import json


class DataStorage():
    BASE_STORAGE_DIR = Path()

    def save_data(self, data: dict):
        filename = self.BASE_STORAGE_DIR / "data.json"
        if not data:
            logger.error("save_data: Empty data")
            return 1
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
            except OSError as e:
                logger.error(e)


    def init_storage(self, storage: Path):
        self.BASE_STORAGE_DIR = storage
        if not storage.is_dir():
            logger.debug(f"init_storage : creating need folder: {storage}")
        storage.mkdir(parents=True, exist_ok=True)
        data_file = storage / "data.json"
        if not data_file.is_file():
            with open(data_file, "w", encoding="utf-8") as fp:
                json.dump({}, fp)

def run():
    global logger
    logger = logging.getLogger(__name__)
    storage = Path("storage/")
    data_storage = DataStorage()
    data_storage.init_storage(storage)
    logger.info("Start Socket server")
    time.sleep(10)
    logger.info("Stop Socket server")


logger: logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    run()
