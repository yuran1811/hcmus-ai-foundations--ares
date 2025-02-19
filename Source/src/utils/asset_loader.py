import os

import pygame as pg

from constants.paths import ASSETS_PATH, CHARACTERS_PATH


def load_spritesheet(
    file_path: str,
    *,
    frame_size: tuple[int, int],
    scale_factor: float,
    columns: int,
    direction_map: list[str],
    mirrored_pairs=None,
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

    #  scaling transformation
    scaled_size = (int(frame_size[0] * scale_factor), int(frame_size[1] * scale_factor))

    # Extract original directions
    for row, direction in enumerate(direction_map):
        frames = []
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height

            frame = pg.Surface(frame_size, pg.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))

            scaled_frame = pg.transform.scale(frame, scaled_size)
            frames.append(scaled_frame)

        animations[direction] = frames

    # Create mirrored versions
    if mirrored_pairs:
        for source, target in mirrored_pairs:
            if source in animations:
                mirrored_frames = [
                    pg.transform.flip(frame, True, False)
                    for frame in animations[source]
                ]
                animations[target] = mirrored_frames

    return animations


def load_character_animations():
    return {
        "idle": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "idle.png"),
            frame_size=(80, 80),
            scale_factor=2.5,
            columns=4,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
        ),
        "walk": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "walk.png"),
            frame_size=(80, 80),
            scale_factor=2.5,
            columns=8,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
        ),
        "run": load_spritesheet(
            os.path.join(CHARACTERS_PATH, "hana-caraka", "run.png"),
            frame_size=(80, 80),
            scale_factor=2.5,
            columns=4,
            direction_map=["right", "front", "back"],
            mirrored_pairs=[("right", "left")],
        ),
    }


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


def get_asset_path(*args):
    return os.path.join(ASSETS_PATH, *args)
