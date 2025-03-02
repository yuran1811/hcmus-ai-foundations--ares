from __future__ import annotations

import heapq

from constants.enums import Direction
from utils import profile

from .search import Point, ProblemState, Search, StateHashTable, StonesPosFreeze


class Dijkstra(Search):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
        use_deadlock: bool = True,
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

        self.initial_state.gval = 0

    def handle(
        self,
        new_state: ProblemState,
        closed: set[ProblemState],
        frontier: list[ProblemState],
        state_hash_table: StateHashTable,
    ):
        id = hash(new_state)

        if new_state not in closed:
            heapq.heappush(frontier, new_state)
            closed.add(new_state)
            state_hash_table[id] = [new_state, True]
            return

        if new_state.gval < state_hash_table[id][0].gval:
            state_hash_table[id][0].gval = new_state.gval
            state_hash_table[id][0].ancestor = new_state.ancestor

            if not state_hash_table[id][1]:
                state_hash_table[id][1] = True
                heapq.heappush(frontier, new_state)

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
            current_hash = hash(current_state)
            if state_hash_table[current_hash][0] != current_state:
                continue

            expanded_count += 1

            state_hash_table[current_hash][1] = False

            for dir in Direction:
                if self.can_go(current_state, dir):
                    new_state = self.go(current_state, dir)
                    self.handle(new_state, closed, frontier, state_hash_table)

        min_g = float("inf")
        min_state = None
        for x in state_hash_table.values():
            state: ProblemState = x[0]
            if state.is_final(self.switches_pos):
                if state.gval < min_g:
                    min_g = state.gval
                    min_state = state

        if min_state is None:
            return "Impossible", 0, expanded_count, len(closed)

        path, w = self.construct_path(min_state)
        return path, w, expanded_count, len(closed)
