import os

import pygame as pg

<<<<<<< HEAD
from constants.enums import Direction
from constants.paths import ASSETS_PATH, CHARACTERS_PATH, FONTS_PATH
=======
from constants.paths import ASSETS_PATH, CHARACTERS_PATH
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d


def load_spritesheet(
    file_path: str,
    *,
    frame_size: tuple[int, int],
    scale_factor: float,
    columns: int,
    direction_map: list[str],
<<<<<<< HEAD
    mirrored_pairs: list[tuple[str, str]] = [],
=======
    mirrored_pairs=None,
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
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
<<<<<<< HEAD
    scaled_size = (int(frame_width * scale_factor), int(frame_height * scale_factor))
=======

    #  scaling transformation
    scaled_size = (int(frame_size[0] * scale_factor), int(frame_size[1] * scale_factor))
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

    # Extract original directions
    for row, direction in enumerate(direction_map):
        frames = []
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height

            frame = pg.Surface(frame_size, pg.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))

<<<<<<< HEAD
            frames.append(pg.transform.scale(frame, scaled_size))
=======
            scaled_frame = pg.transform.scale(frame, scaled_size)
            frames.append(scaled_frame)
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

        animations[direction] = frames

    # Create mirrored versions
<<<<<<< HEAD
    if len(mirrored_pairs):
        for source, target in mirrored_pairs:
            if source in animations:
                animations[target] = [
                    pg.transform.flip(frame, True, False)
                    for frame in animations[source]
                ]
=======
    if mirrored_pairs:
        for source, target in mirrored_pairs:
            if source in animations:
                mirrored_frames = [
                    pg.transform.flip(frame, True, False)
                    for frame in animations[source]
                ]
                animations[target] = mirrored_frames
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

    return animations


def load_character_animations():
    return {
        "idle": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "idle.png"),
            frame_size=(80, 80),
<<<<<<< HEAD
            scale_factor=2,
            columns=4,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
=======
            scale_factor=2.5,
            columns=4,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
        ),
        "walk": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "walk.png"),
            frame_size=(80, 80),
<<<<<<< HEAD
            scale_factor=2,
            columns=8,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
=======
            scale_factor=2.5,
            columns=8,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
        ),
        "run": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "run.png"),
            frame_size=(80, 80),
<<<<<<< HEAD
            scale_factor=2,
            columns=4,
            direction_map=[
                Direction.RIGHT.value[1],
                Direction.DOWN.value[1],
                Direction.UP.value[1],
            ],
            mirrored_pairs=[(Direction.RIGHT.value[1], Direction.LEFT.value[1])],
=======
            scale_factor=2.5,
            columns=4,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
        ),
    }


<<<<<<< HEAD
def get_frame_from_sprite(
    sheet: pg.Surface,
    index: int,
    frame_size: float,
    num_cols: int,
    *,
    scale_factor: float = 1.0,
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
=======
def load_tile_sprites(path: str, tile_width=16, tile_height=16):
    """
    Load a tile-based (tile-based) sprite sheet and split into sub-tiles.
    Returns a dictionary of tile surfaces keyed by an index.
    """

    # 🖼️ Load the full sprite sheet
    sheet = pg.image.load(path).convert_alpha()

    # 📐 Calculate how many tiles fit horizontally & vertically
    sheet_width, sheet_height = sheet.get_size()
    tiles_x = sheet_width // tile_width
    tiles_y = sheet_height // tile_height

    # 🗂️ Dictionary (dictionary) to hold tile surfaces
    tile_dict = {}
    tile_id = 1  # or 0, depending on how you want to index

    # 🧩 Slice each sub-tile from the sprite sheet
    for row in range(tiles_y):
        for col in range(tiles_x):
            # Create a new surface for each tile
            tile_surface = pg.Surface((tile_width, tile_height), pg.SRCALPHA)

            # Blit the tile image from the sheet
            tile_surface.blit(
                sheet,
                (0, 0),
                (col * tile_width, row * tile_height, tile_width, tile_height),
            )

            # Store in dictionary with a unique ID
            tile_dict[tile_id] = tile_surface
            tile_id += 1

    return tile_dict


def draw_tile_map(
    screen: pg.Surface, tile_dict, tile_map, tile_width=16, tile_height=16
):
    """
    Given a 2D array (tile_map) of tile IDs, draw them on screen.
    """
    for row_idx, row in enumerate(tile_map):
        for col_idx, tile_id in enumerate(row):
            # Only draw if the tile_id is valid in tile_dict
            if tile_id in tile_dict:
                screen.blit(
                    tile_dict[tile_id], (col_idx * tile_width, row_idx * tile_height)
                )
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d


def get_asset_path(*args):
    return os.path.join(ASSETS_PATH, *args)
<<<<<<< HEAD


def get_font(*, font_name: str = "pixelify", size: int = 24):
    paths = {
        "pixelify": "Pixelify_Sans/static/PixelifySans-Regular.ttf",
        "pixeloperator": "PixelOperator8/PixelOperator8.ttf",
    }

    return pg.font.Font(
        os.path.join(FONTS_PATH, paths.get(font_name, "pixelify")), size
    )
=======
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
