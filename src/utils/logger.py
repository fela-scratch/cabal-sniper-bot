"""
Logging utilities for the pump.fun trading bot.
"""

import logging
import platform

# Global dict to store loggers
_loggers: dict[str, logging.Logger] = {}

# Detect if running on Windows (which has limited emoji support in console)
_IS_WINDOWS = platform.system() == "Windows"


def safe_emoji(emoji: str, text_fallback: str) -> str:
    """Return emoji on non-Windows systems, text fallback on Windows.

    This prevents UnicodeEncodeError on Windows Command Prompt which uses cp1252.

    Args:
        emoji: Emoji character(s)
        text_fallback: Text fallback for Windows systems

    Returns:
        Emoji on Unix/macOS, text fallback on Windows
    """
    return text_fallback if _IS_WINDOWS else emoji


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Get or create a logger with the given name.

    Args:
        name: Logger name, typically __name__
        level: Logging level

    Returns:
        Configured logger
    """
    global _loggers

    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    _loggers[name] = logger
    return logger


def setup_file_logging(
    filename: str = "pump_trading.log", level: int = logging.INFO
) -> None:
    """Set up file logging for all loggers.

    Args:
        filename: Log file path
        level: Logging level for file handler
    """
    root_logger = logging.getLogger()

    # Check if file handler with same filename already exists
    for handler in root_logger.handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and handler.baseFilename == filename
        ):
            return  # File handler already added

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
