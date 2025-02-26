from __future__ import annotations

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
        closed: set[ProblemState] = set()
        closed.add(self.initial_state)

        expanded_count = 0

        return "Impossible", 0, expanded_count, len(closed)


# def dfs(matrix, start, end):
#     frontier = [(start, None)]
#     visited = {}
#     path = []

#     while frontier:
#         current, predecessor = frontier.pop()
#         visited[current] = predecessor

#         while len(path) > 0 and path[-1] != visited[current]:
#             path.pop()
#         path.append(current)

#         if current == end:
#             print("-----------------")
#             print(f"visited: {visited}")
#             print(f"path: {path}")
#             return visited, path

#         for neighbor in range(len(matrix[current]) - 1, -1, -1):
#             if matrix[current][neighbor] != 0 and neighbor not in visited:
#                 frontier.append((neighbor, current))

#     print(f"visited: {visited}")
#     return visited, path
