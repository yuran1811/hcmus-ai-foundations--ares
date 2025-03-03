import os

import pygame as pg

from constants.enums import Direction
from constants.paths import ASSETS_PATH, CHARACTERS_PATH, FONTS_PATH


def load_spritesheet(
    file_path: str,
    *,
    frame_size: tuple[int, int],
    scale_factor: int,
    columns: int,
    direction_map: list[str],
    mirrored_pairs: list[tuple[str, str]] = [],
):
    """
    Load a spritesheet with automatic mirroring for directions
    Parameters:
        file_path: Path to spritesheet image
        frame_size: (width, height) of individual frames
        rows: Number of animation rows
        columns: Number of animation columns
        direction_map: List of direction names for each row (top to bottom)
        mirrored_pairs: List of tuples specifying mirrored directions (e.g., ('left', 'right'))
    """

    sheet = pg.image.load(file_path).convert_alpha()
    animations: dict[str, list[pg.Surface]] = {}

    frame_width, frame_height = frame_size
    scaled_size = (int(frame_width * scale_factor), int(frame_height * scale_factor))

    # Extract original directions
    for row, direction in enumerate(direction_map):
        frames = []
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height

            frame = pg.Surface(frame_size, pg.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))

            frames.append(pg.transform.scale(frame, scaled_size))

        animations[direction] = frames

    # Create mirrored versions
    if len(mirrored_pairs):
        for source, target in mirrored_pairs:
            if source in animations:
                animations[target] = [
                    pg.transform.flip(frame, True, False)
                    for frame in animations[source]
                ]

    return animations


def load_character_animations():
    return {
        "idle": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "idle.png"),
            frame_size=(80, 80),
            scale_factor=2,
            columns=4,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
        ),
        "walk": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "walk.png"),
            frame_size=(80, 80),
            scale_factor=2,
            columns=8,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
        ),
        "run": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "run.png"),
            frame_size=(80, 80),
            scale_factor=2,
            columns=4,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
        ),
    }


def get_frame_from_sprite(
    sheet: pg.Surface,
    index: int,
    frame_size: int,
    num_cols: int,
    *,
    scale_factor: int = 1,
):
    row = index // num_cols
    col = index % num_cols

    return pg.transform.scale(
        sheet.subsurface(
            (
                col * frame_size,
                row * frame_size,
                frame_size,
                frame_size,
            )
        ),
        (frame_size * scale_factor, frame_size * scale_factor),
    )


def get_asset_path(*args: str):
    return os.path.join(ASSETS_PATH, *args)


def get_font(*, font_name: str = "pixelify", size: int = 24):
    paths = {
        "pixelify": "Pixelify_Sans/static/PixelifySans-Regular.ttf",
        "pixeloperator": "PixelOperator8/PixelOperator8.ttf",
        "firacode": "FiraCode/FiraCode-Regular.ttf",
    }

    return pg.font.Font(
        os.path.join(FONTS_PATH, paths.get(font_name, "pixelify")), size
    )
