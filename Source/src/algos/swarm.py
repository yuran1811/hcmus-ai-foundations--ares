from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment

from utils.base import manhattan
from utils.metrics import profile

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
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0

        return "Impossible", 0, expanded_count, len(closed)


class SwarmConvergent(Swarm):
    @profile
    def search(self):
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0

        return "Impossible", 0, expanded_count, len(closed)


class SwarmBidirectional(Swarm):
    @profile
    def search(self):
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0

        return "Impossible", 0, expanded_count, len(closed)


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

    @profile
    def search(self):
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0

        return "Impossible", 0, expanded_count, len(closed)


# def swarm_search(matrix, start, end, pos):
#     n = len(matrix)
#     distances = {i: float("inf") for i in range(n)}
#     distances[start] = 0
#     pheromones = {i: 1.0 for i in range(n)}
#     visited = {}
#     frontier = [(0, start, None)]  # (score, node, predecessor)
#     path = []

#     while frontier:
#         current_score, current, predecessor = heapq.heappop(frontier)

#         if current in visited:
#             continue

#         visited[current] = predecessor

#         while len(path) > 0 and path[-1] != visited[current]:
#             path.pop()
#         path.append(current)

#         if current == end:
#             print("-----------------")
#             print(f"visited: {visited}")
#             print(f"path: {path}")
#             print(f"distance: {distances[end]}")
#             return visited, path, distances

#         pheromones[current] *= 1.1

#         for neighbor in range(n):
#             if matrix[current][neighbor] != 0 and neighbor not in visited:
#                 distance = distances[current] + matrix[current][neighbor]
#                 heuristic_value = heuristic(neighbor, end, pos)
#                 score = (0.7 * distance / pheromones[neighbor]) + (
#                     0.3 * heuristic_value
#                 )

#                 if distance < distances[neighbor]:
#                     distances[neighbor] = distance
#                     heapq.heappush(frontier, (score, neighbor, current))

#         for node in pheromones:
#             pheromones[node] *= 0.95

#     print("No path found!")
#     return visited, path, distances


# def compute_probability(current, unvisited, matrix, pheromones, alpha, beta):
#     probabilities = []
#     total = 0
#     for neighbor in unvisited:
#         if matrix[current][neighbor] > 0:
#             tau = pheromones[current][neighbor] ** alpha
#             eta = (1 / matrix[current][neighbor]) ** beta
#             prob = tau * eta
#             probabilities.append((neighbor, prob))
#             total += prob
#     return [(n, p / total) for n, p in probabilities] if total > 0 else []


# def update_pheromones(pheromones, paths, distances, evaporation_rate):
#     pheromones *= 1 - evaporation_rate
#     for path, distance in zip(paths, distances):
#         for i in range(len(path) - 1):
#             pheromones[path[i]][path[i + 1]] += 1.0 / distance


# def ant_colony_optimization(
#     matrix,
#     start,
#     end,
#     pos,
#     num_ants=10,
#     alpha=1.0,
#     beta=2.0,
#     evaporation_rate=0.5,
#     iterations=100,
# ):
#     num_nodes = len(matrix)
#     pheromones = np.ones((num_nodes, num_nodes))
#     best_path = None
#     best_distance = float("inf")

#     for _ in range(iterations):
#         paths = []
#         distances = []

#         for _ in range(num_ants):
#             current = start
#             path = [current]
#             unvisited = set(range(num_nodes)) - {start}
#             distance = 0

#             while current != end and unvisited:
#                 probabilities = compute_probability(
#                     current, unvisited, matrix, pheromones, alpha, beta
#                 )
#                 if not probabilities:
#                     break

#                 next_node = random.choices(
#                     [n for n, _ in probabilities], [p for _, p in probabilities]
#                 )[0]
#                 path.append(next_node)
#                 unvisited.remove(next_node)
#                 distance += matrix[current][next_node]
#                 current = next_node

#             if current == end:
#                 paths.append(path)
#                 distances.append(distance)
#                 if distance < best_distance:
#                     best_distance = distance
#                     best_path = path

#         update_pheromones(pheromones, paths, distances, evaporation_rate)

#     return best_path, best_distance


# def bidirectional_swarm_search(matrix, start, end, pos):
#     distances_start = {i: float("inf") for i in range(len(matrix))}
#     distances_end = {i: float("inf") for i in range(len(matrix))}
#     distances_start[start] = 0
#     distances_end[end] = 0

#     pheromones_start = {i: 1.0 for i in range(len(matrix))}
#     pheromones_end = {i: 1.0 for i in range(len(matrix))}

#     visited_start = {}
#     visited_end = {}

#     frontier_start = [(0, start, None)]  # (score, node, predecessor)
#     frontier_end = [(0, end, None)]

#     path_start = []
#     path_end = []

#     meeting_node = None

#     while frontier_start and frontier_end:
#         for frontier, visited, distances, pheromones, path, other_visited in [
#             (
#                 frontier_start,
#                 visited_start,
#                 distances_start,
#                 pheromones_start,
#                 path_start,
#                 visited_end,
#             ),
#             (
#                 frontier_end,
#                 visited_end,
#                 distances_end,
#                 pheromones_end,
#                 path_end,
#                 visited_start,
#             ),
#         ]:
#             current_score, current, predecessor = heapq.heappop(frontier)

#             if current in visited:
#                 continue

#             visited[current] = predecessor

#             while len(path) > 0 and path[-1] != visited[current]:
#                 path.pop()
#             path.append(current)

#             if current in other_visited:
#                 meeting_node = current
#                 break

#             pheromones[current] *= 1.1

#             for neighbor in range(len(matrix)):
#                 if matrix[current][neighbor] != 0 and neighbor not in visited:
#                     distance = distances[current] + matrix[current][neighbor]
#                     heuristic_value = heuristic(
#                         neighbor, end if frontier is frontier_start else start, pos
#                     )
#                     score = (0.7 * distance / pheromones[neighbor]) + (
#                         0.3 * heuristic_value
#                     )

#                     if distance < distances[neighbor]:
#                         distances[neighbor] = distance
#                         heapq.heappush(frontier, (score, neighbor, current))

#             for node in pheromones:
#                 pheromones[node] *= 0.95

#         if meeting_node:
#             break

#     if meeting_node:
#         full_path = []
#         node = meeting_node
#         while node is not None:
#             full_path.append(node)
#             node = visited_start.get(node)
#         full_path.reverse()
#         node = visited_end.get(meeting_node)
#         while node is not None:
#             full_path.append(node)
#             node = visited_end.get(node)

#         print("-----------------")
#         print(f"visited_start: {visited_start}")
#         print(f"visited_end: {visited_end}")
#         print(f"path: {full_path}")
#         print(
#             f"distance: {distances_start[meeting_node] + distances_end[meeting_node]}"
#         )
#         return visited_start, visited_end, full_path, distances_start, distances_end

#     print("No path found!")
#     return visited_start, visited_end, [], distances_start, distances_end


# def convergent_swarm_search(matrix, start, end, pos):
#     n = len(matrix)

#     distances = {i: float("inf") for i in range(n)}
#     distances[start] = 0

#     pheromones = {i: 1.0 for i in range(n)}
#     visited = {}

#     frontier = [(0, start, None)]  # (score, node, predecessor)
#     path = []

#     while frontier:
#         current_score, current, predecessor = heapq.heappop(frontier)

#         if current in visited:
#             continue

#         visited[current] = predecessor

#         while path and path[-1] != visited[current]:
#             path.pop()
#         path.append(current)

#         if current == end:
#             print("-----------------")
#             print(f"visited: {visited}")
#             print(f"path: {path}")
#             print(f"distance: {distances[end]}")
#             return visited, path, distances

#         pheromones[current] *= 1.1

#         for neighbor in range(n):
#             if matrix[current][neighbor] == 0 or neighbor in visited:
#                 continue

#             distance = distances[current] + matrix[current][neighbor]
#             heuristic_value = heuristic(neighbor, end, pos)
#             score = (0.7 * distance / pheromones[neighbor]) + (0.3 * heuristic_value)

#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 heapq.heappush(frontier, (score, neighbor, current))

#         for node in pheromones:
#             pheromones[node] *= 0.95

#     print("No path found!")
#     return visited, path, distances
