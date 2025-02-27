from __future__ import annotations

from constants.enums import Direction
from utils.metrics import profile

from .search import Point, ProblemState, Search, StonesPos


class DFS(Search):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPos,
        switches_pos: frozenset[Point],
        use_deadlock: bool = True,
    ):
        super().__init__(
            num_row, num_col, matrix, player_pos, stones_pos, switches_pos, use_deadlock
        )

    @profile
    def search(self):
        frontier: list[ProblemState] = []  # Stack 
        frontier.append(self.initial_state)

        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0
        while frontier:  
            expanded_count += 1

            current_state = frontier.pop() 

            for dir in Direction:
                if self.can_go(current_state, dir):
                    new_state = self.go(current_state, dir)

                    if new_state.is_final(self.switches_pos):
                        path, w = self.construct_path(new_state)
                        return path, w, expanded_count, len(closed)

                    if new_state not in closed:
                        closed.add(new_state)
                        frontier.append(new_state)

        return "Impossible", 0, expanded_count, len(closed)