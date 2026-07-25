import logging
import sys
from pathlib import Path
from automation.config.config import LOGS_DIR

def setup_logger(name="AutomationLogger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler (UTF-8)
    log_file = LOGS_DIR / "execution.log"
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Console Handler (Safe UTF-8 stream)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logger = setup_logger()
