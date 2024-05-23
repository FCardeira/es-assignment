import logging
import os
import sys
from settings import settings

log = logging.getLogger(__name__)

LOGGER_FORMAT = "%(levelname)s - %(asctime)s - %(process)d:%(thread)d [%(name)s.%(funcName)s:%(lineno)d] %(message)s"


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    blue = "\x1b[36m"
    format = "%(asctime)s - %(process)d:%(thread)d [%(name)s.%(funcName)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: f"{blue}%(levelname)s{reset}: {format}",
        logging.INFO: f"{green}%(levelname)s{reset}: {format}",
        logging.WARNING: f"{yellow}%(levelname)s{reset}: {format}",
        logging.ERROR: f"{red}%(levelname)s{reset}: {format}",
        logging.CRITICAL: f"{bold_red}%(levelname)s{reset}: {format}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger() -> None:
    log.debug("Setting up logger")
    log_directory = f"logs"
    # Create log directory if it does not exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # File handler
    file_formatter = logging.Formatter(LOGGER_FORMAT)
    file_handler = logging.FileHandler(
        filename=f"{log_directory}/app.log"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_formatter = logging.Formatter(LOGGER_FORMAT)
    console_handler = logging.StreamHandler(sys.stdout)

    if settings.IS_LOCAL:
        console_handler.setFormatter(CustomFormatter())
    else:
        console_handler.setFormatter(console_formatter)

    if settings.IS_LOCAL:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    logging.root.addHandler(console_handler)
    logging.root.addHandler(file_handler)
    logging.root.setLevel(logging.DEBUG if settings.IS_LOCAL else logging.INFO)

    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    # logging.getLogger("databases").setLevel(logging.WARNING)
