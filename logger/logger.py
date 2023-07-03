import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        self.log_format = "%(asctime)s - %(levelname)s - %(message)s"
        self.log_level = logging.DEBUG
        self.log_directory = os.path.join(os.getcwd(), 'logs')
        self.log_file = os.path.join(self.log_directory, 'app.log')

    def configure_logging(self):
        # Create the log directory if it doesn't exist
        os.makedirs(self.log_directory, exist_ok=True)

        # Create and configure the logger
        logging.basicConfig(level=self.log_level, format=self.log_format)

        # Add a rotating file handler for log file rotation
        file_handler = RotatingFileHandler(self.log_file, mode='a', maxBytes=1024 * 1024, backupCount=5)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(logging.Formatter(self.log_format))

        # Add the file handler to the logger
        logger = logging.getLogger()
        logger.addHandler(file_handler)

    def log_message(self, message, level=logging.INFO):
        logger = logging.getLogger()
        logger.log(level, message)

    def log_exception(self, message):
        logger = logging.getLogger()
        logger.exception(message)

    def log_info(self, message):
        self.log_message(message, level=logging.INFO)

    def log_warning(self, message):
        self.log_message(message, level=logging.WARNING)

    def log_error(self, message):
        self.log_message(message, level=logging.ERROR)

    def log_debug(self, message):
        self.log_message(message, level=logging.DEBUG)
