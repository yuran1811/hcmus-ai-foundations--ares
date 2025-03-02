from __future__ import annotations

import heapq

import numpy as np
from scipy.optimize import linear_sum_assignment

from constants.enums import Direction
from utils.base import manhattan
from utils.metrics import profile

from .search import Point, ProblemState, Search, StateHashTable, StonesPosFreeze


class GBFS(Search):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
        use_deadlock: bool = True,
        use_optimized: bool = True,
    ):
        super().__init__(
            num_row,
            num_col,
            matrix,
            player_pos,
            stones_pos,
            switches_pos,
            use_deadlock=use_deadlock,
            use_weight=True,
        )

        self.use_optimized = use_optimized

        self.initial_state.fval = self.heuristic(frozenset(stones_pos), switches_pos)

    def handle(
        self,
        new_state: ProblemState,
        closed: set[ProblemState],
        frontier: list[ProblemState],
        state_hash_table: StateHashTable,
    ):
        id = hash(new_state)

        if new_state not in closed:
            closed.add(new_state)
            heapq.heappush(frontier, new_state)
            state_hash_table[id] = [new_state, True]
            return

        if new_state.fval < state_hash_table[id][0].fval:
            state_hash_table[id][0].fval = new_state.fval
            state_hash_table[id][0].ancestor = new_state.ancestor

            if not state_hash_table[id][1]:
                state_hash_table[id][1] = True
                heapq.heappush(frontier, new_state)

    def heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        return (
            self.hungarian_heuristic(stones_pos, switches_pos)
            if self.use_optimized
            else self.mahattan_heuristic(stones_pos, switches_pos)
        )

    def mahattan_heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        sum = 0
        for stone in stones_pos:
            sum = sum + stone[2] * min(
                [
                    manhattan(stone[0], stone[1], switch[0], switch[1])
                    for switch in switches_pos
                ]
            )
        return sum

    def hungarian_heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        dists = np.zeros((len(stones_pos), len(switches_pos)))

        for i, (sx, sy, w) in enumerate(stones_pos):
            for j, (gx, gy) in enumerate(switches_pos):
                dists[i, j] = w * manhattan(sx, sy, gx, gy)

        row_ind, col_ind = linear_sum_assignment(dists)
        return dists[row_ind, col_ind].sum()

    @profile
    def search(self):
        frontier: list[ProblemState] = []
        heapq.heappush(frontier, self.initial_state)

        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        state_hash_table = {hash(self.initial_state): [self.initial_state, True]}

        expanded_count = 0
        while frontier:
            current_state = heapq.heappop(frontier)
            if current_state.is_final(self.switches_pos):
                path, w = self.construct_path(current_state)
                return path, w, expanded_count, len(closed)

            current_hash = hash(current_state)
            if state_hash_table[current_hash][0] != current_state:
                continue

            state_hash_table[current_hash][1] = False

            expanded_count += 1

            for dir in Direction:
                if self.can_go(current_state, dir):
                    new_state = self.go(current_state, dir, heuristic=self.heuristic)
                    new_state.fval -= new_state.gval
                    new_state.gval = 0
                    self.handle(new_state, closed, frontier, state_hash_table)

        return "Impossible", 0, expanded_count, len(closed)
