import logging
import sys


def create_logger() -> logging.Logger:
    """
        Set up and cache a logger.

        return:
        - Logger: Configured logger instance.
    """

    logger = logging.getLogger("rpn-calculator")
    logger.setLevel(logging.INFO)
    log_format = f"%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
