from threading import Thread
from webapp.app import run
import logging

def run_threads():
    logger.info("run_threads")
    threads = []
    th_http_server = Thread(name="WEB SERVER", target=run)
    th_http_server.start()
    threads.append(th_http_server)

    logger.info("wait finish servers threads")
    [th.join() for th in threads]

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    logger = logging.getLogger(__name__)
    run_threads()