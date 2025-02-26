from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue

from constants.enums import Direction, GridItem
from utils import profile

type Point = tuple[int, int]
type Stone = tuple[int, int, int]
type StonesPosFreeze = frozenset[Stone]
type StonesPos = StonesPosFreeze | set[Stone]
type StateHashTable = dict[int, list]


def stone_exists(stones_pos: StonesPos, pos: Point):
    return any((_[0], _[1]) == pos for _ in stones_pos)


def get_stone(stones_pos: StonesPos, pos: Point):
    for _ in stones_pos:
        if (_[0], _[1]) == pos:
            return _

    return None


class ProblemState:
    def __init__(
        self,
        ancestor: ProblemState | None,
        player_pos: Point,
        stones_pos: StonesPos,
        gval: int = -1,
        fval: float = -1,
        pushed_stone: Stone | None = None,
    ):
        self.ancestor = ancestor

        self.player_pos = player_pos

        # use frozenset (immutable set) for creating hashable value
        self.stones_pos = (
            stones_pos if isinstance(stones_pos, frozenset) else frozenset(stones_pos)
        )

        self.pushed_stone = pushed_stone

        self.gval = gval
        self.fval = fval

    def __lt__(self, state: ProblemState):
        if self.fval == state.fval:
            return self.gval > state.gval
        return self.fval < state.fval

    def __eq__(self, state: object):
        if not isinstance(state, ProblemState):
            return NotImplemented

        return (
            self.player_pos == state.player_pos and self.stones_pos == state.stones_pos
        )

    def __hash__(self):
        return hash((self.player_pos, self.stones_pos))

    def is_final(self, switches_pos: frozenset[Point]):
        return frozenset({(x, y) for x, y, _ in self.stones_pos}) == switches_pos

    def has_cycle(self, state_hash_table: StateHashTable):
        cur_hash = state_hash_table[hash(self)][0]
        p = self.ancestor
        while p:
            if hash(p) == cur_hash:
                return True
            p = p.ancestor
        return False


class DeadlockDetect:
    @staticmethod
    def has_simple_deadlock(
        matrix: list[list[str]],
        num_row: int,
        num_col: int,
        switches_pos: frozenset[Point],
    ):
        reachable = [[False] * num_col for _ in range(num_row)]

        q: Queue[Point] = Queue()
        dir_vecs = Direction.get_vec_list()
        for g in switches_pos:
            q.put(g)
            reachable[g[0]][g[1]] = True

            for dx, dy in dir_vecs:
                nx, ny = g[0] + dx, g[1] + dy

                if (
                    0 <= nx < num_row
                    and 0 <= ny < num_col
                    and matrix[nx][ny] != GridItem.get_char(GridItem.WALL)
                ):
                    q.put((nx, ny))
                    reachable[nx][ny] = True

        dir_vecs = [(2 * _[0], 2 * _[1]) for _ in dir_vecs]
        while not q.empty():
            x, y = q.get()

            for dx, dy in dir_vecs:
                nx, ny = x + dx // 2, y + dy // 2
                tx, ty = x + dx, y + dy

                if (
                    0 <= tx < num_row
                    and 0 <= ty < num_col
                    and matrix[nx][ny] != GridItem.get_char(GridItem.WALL)
                    and matrix[tx][ty] != GridItem.get_char(GridItem.WALL)
                    and not reachable[nx][ny]
                ):
                    q.put((nx, ny))
                    reachable[nx][ny] = True

        return [[not cell for cell in row] for row in reachable]

    @staticmethod
    def has_freeze_deadlock(
        pos: Point,
        matrix: list[list[str]],
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
        has_simple_deadlock: list[list[bool]],
        checked_list: set[Point],
    ):
        # mark new position as being checked
        checked_list.add(pos)

        # The stone is blocked along the vertical axis when one of the following checks are true:
        #     If there is a wall on the left or on the right side of the stone then the stone is blocked along this axis
        #     If there is a simple deadlock square on both sides (left and right) of the stone the stone is blocked along this axis
        #     If there is a stone one the left or right side then this stone is blocked if the other stone is blocked.
        x, y = pos
        x_axis_freeze = DeadlockDetect.check_axis(
            x,
            y,
            matrix,
            stones_pos,
            switches_pos,
            has_simple_deadlock,
            checked_list,
            axis="x",
        )
        y_axis_freeze = DeadlockDetect.check_axis(
            x,
            y,
            matrix,
            stones_pos,
            switches_pos,
            has_simple_deadlock,
            checked_list,
            axis="y",
        )

        if not x_axis_freeze or not y_axis_freeze:
            return False

        # If the new stone position doesn't make a goal state, we accept this situation as freeze deadlock
        return any(stone not in switches_pos for stone in checked_list)

    @staticmethod
    def check_axis(
        x: int,
        y: int,
        matrix: list[list[str]],
        stones_pos: StonesPosFreeze,
        switches_pos: frozenset[Point],
        has_simple_deadlock: list[list[bool]],
        checked_list: set[Point],
        axis: str,
    ):
        dir_vecs = ((1, 0), (-1, 0)) if axis == "x" else ((0, 1), (0, -1))
        simple_dl_count = 0

        for dx, dy in dir_vecs:
            nx, ny = x + dx, y + dy

            if matrix[nx][ny] == GridItem.get_char(GridItem.WALL):
                return True

            if has_simple_deadlock[nx][ny]:
                simple_dl_count += 1
                if simple_dl_count == 2:
                    return True
                continue

            if stone_exists(stones_pos, (nx, ny)):
                if (nx, ny) in checked_list or DeadlockDetect.has_freeze_deadlock(
                    (nx, ny),
                    matrix,
                    stones_pos,
                    switches_pos,
                    has_simple_deadlock,
                    checked_list.copy(),
                ):
                    return True

        return False


class Search(ABC):
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
        self.num_row = num_row
        self.num_col = num_col
        self.matrix = matrix

        self.switches_pos = frozenset(switches_pos)
        self.initial_state = ProblemState(None, player_pos, stones_pos)

        self.use_deadlock = use_deadlock
        self.has_simple_deadlock = DeadlockDetect.has_simple_deadlock(
            self.matrix, self.num_row, self.num_col, self.switches_pos
        )

    def can_go(self, current_state: ProblemState, dir: Direction):
        x, y = current_state.player_pos

        if dir == Direction.UP and x <= 1:
            return False
        if dir == Direction.DOWN and x >= self.num_row - 2:
            return False
        if dir == Direction.LEFT and y <= 1:
            return False
        if dir == Direction.RIGHT and y >= self.num_col - 2:
            return False

        axis_x, axis_y = Direction.get_vec(dir)

        t1 = self.matrix[x + axis_x][y + axis_y]
        t2 = (
            self.matrix[x + (2 * axis_x)][y + (2 * axis_y)] if self.use_deadlock else ""
        )

        if t1 == GridItem.get_char(GridItem.WALL):
            return False

        stones_pos = current_state.stones_pos
        if stone_exists(stones_pos, (x + axis_x, y + axis_y)):
            if self.use_deadlock:
                if (
                    t2 == GridItem.get_char(GridItem.WALL)
                    or stone_exists(stones_pos, (x + (2 * axis_x), y + (2 * axis_y)))
                    or self.has_simple_deadlock[x + (2 * axis_x)][y + (2 * axis_y)]
                ):
                    return False

            new_stones_pos = set(stones_pos)
            stone = get_stone(stones_pos, (x + axis_x, y + axis_y))
            if stone:
                new_stones_pos.remove(stone)
                new_stones_pos.add((x + (2 * axis_x), y + (2 * axis_y), stone[2]))

            if self.use_deadlock and DeadlockDetect.has_freeze_deadlock(
                (x + (2 * axis_x), y + (2 * axis_y)),
                self.matrix,
                frozenset(new_stones_pos),
                self.switches_pos,
                self.has_simple_deadlock,
                set(),
            ):
                return False

        return True

    def go(self, current_state: ProblemState, dir: Direction, heuristic=None):
        player_x, player_y = current_state.player_pos

        axis_x, axis_y = Direction.get_vec(dir)

        new_stone_pos = set(current_state.stones_pos)
        stone = get_stone(
            current_state.stones_pos, (player_x + axis_x, player_y + axis_y)
        )
        if stone:
            new_stone_pos.remove(stone)
            new_stone_pos.add((stone[0] + axis_x, stone[1] + axis_y, stone[2]))
        new_stone_pos = frozenset(new_stone_pos)

        if heuristic:
            gval = current_state.gval + (stone[2] if stone else 1)

            return ProblemState(
                current_state,
                (player_x + axis_x, player_y + axis_y),
                new_stone_pos,
                gval,
                (gval + heuristic(new_stone_pos, self.switches_pos)),
                stone,
            )

        return ProblemState(
            current_state,
            (player_x + axis_x, player_y + axis_y),
            new_stone_pos,
            pushed_stone=stone,
        )

    def construct_path(self, state: ProblemState):
        path = ""
        weight = 0

        movements = [Direction.get_movement(_) for _ in Direction]
        pushings = [Direction.get_pushing(_) for _ in Direction]

        while state.ancestor:
            x1, y1 = state.ancestor.player_pos
            x2, y2 = state.player_pos

            weight += state.pushed_stone[2] if state.pushed_stone else 0

            if x2 > x1:
                path = (movements[1] if not state.pushed_stone else pushings[1]) + path
            elif x2 < x1:
                path = (movements[0] if not state.pushed_stone else pushings[0]) + path
            elif y2 > y1:
                path = (movements[3] if not state.pushed_stone else pushings[3]) + path
            else:
                path = (movements[2] if not state.pushed_stone else pushings[2]) + path

            state = state.ancestor

        return path, weight

    @abstractmethod
    @profile
    def search(self) -> tuple[str, int, int, int]:
        pass
