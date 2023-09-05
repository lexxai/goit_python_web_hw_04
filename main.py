from threading import Thread
from webapp import http_server, socket_server
import logging

def run_threads():
    logger.info("run_threads")
    threads = []
    th_socket_server = Thread(name="SOCKET SERVER", target=socket_server.run)
    th_socket_server.start()
    threads.append(th_socket_server)

    th_http_server = Thread(name="HTTP SERVER", target=http_server.run)
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