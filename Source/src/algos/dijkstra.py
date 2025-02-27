from __future__ import annotations
import heapq
from constants.enums import Direction
from utils.metrics import profile
from .search import Point, ProblemState, Search, StonesPos


class Dijkstra(Search):
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
        self.initial_state.gval = 0  # Distance from start

    @profile
    def search(self):
        # Priority queue storing (distance, state)
        frontier = [(0, self.initial_state)]
        
        # Keep track of distances
        distances = {self.initial_state: 0}
        
        closed: set[ProblemState] = set()
        
        expanded_count = 0
        while frontier:
            expanded_count += 1
            
            current_dist, current_state = heapq.heappop(frontier)
            
            if current_state.is_final(self.switches_pos):
                path, w = self.construct_path(current_state)
                return path, w, expanded_count, len(closed)
                
            if current_state in closed:
                continue
                
            closed.add(current_state)
            
            for dir in Direction:
                if self.can_go(current_state, dir):
                    new_state = self.go(current_state, dir)
                    new_dist = current_dist + 1  # Assuming unit edge weights
                    
                    if new_state not in distances or new_dist < distances[new_state]:
                        distances[new_state] = new_dist
                        new_state.gval = new_dist
                        heapq.heappush(frontier, (new_dist, new_state))

        return "Impossible", 0, expanded_count, len(closed)