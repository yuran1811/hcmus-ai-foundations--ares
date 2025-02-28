from enum import Enum


class GridItem(Enum):
    WALL = 0, "#"
    FLOOR = 1, " "
    STONE = 2, "$"
    ARES = 3, "@"
    SWITCH = 4, "."
    STONE_ON_SWITCH = 5, "*"
    ARES_ON_SWITCH = 6, "+"

    @classmethod
    def get_char(cls, item):
        return cls(item).value[1]

    @classmethod
    def convert_char(cls, char: str):
        for item in cls:
            if item.value[1] == char:
                return item.value[0]
        return None


class Algorithm(Enum):
    BFS = 0, "BFS", "Breadth First Search"
    DFS = 1, "DFS", "Depth First Search"
    ASTAR = 2, "A*", "A* Search with heuristic"
    GREEDY = 3, "GBFS", "Greedy Best First Search"
    DIJKSTRA = 4, "Dijkstra", "Dijkstra's Algorithm"
    SWARM = 5, "Swarm", "Swarm Algorithm"
    CONVERGENT_SWARM = 6, "Convergent Swarm", "Convergent Swarm Algorithm"
    BIDIRECTIONAL_SWARM = 7, "Bidirectional Swarm", "Bidirectional Swarm Algorithm"
    ANT_COLONY = 8, "Ant Colony", "Ant Colony Optimization"

    @classmethod
    def from_label(cls, label):
        for algo in Algorithm:
            if algo.value[1] == label:
                return algo

        return Algorithm.BFS

    @classmethod
    def get_label(cls, algo):
        return cls(algo).value[1]

    @classmethod
    def get_labels(cls):
        return [cls(algo).value[1] for algo in cls]

    @classmethod
    def get_desc(cls, algo):
        return cls(algo).value[2]


class Direction(Enum):
    UP = 0, "UP", "u", (0, -1)
    DOWN = 1, "DOWN", "d", (0, 1)
    LEFT = 2, "LEFT", "l", (-1, 0)
    RIGHT = 3, "RIGHT", "r", (1, 0)
<<<<<<< HEAD

    @classmethod
    def from_char(cls, char):
        for direction in Direction:
            if direction.value[2] == char:
                return direction
=======
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

    @classmethod
    def get_label(cls, direction):
        return cls(direction).value[1]

    @classmethod
    def get_movement(cls, direction):
        return cls(direction).value[2]

    @classmethod
    def get_pushing(cls, direction):
        return cls(direction).value[2].upper()

    @classmethod
    def get_vec(cls, direction):
        return cls(direction).value[3]
<<<<<<< HEAD


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class GameStateType(Enum):
    PLAYING = 0
    VICTORY = 1
=======
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
