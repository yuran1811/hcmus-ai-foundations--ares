from __future__ import annotations

import heapq
import random

import numpy as np
from scipy.optimize import linear_sum_assignment

from constants.enums import Direction
from utils import manhattan, profile

from .search import Point, ProblemState, Search, StonesPos, StonesPosFreeze


class Swarm(Search):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPos,
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

    def heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        return (
            self.hungarian_heuristic(stones_pos, switches_pos)
            if self.use_optimized
            else self.manhattan_heuristic(stones_pos, switches_pos)
        )

    def manhattan_heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        total_cost = 0
        for stone in stones_pos:
            total_cost += stone[2] * min(
                [
                    manhattan(stone[0], stone[1], switch[0], switch[1])
                    for switch in switches_pos
                ]
            )
        return total_cost

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

    def get_neighbors(self, state: ProblemState):
        neighbors = []
        for dir in Direction:
            if self.can_go(state, dir):
                new_state = self.go(state, dir, heuristic=self.heuristic)
                neighbors.append(new_state)
        return neighbors

    @profile
    def search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.initial_state))

        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        state_hash_table = {hash(self.initial_state): [self.initial_state, True]}

        expanded_count = 0
        visited_count = 1

        while open_set:
            _, current_state = heapq.heappop(open_set)

            if current_state.is_final(self.switches_pos):
                path, w = self.construct_path(current_state)
                return path, w, expanded_count, visited_count

            current_hash = hash(current_state)
            if state_hash_table[current_hash][0] != current_state:
                continue

            state_hash_table[current_hash][1] = False
            expanded_count += 1

            neighbors = self.get_neighbors(current_state)
            for neighbor in neighbors:
                new_distance = current_state.gval + (
                    neighbor.pushed_stone[2] if neighbor.pushed_stone else 1
                )
                h_score = self.heuristic(neighbor.stones_pos, self.switches_pos)

                if neighbor not in closed:
                    f_score = new_distance + h_score
                    neighbor.gval = new_distance
                    neighbor.fval = f_score

                    closed.add(neighbor)
                    heapq.heappush(open_set, (f_score, neighbor))
                    state_hash_table[hash(neighbor)] = [neighbor, True]
                    visited_count += 1
                else:
                    id = hash(neighbor)
                    if new_distance <= state_hash_table[id][0].gval:
                        f_score = new_distance + h_score
                        state_hash_table[id][0].fval = f_score
                        state_hash_table[id][0].gval = new_distance
                        state_hash_table[id][0].ancestor = current_state

                        heapq.heappush(open_set, (f_score, neighbor))
                        visited_count += 1

                    elif (
                        new_distance <= state_hash_table[id][0].gval * 1.1
                    ):  # Allow 10% higher cost
                        f_score = new_distance + h_score
                        heapq.heappush(open_set, (f_score, neighbor))
                        visited_count += 1

        return "Impossible", 0, expanded_count, visited_count


class SwarmConvergent(Swarm):
    @profile
    def search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.initial_state))
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)
        expanded_count = 0

        while open_set:
            _, current_state = heapq.heappop(open_set)

            if current_state.is_final(self.switches_pos):
                path, w = self.construct_path(current_state)
                return (
                    path,
                    w,
                    expanded_count,
                    len(closed),
                )

            for neighbor in self.get_neighbors(current_state):
                if neighbor not in closed:
                    cost = self.heuristic(neighbor.stones_pos, self.switches_pos)
                    heapq.heappush(open_set, (cost, neighbor))
                    closed.add(neighbor)

            expanded_count += 1

        return "Impossible", 0, expanded_count, len(closed)


class SwarmBidirectional(Swarm):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPos,
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
            use_deadlock,
            use_optimized,
        )

        # Initialize goal state
        self.goal_state = ProblemState(
            None,
            player_pos,
            frozenset((x, y, w) for (x, y), (_, _, w) in zip(switches_pos, stones_pos)),
            with_heuristic=True,
            use_weight=True,
        )
        self.goal_state.gval = 0
        self.goal_state.fval = 0

    @profile
    def search(self):
        forward_open_set = []
        backward_open_set = []

        heapq.heappush(forward_open_set, (0, self.initial_state))
        heapq.heappush(backward_open_set, (0, self.goal_state))

        forward_closed: set[ProblemState] = set()
        backward_closed: set[ProblemState] = set()

        forward_closed.add(self.initial_state)
        backward_closed.add(self.goal_state)

        expanded_count = 0

        while forward_open_set or backward_open_set:
            _, forward_state = (
                heapq.heappop(forward_open_set)
                if forward_open_set
                else (
                    float("inf"),
                    None,
                )
            )
            _, backward_state = (
                heapq.heappop(backward_open_set)
                if backward_open_set
                else (
                    float("inf"),
                    None,
                )
            )

            if (
                forward_state in backward_closed
                or backward_state in forward_closed
                or forward_state == backward_state
            ):
                path1, w1 = (
                    self.construct_path(forward_state) if forward_state else ("", 0)
                )
                path2, w2 = (
                    self.construct_path(backward_state) if backward_state else ("", 0)
                )

                return (
                    path1 + path2[::-1],
                    w1 + w2,
                    expanded_count,
                    len(forward_closed) + len(backward_closed),
                )

            if forward_state:
                for neighbor in self.get_neighbors(forward_state):
                    if neighbor not in forward_closed:
                        cost = self.heuristic(neighbor.stones_pos, self.switches_pos)
                        heapq.heappush(forward_open_set, (cost, neighbor))
                        forward_closed.add(neighbor)

            if backward_state:
                for neighbor in self.get_neighbors(backward_state):
                    if neighbor not in backward_closed:
                        cost = self.heuristic(neighbor.stones_pos, self.switches_pos)
                        heapq.heappush(backward_open_set, (cost, neighbor))
                        backward_closed.add(neighbor)

            expanded_count += 1

        return (
            "Impossible",
            0,
            expanded_count,
            len(forward_closed) + len(backward_closed),
        )


class AntColonyOptimization(Search):
    def __init__(
        self,
        num_row: int,
        num_col: int,
        matrix: list[list[str]],
        player_pos: Point,
        stones_pos: StonesPos,
        switches_pos: frozenset[Point],
        use_deadlock: bool = True,
        use_optimized: bool = True,
        num_ants: int = 10,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation_rate: float = 0.5,
        iterations: int = 100,
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
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.iterations = iterations
        self.pheromone = np.ones((num_row, num_col))

    def heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        return (
            self.hungarian_heuristic(stones_pos, switches_pos)
            if self.use_optimized
            else self.manhattan_heuristic(stones_pos, switches_pos)
        )

    def manhattan_heuristic(
        self,
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
    ):
        total_cost = 0
        for stone in stones_pos:
            total_cost += stone[2] * min(
                manhattan(stone[0], stone[1], switch[0], switch[1])
                for switch in switches_pos
            )
        return total_cost

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

    def get_neighbors(self, state: ProblemState):
        neighbors = []
        for dir in Direction:
            if self.can_go(state, dir):
                new_state = self.go(state, dir)
                neighbors.append(new_state)
        return neighbors

    def choose_next_move(self, state: ProblemState, neighbors: list[ProblemState]):
        probabilities = []
        total = 0

        for neighbor in neighbors:
            x, y = neighbor.player_pos
            pheromone = self.pheromone[x][y] ** self.alpha
            # Calculate heuristic using Manhattan distance to goal
            heuristic = (
                1 / (1 + self.heuristic(neighbor.stones_pos, self.switches_pos))
            ) ** self.beta
            score = pheromone * heuristic
            probabilities.append(score)
            total += score

        if total == 0:
            return random.choice(neighbors)

        probabilities = [p / total for p in probabilities]
        return random.choices(neighbors, weights=probabilities, k=1)[0]

    def update_pheromone(self, paths: list[tuple[list[ProblemState], int]]):
        self.pheromone *= 1 - self.evaporation_rate

        for path, cost in paths:
            pheromone_deposit = 1 / cost if cost > 0 else 1
            for state in path:
                self.pheromone[state.player_pos[0], state.player_pos[1]] += (
                    pheromone_deposit
                )

    @profile
    def search(self):
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        best_path = None
        best_cost = float("inf")
        expanded_count = 0

        for _ in range(self.iterations):
            paths: list[tuple[list[ProblemState], int]] = []

            for _ in range(self.num_ants):
                state = self.initial_state
                path: list[ProblemState] = []
                cost = 0

                while not state.is_final(self.switches_pos):
                    neighbors = self.get_neighbors(state)
                    if not neighbors:
                        break

                    next_state = self.choose_next_move(state, neighbors)
                    cost += 1
                    path.append(next_state)
                    state = next_state

                if state.is_final(self.switches_pos) and cost < best_cost:
                    best_path, best_cost = path, cost

                paths.append((path, cost))
                closed.add(state)

            self.update_pheromone(paths)

            expanded_count += 1

        return (
            best_path if best_path else "Impossible",
            best_cost,
            expanded_count,
            len(closed),
        )
