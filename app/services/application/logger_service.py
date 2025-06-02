import logging


class LoggerService:
    """
    Wrapper around the logger.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)
