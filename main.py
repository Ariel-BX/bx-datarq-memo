import time
import threading

from src.service.logger.json_logger_service import LoggerService
from src.application.messages_processors import MessagesProcessor
from src.service.healthcheck.server import run_health_check_server

def main():
    logger_service = LoggerService()
    logger_service.log(message='Application started')
    proccesor = MessagesProcessor(logger_service)
    while True:
        proccesor.start_consuming_messages()
if __name__ == '__main__':
    threading.Thread(target=run_health_check_server, daemon=True).start()
    main()
