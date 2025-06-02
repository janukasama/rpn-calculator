from app.utils.config import ConfigLoader
from app.utils.logger import create_logger
from app.services.application.logger_service import LoggerService


def boot_services():
    """
    Bootstraps all services and returns them.
    """
    config = ConfigLoader.load()
    logger = create_logger()

    logger_service = LoggerService(logger)

    return {
        "config": config,
        "logger": logger_service
    }
