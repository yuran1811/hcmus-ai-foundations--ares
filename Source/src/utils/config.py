import os

import tomllib

from config import SCREEN_SIZE
from constants.paths import ROOT_DIR

screen_size_change: tuple[int, int] = SCREEN_SIZE


def get_project_toml_data() -> dict:
    try:
        with open(os.path.join(ROOT_DIR, "pyproject.toml"), "rb") as f:
            return tomllib.load(f)["project"]
    except FileNotFoundError:
        return {}


def get_speed(speed: int, speed_up: bool):
    return min(16, speed << 1) if speed_up else max(1, speed >> 1)


def get_speed_cycle(speed: int, speed_up: bool):
    if speed == 0:
        return 1

    if speed_up and speed == 16:
        return 1

    if not speed_up and speed == 1:
        return 16

    return get_speed(speed, speed_up)


def get_screen_sz():
    return screen_size_change


def update_screen_sz(size: tuple[int, int]):
    global screen_size_change
    screen_size_change = (max(420, size[0]), max(400, size[1]))

    return screen_size_change


def get_screen_modes(idx: int | None = None):
    from pygame.display import get_desktop_sizes, list_modes

    default_modes = list_modes()[:-2]
    modes = [("w", "h"), (768, 456)] + get_desktop_sizes() + default_modes

    return modes if idx is None else [modes[idx]]
