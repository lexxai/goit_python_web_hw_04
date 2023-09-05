import logging
import time


def run():
    global logger
    logger = logging.getLogger(__name__)
    logger.info("Start Socket server")
    time.sleep(10)
    logger.info("Stop Socket server")


logger: logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    run()
