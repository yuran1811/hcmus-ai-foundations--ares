from __future__ import annotations

from enum import Enum


class GridItem(Enum):
    WALL = 0, "#"
    FLOOR = 1, " "
    STONE = 2, "$"
    ARES = 3, "@"
    SWITCH = 4, "."
    STONE_ON_SWITCH = 5, "*"
    ARES_ON_SWITCH = 6, "+"

    @staticmethod
    def get_char(item: GridItem):
        return item.value[1]

    @staticmethod
    def convert_char(char: str):
        for item in GridItem:
            if item.value[1] == char:
                return item.value[0]
        return None


class MinimapTileColor(Enum):
    WALL = 0, (106, 106, 149, 255)
    FLOOR = 1, (30, 30, 46, 255)
    STONE = 2, (253, 199, 0, 255)
    ARES = 3, (0, 255, 0, 255)
    SWITCH = 4, (80, 162, 255, 255)
    STONE_ON_SWITCH = 5, (5, 223, 114, 255)
    ARES_ON_SWITCH = 6, (0, 255, 0, 255)
    INVALID = 7, (255, 0, 0, 255)

    @staticmethod
    def get_color(tile_type: MinimapTileColor):
        return tile_type.value[1]

    @staticmethod
    def get_color_by_type(tile_type: str):
        for color in MinimapTileColor:
            if color.name.lower() == tile_type:
                return color.value[1]

    @staticmethod
    def get_color_by_char(char: str):
        for color in MinimapTileColor:
            if GridItem.convert_char(char) == color.value[0]:
                return color.value[1]

        return MinimapTileColor.INVALID.value[1]


class Algorithm(Enum):
    BFS = 0, "BFS", "Breadth First Search"
    DFS = 1, "DFS", "Depth First Search"
    UCS = 2, "UCS", "Depth First Search"
    ASTAR = 3, "A*", "A* Search with heuristic"
    GREEDY = 4, "GBFS", "Greedy Best First Search"
    DIJKSTRA = 5, "Dijkstra", "Dijkstra's Algorithm"
    SWARM = 6, "Swarm", "Swarm Algorithm"
    CONVERGENT_SWARM = 7, "Convergent Swarm", "Convergent Swarm Algorithm"
    BIDIR_SWARM = 8, "Bidirectional Swarm", "Bidirectional Swarm Algorithm"
    ANT_COLONY = 9, "Ant Colony", "Ant Colony Optimization"

    @staticmethod
    def from_label(label: str):
        for algo in Algorithm:
            if algo.value[1] == label:
                return algo

        return Algorithm.BFS

    @staticmethod
    def get_label(algo: Algorithm):
        return algo.value[1]

    @staticmethod
    def get_labels():
        return [algo.value[1] for algo in Algorithm]

    @staticmethod
    def get_desc(algo):
        return algo.value[2]


class Direction(Enum):
    # DIR = idx, label, movement, vec(row, col)
    UP = 0, "UP", "u", (-1, 0)
    DOWN = 1, "DOWN", "d", (1, 0)
    LEFT = 2, "LEFT", "l", (0, -1)
    RIGHT = 3, "RIGHT", "r", (0, 1)

    @staticmethod
    def from_char(char: str):
        for direction in Direction:
            if direction.value[2] == char:
                return direction

    @staticmethod
    def to_list():
        return [x.value for x in Direction]

    @staticmethod
    def get_label(dir: Direction):
        return dir.value[1]

    @staticmethod
    def get_movement(dir: Direction):
        return dir.value[2]

    @staticmethod
    def get_pushing(dir: Direction):
        return dir.value[2].upper()

    @staticmethod
    def get_vec(dir: Direction):
        return dir.value[3]

    @staticmethod
    def get_vec_list():
        return [dir.value[3] for dir in Direction]


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class GameStateType(Enum):
    PLAYING = 0
    VICTORY = 1
