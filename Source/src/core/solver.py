from __future__ import annotations

import os
import re

from algos import BFS, DFS, GBFS, UCS, AStar, Dijkstra, Swarm
from algos.search import Search, StonesPosFreeze
from algos.swarm import AntColonyOptimization, SwarmBidirectional, SwarmConvergent
from constants.enums import Algorithm, GridItem
from constants.paths import INPUT_DIR
from utils import generate_output_content


class SokobanSolver:
    def __init__(self):
        self.num_row: int = 0
        self.num_col: int = 0
        self.search_matrix: list[list[str]] = []

        self.player_pos = tuple()
        self.stones_pos: StonesPosFreeze = frozenset()
        self.switches_pos = frozenset()

        self.expanded_node: int = 0
        self.explored_node: int = 0
        self.execution_time = None
        self.path: str = ""

    def load_map(self, level: str):
        stone_weights: list[int] = []
        search_matrix: list[str] = []

        with open(level, "r") as f:
            search_matrix = [line.rstrip() for line in f]

        if bool(re.search(r"\d", "_".join(search_matrix[0]))):
            stone_weights = list(map(int, search_matrix[0].split(" ")))
            search_matrix.pop(0)

        self.search_matrix = [list(row) for row in search_matrix]
        self.num_row, self.num_col = (
            len(self.search_matrix),
            max([len(row) for row in self.search_matrix]),
        )

        if len(stone_weights) == 0:
            stone_weights = [1] * len(
                [
                    cell
                    for row in self.search_matrix
                    for cell in row
                    if cell
                    in [
                        GridItem.get_char(GridItem.STONE),
                        GridItem.get_char(GridItem.STONE_ON_SWITCH),
                    ]
                ]
            )

        stone_weights_copy = stone_weights.copy()

        new_switches_pos = set()
        new_stones_pos = set()
        for i in range(len(self.search_matrix)):
            for j in range(len(self.search_matrix[i]) - 1):  # omit endline
                if self.search_matrix[i][j] == ".":
                    new_switches_pos.add((i, j))
                elif self.search_matrix[i][j] == "*":
                    new_stones_pos.add((i, j, stone_weights_copy.pop(0)))
                    new_switches_pos.add((i, j))
                elif self.search_matrix[i][j] == "$":
                    new_stones_pos.add((i, j, stone_weights_copy.pop(0)))
                elif self.search_matrix[i][j] == "@":
                    self.player_pos = (i, j)
                elif self.search_matrix[i][j] == "+":
                    self.player_pos = (i, j)
                    new_switches_pos.add((i, j))
        self.stones_pos = frozenset(new_stones_pos)
        self.switches_pos = frozenset(new_switches_pos)

        # add extra " " character to some lines of matrix
        for row in self.search_matrix:
            for i in range(self.num_col):
                if i > len(row) - 1:
                    row.append(" ")

        return self

    def searching(self, algos: list[Algorithm] = []):
        args = (
            self.num_row,
            self.num_col,
            self.search_matrix,
            self.player_pos,
            self.stones_pos,
            self.switches_pos,
            # use_deadlock=False,
            # use_optimized=False,
        )

        __algos_searching: dict[str, Search] = {
            Algorithm.get_label(Algorithm.BFS): BFS(*args),
            Algorithm.get_label(Algorithm.DFS): DFS(*args),
            Algorithm.get_label(Algorithm.UCS): UCS(*args),
            Algorithm.get_label(Algorithm.ASTAR): AStar(*args),
            Algorithm.get_label(Algorithm.GREEDY): GBFS(*args),
            Algorithm.get_label(Algorithm.DIJKSTRA): Dijkstra(*args),
            Algorithm.get_label(Algorithm.SWARM): Swarm(*args),
            Algorithm.get_label(Algorithm.CONVERGENT_SWARM): SwarmConvergent(*args),
            Algorithm.get_label(Algorithm.BIDIR_SWARM): SwarmBidirectional(*args),
            Algorithm.get_label(Algorithm.ANT_COLONY): AntColonyOptimization(*args),
        }

        if len(algos) == 0:
            return {key: algo.search() for key, algo in __algos_searching.items()}

        return {
            key: algo.search()
            for key, algo in __algos_searching.items()
            if key in algos
        }


if __name__ == "__main__":
    for algo, res in (
        SokobanSolver().load_map(os.path.join(INPUT_DIR, "input-01.txt")).searching()
    ).items():
        (path, weight, expanded_node, explored_node), time, mem, mem_peak = res
        print(
            generate_output_content(
                algo,
                len(path),
                weight,
                expanded_node,
                time,
                mem_peak,
                path,
            )
        )
