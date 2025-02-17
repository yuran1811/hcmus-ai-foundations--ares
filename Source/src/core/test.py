import heapq

# Các hướng di chuyển: Lên, Xuống, Trái, Phải
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class SokobanSolver:
    def __init__(self, grid, player, stones, goals, weights):
        self.grid = grid
        self.player = player
        self.stones = stones
        self.goals = goals
        self.weights = weights  # Khối lượng của từng viên đá
        self.rows = len(grid)
        self.cols = len(grid[0])

    def heuristic(self, stones):
        """Heuristic: Tổng khoảng cách tối thiểu từ đá đến ô điểm có trọng số"""
        return sum(
            self.weights[i]
            * min(abs(stone[0] - gx) + abs(stone[1] - gy) for gx, gy in self.goals)
            for i, stone in enumerate(stones)
        )

    def is_valid(self, x, y):
        """Kiểm tra ô (x, y) có hợp lệ không"""
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != "#"

    def astar(self):
        """Thuật toán A*"""
        start_state = (self.player, tuple(self.stones), 0)
        pq = [(self.heuristic(self.stones), 0, start_state)]  # (f, g, state)
        visited = set()

        while pq:
            _, g, (player, stones, cost) = heapq.heappop(pq)
            if stones in self.goals:
                return cost  # Đã đưa tất cả đá về đích

            if (player, stones) in visited:
                continue
            visited.add((player, stones))

            # Thử tất cả các hướng di chuyển
            for dx, dy in DIRECTIONS:
                new_px, new_py = player[0] + dx, player[1] + dy

                if not self.is_valid(new_px, new_py):
                    continue  # Không thể di chuyển đến đây

                new_stones = list(stones)
                if (new_px, new_py) in stones:  # Nếu chạm vào đá, cần đẩy nó
                    push_x, push_y = new_px + dx, new_py + dy
                    if (push_x, push_y) not in stones and self.is_valid(push_x, push_y):
                        # Đẩy đá thành công
                        new_stones.remove((new_px, new_py))
                        new_stones.append((push_x, push_y))
                    else:
                        continue  # Không thể đẩy

                new_stones = tuple(new_stones)
                new_cost = (
                    cost
                    + 1
                    + sum(
                        self.weights[i]
                        for i, stone in enumerate(stones)
                        if stone == (new_px, new_py)
                    )
                )
                f = new_cost + self.heuristic(new_stones)

                heapq.heappush(
                    pq, (f, new_cost, ((new_px, new_py), new_stones, new_cost))
                )

        return -1  # Không tìm thấy lời giải


# Ví dụ: Map, người chơi, đá, điểm đến, khối lượng đá
grid = ["######", "# .. #", "# $$ #", "# @  #", "######"]
player = (3, 2)
stones = [(2, 2), (2, 3)]
goals = [(1, 2), (1, 3)]
weights = [2, 3]  # Trọng số đá

solver = SokobanSolver(grid, player, stones, goals, weights)
result = solver.astar()
print(f"Chi phí tối thiểu: {result}")
