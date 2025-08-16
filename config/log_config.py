import logging
from pydantic import BaseModel
from logging.config import dictConfig


class LogConfig(BaseModel):
    LOGGER_NAME: str = "mylogger"
    LOG_FORMAT: str = "%(levelprefix)s %(message)s"
    LOG_LEVEL: str = "DEBUG"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {"()": "uvicorn.logging.DefaultFormatter", "fmt": LOG_FORMAT},
    }

    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    }

    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().model_dump())
logger = logging.getLogger("mylogger")
