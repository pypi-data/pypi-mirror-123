import logging
import os
from pathlib import Path

import colorlog

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_log_dir = Path("logs/")

if not _log_dir.is_dir():
    os.mkdir(_log_dir)

_debug_log_fp: Path = _log_dir / "debug.log"
_error_log_fp: Path = _log_dir / "error.log"

_fh1 = logging.FileHandler(_debug_log_fp, mode="a")
_fh1.setLevel(logging.DEBUG)

_fh2 = logging.FileHandler(_error_log_fp, mode="a")
_fh2.setLevel(logging.ERROR)

_sh = colorlog.StreamHandler()
_sh.setLevel(logging.DEBUG)

# define formatter for logger file output
_formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)-8s | %(filename)s:%(lineno)s | %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# define formatter for logger console output
_color_formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s %(black)s(%(filename)s:%(lineno)s)",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_yellow",
    },
    secondary_log_colors={},
    style="%",
)

# Set the formatter for each handler
_fh1.setFormatter(_formatter)
_fh2.setFormatter(_formatter)
_sh.setFormatter(_color_formatter)

# Add all three handlers to the logger
logger.addHandler(_fh1)
logger.addHandler(_fh2)
logger.addHandler(_sh)

if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is a message for your information")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical error message")
