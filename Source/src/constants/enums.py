from enum import Enum


class GridItem(Enum):
    WALL = 0, "#"
    EMPTY = 1, " "
    STONE = 2, "$"
    ARES = 3, "@"
    SWITCH = 4, "."
    STONE_ON_SWITCH = 5, "*"
    ARES_ON_SWITCH = 6, "+"

    @classmethod
    def get_char(cls, item):
        return cls(item).value[1]

    @classmethod
    def convert_char(cls, char):
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
    def get_label(cls, algo):
        return cls(algo).value[1]

    @classmethod
    def get_desc(cls, algo):
        return cls(algo).value[2]


class Direction(Enum):
    UP = 0, "UP", "u"
    DOWN = 1, "DOWN", "d"
    LEFT = 2, "LEFT", "l"
    RIGHT = 3, "RIGHT", "r"

    @classmethod
    def get_label(cls, direction):
        return cls(direction).value[1]

    @classmethod
    def get_movement(cls, direction):
        return cls(direction).value[2]

    @classmethod
    def get_pushing(cls, direction):
        return cls(direction).value[2].upper()
