import os
from enum import Enum

from constants.paths import LOG_DIR

from .base import get_timestamp


class LogType(Enum):
    INFO = 0
    ERR = 1
    OK = 2


def raw_log(log_type: LogType, message: str):
    return f"[{log_type.name if log_type in LogType else 'i'}] - {message}"


def console_log(log_type: LogType, message: str):
    print(raw_log(log_type, message))


def local_log(log_type: LogType, *, message: str, path: str = "dev.log"):
    with open(os.path.join(LOG_DIR, path), "a") as f:
        if log_type in LogType:
            f.write(f"{get_timestamp()}: [{log_type.name}] - {message}\n")
        else:
            f.write(f"{get_timestamp()}: [i] - {message}\n")
