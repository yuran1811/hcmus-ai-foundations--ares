import heapq

import numpy as np
from scipy.optimize import linear_sum_assignment  # Hungarian Algorithm

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class SokobanSolver:
    def __init__(self, grid, player, stones, goals, weights):
        self.grid = grid
        self.player = player
        self.stones = stones
        self.goals = goals
        self.weights = weights
        self.rows = len(grid)
        self.cols = len(grid[0])

    def hungarian_heuristic(self, stones):
        """Sử dụng thuật toán Hungarian để tối ưu hóa heuristic"""
        cost_matrix = np.zeros((len(stones), len(self.goals)))

        for i, (sx, sy) in enumerate(stones):
            for j, (gx, gy) in enumerate(self.goals):
                cost_matrix[i, j] = self.weights[i] * (abs(sx - gx) + abs(sy - gy))

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        return cost_matrix[row_ind, col_ind].sum()

    def is_deadlock(self, stone):
        """Kiểm tra xem viên đá có bị mắc kẹt vào góc không"""
        x, y = stone
        if self.grid[x][y] == "#":
            return True
        # Kiểm tra bị kẹt ở góc với tường
        if (
            (self.grid[x - 1][y] == "#" and self.grid[x][y - 1] == "#")
            or (self.grid[x - 1][y] == "#" and self.grid[x][y + 1] == "#")
            or (self.grid[x + 1][y] == "#" and self.grid[x][y - 1] == "#")
            or (self.grid[x + 1][y] == "#" and self.grid[x][y + 1] == "#")
        ):
            return True
        return False

    def bidirectional_astar(self):
        """Thuật toán A* hai chiều"""
        start_state = (self.player, tuple(self.stones), 0)
        goal_state = (None, tuple(self.goals), 0)

        forward_pq = [(self.hungarian_heuristic(self.stones), 0, start_state)]
        backward_pq = [(0, 0, goal_state)]  # Không cần heuristic phía goal

        forward_visited = {}
        backward_visited = {}

        while forward_pq and backward_pq:
            # Forward search
            _, g, (player, stones, cost) = heapq.heappop(forward_pq)
            print(f"Player: {player}, Stones: {stones}, Cost: {cost}")

            if (player, stones) in backward_visited:
                return g + backward_visited[(player, stones)]

            forward_visited[(player, stones)] = g

            # Thử các nước đi hợp lệ
            for dx, dy in DIRECTIONS:
                new_px, new_py = player[0] + dx, player[1] + dy
                if (new_px, new_py) in stones:  # Nếu gặp đá, kiểm tra đẩy
                    push_x, push_y = new_px + dx, new_py + dy
                    if (push_x, push_y) not in stones and self.grid[push_x][
                        push_y
                    ] != "#":
                        new_stones = list(stones)
                        new_stones.remove((new_px, new_py))
                        new_stones.append((push_x, push_y))

                        if any(self.is_deadlock(stone) for stone in new_stones):
                            continue  # Bỏ qua nếu rơi vào deadlock

                        new_stones = tuple(new_stones)
                        new_cost = (
                            cost + 1 + self.weights[stones.index((new_px, new_py))]
                        )
                        f = new_cost + self.hungarian_heuristic(new_stones)

                        heapq.heappush(
                            forward_pq,
                            (f, new_cost, ((new_px, new_py), new_stones, new_cost)),
                        )

            # Backward search
            _, g_b, (p_b, stones_b, cost_b) = heapq.heappop(backward_pq)
            if (p_b, stones_b) in forward_visited:
                return g_b + forward_visited[(p_b, stones_b)]

            backward_visited[(p_b, stones_b)] = g_b

        return -1  # Không tìm thấy lời giải


# Ví dụ: Map, người chơi, đá, điểm đến, khối lượng đá
grid = ["######", "# .. #", "# $$ #", "# @  #", "######"]
player = (3, 2)
stones = [(2, 2), (2, 3)]
goals = [(1, 2), (1, 3)]
weights = [2, 3]  # Trọng số đá

solver = SokobanSolver(grid, player, stones, goals, weights)
result = solver.bidirectional_astar()
print(f"Chi phí tối thiểu: {result}")
