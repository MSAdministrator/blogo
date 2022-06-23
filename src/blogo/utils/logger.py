# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

import logging
import logging.config
import os
from logging import DEBUG
from logging import FileHandler

import yaml


class DebugFileHandler(FileHandler):
    """Debug file handler."""

    def __init__(self, filename, mode="a", encoding=None, delay=False):
        """Instantiating a debug file handler.

        Args:
            filename (str): A filename
            mode (str, optional): Write mode.. Defaults to "a".
            encoding (str, optional): File encoding type. Defaults to None.
            delay (bool, optional): Delay write or read of file. Defaults to False.
        """
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        """Emits logs to a configured source.

        Args:
            record (dict): A record object.
        """
        if not record.levelno == DEBUG:
            return
        super().emit(record)


class LoggingBase(type):
    """Logging meta class."""

    def __init__(cls, *args):
        """Setting up meta class arguments."""
        super().__init__(*args)
        cls.setup_logging()

        # Explicit name mangling
        logger_attribute_name = "_" + cls.__name__ + "__logger"

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = ".".join([c.__name__ for c in cls.mro()[-2::-1]])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))

    def setup_logging(cls, default_path="./blogo/data/logging.yml", default_level=logging.INFO, env_key="LOG_CFG"):
        """Setup logging configuration."""
        path = os.path.abspath(os.path.expanduser(os.path.expandvars(default_path)))
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(os.path.abspath(path)):
            with open(path) as f:
                config = yaml.safe_load(f.read())
            logger = logging.config.dictConfig(config)
        else:
            logger = logging.basicConfig(level=default_level)
