import random
from collections.abc import Callable
from typing import TypedDict

import pygame as pg

from config import GRID_SIZE
from constants.enums import GridItem
from constants.paths import TILESETS_PATH


class Tile:
    def __init__(self, tile_type: str, image: pg.Surface, passable: bool):
        self.tile_type = tile_type
        self.image = image
        self.passable = passable


class MapStone(TypedDict):
    pos: pg.Vector2
    weight: int


class Map:
    TILE_MAPPING = {
        GridItem.WALL.value[1]: "wall",
        GridItem.FLOOR.value[1]: "floor",
        GridItem.ARES.value[1]: "floor",
        GridItem.STONE.value[1]: "stone",
        GridItem.SWITCH.value[1]: "switch",
        GridItem.ARES_ON_SWITCH.value[1]: "floor",
        GridItem.STONE_ON_SWITCH.value[1]: "sos",
    }

    def __init__(self, grid_data: str, *, stone_weights: list[int] = []):
        self.tileset = self.load_tileset()
        self.tile_grid: list[list[Tile]] = []

        self.hero_start_pos = (0, 0)
        self.switches_pos: list[pg.Vector2] = []
        self.stones_pos: list[MapStone] = []
        self.stone_weights = stone_weights

        self.set_grid(grid_data)

    def is_win(self):
        return all(stone["pos"] in self.switches_pos for stone in self.stones_pos)

    def set_grid(self, grid_data: str):
        self.grid = self.parse_grid(grid_data)
        self.size = self.calc_map_size()
        self.load()

    def parse_grid(self, grid_str: str):
        return [list(line) for line in grid_str.split("\n") if line.strip()]

    def calc_map_size(self):
        max_cols = max(len(row) for row in self.grid) if self.grid else 0
        return (len(self.grid) * GRID_SIZE, max_cols * GRID_SIZE)

    def get_scaled_tile(self, tileset: pg.Surface, x: int, y: int, size: int):
        tile = tileset.subsurface((x * size, y * size, size, size))
        return pg.transform.scale(tile, (GRID_SIZE, GRID_SIZE))

    def get_tile_at(self, x: float, y: float):
        grid_x = int(x // GRID_SIZE)
        grid_y = int(y // GRID_SIZE)

        if 0 <= grid_y < len(self.tile_grid) and 0 <= grid_x < len(
            self.tile_grid[grid_y]
        ):
            return self.tile_grid[grid_y][grid_x]

        return None

    def get_tile_image(self, x: int, y: int, player_pos: pg.Vector2):
        pos = pg.Vector2(x, y)
        base_tile = self.tile_grid[y][x]

        # player on switch
        if pos == player_pos // GRID_SIZE and pos in self.switches_pos:
            return self.tileset["switch"][0]

        return base_tile.image

    def load_tileset(self) -> dict[str, list[pg.Surface]]:
        tileset_img = pg.image.load(f"{TILESETS_PATH}/dungeon/set1.png").convert_alpha()
        tile_size = 16

        return {
            "wall": [
                *[
                    self.get_scaled_tile(tileset_img, x, 0, tile_size)
                    for x in range(1, 5)
                ],
            ],
            "floor": [
                self.get_scaled_tile(tileset_img, 9, 7, tile_size),
                *[
                    self.get_scaled_tile(tileset_img, x, y, tile_size)
                    for x in range(6, 10)
                    for y in range(3)
                ],
            ],
            "stone": [self.get_scaled_tile(tileset_img, 9, 9, tile_size)],
            "switch": [self.get_scaled_tile(tileset_img, 4, 8, tile_size)],
            "sos": [self.get_scaled_tile(tileset_img, 4, 7, tile_size)],
        }

    def load(self):
        self.wall_tiles = {}
        self.floor_tiles = {}
        stone_weights = self.stone_weights.copy()

        for y, row in enumerate(self.grid):
            tile_row: list[Tile] = []

            for x, char in enumerate(row):
                if (
                    char == GridItem.ARES.value[1]
                    or char == GridItem.ARES_ON_SWITCH.value[1]
                ):
                    self.hero_start_pos = (x * GRID_SIZE, y * GRID_SIZE)

                if (
                    char == GridItem.STONE.value[1]
                    or char == GridItem.STONE_ON_SWITCH.value[1]
                ):
                    self.stones_pos.append(
                        {"pos": pg.Vector2(x, y), "weight": stone_weights.pop(0)}
                    )

                if (
                    char == GridItem.SWITCH.value[1]
                    or char == GridItem.ARES_ON_SWITCH.value[1]
                    or char == GridItem.STONE_ON_SWITCH.value[1]
                ):
                    self.switches_pos.append(pg.Vector2(x, y))

                tile_type = self.TILE_MAPPING.get(char, "floor")
                tile_row.append(
                    Tile(
                        tile_type=tile_type,
                        image=self.tileset[tile_type][0]
                        if tile_type != "floor"
                        else random.choice(self.tileset["floor"]),
                        passable=char
                        not in [
                            GridItem.WALL.value[1],
                            GridItem.STONE.value[1],
                            GridItem.STONE_ON_SWITCH.value[1],
                        ],
                    )
                )

                if tile_type == "wall":
                    self.wall_tiles[(y, x)] = random.choice(self.tileset["wall"])
                else:
                    self.floor_tiles[(y, x)] = random.choice(self.tileset["floor"])

            self.tile_grid.append(tile_row)

    def move_stone(
        self,
        from_pos: pg.Vector2,
        to_pos: pg.Vector2,
        *,
        on_move: Callable[..., None] | None = None,
        restore_from_tile: pg.Surface | None = None,
        restore_to_tile: pg.Surface | None = None,
    ):
        from_x, from_y = int(from_pos.x), int(from_pos.y)
        to_x, to_y = int(to_pos.x), int(to_pos.y)

        if 0 <= from_y < len(self.tile_grid) and 0 <= from_x < len(
            self.tile_grid[from_y]
        ):
            if 0 <= to_y < len(self.tile_grid) and 0 <= to_x < len(
                self.tile_grid[to_y]
            ):
                stone_idx = next(
                    (i for i, s in enumerate(self.stones_pos) if s["pos"] == from_pos),
                    None,
                )
                if stone_idx is not None:
                    self.stones_pos[stone_idx]["pos"] = to_pos.copy()

                    was_on_switch = pg.Vector2(from_x, from_y) in self.switches_pos
                    tile_type = "switch" if was_on_switch else "floor"
                    self.tile_grid[from_y][from_x] = Tile(
                        tile_type=tile_type,
                        image=restore_from_tile
                        or (
                            self.tileset[tile_type][0]
                            if tile_type != "floor"
                            else random.choice(self.tileset["floor"])
                        ),
                        passable=True,
                    )

                    is_on_switch = pg.Vector2(to_x, to_y) in self.switches_pos
                    tile_type = "sos" if is_on_switch else "stone"
                    self.tile_grid[to_y][to_x] = Tile(
                        tile_type=tile_type,
                        image=restore_to_tile or self.tileset[tile_type][0],
                        passable=False,
                    )

                    on_move(
                        self.stones_pos[stone_idx]["weight"],
                        stone_prev_pos=from_pos.copy(),
                        stone_moved=to_pos.copy(),
                        from_tile_type=self.tile_grid[from_y][from_x].image,
                        to_tile_type=self.tile_grid[to_y][to_x].image,
                    ) if on_move else None

    def draw(self, screen: pg.Surface, camera: pg.Vector2, player_pos: pg.Vector2):
        screen_rect = screen.get_rect()
        start_y = max(0, int(camera.y // GRID_SIZE))
        end_y = min(
            len(self.tile_grid), int((camera.y + screen_rect.height) // GRID_SIZE) + 1
        )

        for y in range(start_y, end_y):
            for x in range(
                max(0, int(camera.x // GRID_SIZE)),
                min(
                    len(self.tile_grid[y]),
                    int((camera.x + screen_rect.width) // GRID_SIZE) + 1,
                ),
            ):
                try:
                    pos = (
                        x * GRID_SIZE - camera.x,
                        y * GRID_SIZE - camera.y,
                    )

                    tile_image = self.get_tile_image(x, y, player_pos)

                    if self.tile_grid[y][x].tile_type not in ["floor", "wall"]:
                        screen.blit(
                            self.floor_tiles.get((y, x), self.tileset["floor"][0]), pos
                        )

                    if self.tile_grid[y][x].tile_type == "wall":
                        screen.blit(
                            self.wall_tiles.get((y, x), self.tileset["wall"][0]), pos
                        )
                    else:
                        screen.blit(tile_image, pos)
                except IndexError:
                    continue
