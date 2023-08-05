import logging
from typing import Dict, Optional


class Logger:
    """Wrapper for the logger."""

    _instances: Dict[str, logging.Logger] = {}

    @staticmethod
    def initialize(level: str) -> None:
        """Initialize the logger with given log level.

        Once this is done, the log can be fetched using `get_logger` method.

        Arguments:
            level (str): The level to set in the logger.
        """
        logging.basicConfig(level=level, format="%(levelname)s - %(message)s")

    @staticmethod
    def get_logger(name: Optional[str] = "app") -> logging.Logger:
        """
        Get the instance of the logger with given name.

        Arguments:
            name (str): The name of the logger to fetch.

        Returns:
            (logging.Logger)
        """
        if name not in Logger._instances:
            Logger._instances[name] = logging.getLogger(name)

        return Logger._instances[name]
