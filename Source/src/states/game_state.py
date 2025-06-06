from collections.abc import Generator
from typing import Any, TypedDict

import pygame as pg
from config import BG_COLOR, GRID_SIZE
from constants.enums import Algorithm, Direction, GameStateType, Orientation
from entities.map import Map
from entities.player import Player
from gui.components import (
    Button,
    GameInfo,
    MapImport,
    MediaController,
    MiniMap,
    SelectComponent,
    VictoryDialog,
)
from gui.handlers.cursor import cursor_handler
from utils import (
    get_input_filenames,
    get_screen_sz,
    load_input_data,
    load_output_data,
    normalize_output_data,
)

from .state import State


class MoveData(TypedDict):
    player_pos: pg.Vector2
    stone_moved: pg.Vector2 | None
    stone_prev_pos: pg.Vector2 | None
    weight: int
    from_tile_type: pg.Surface | None
    to_tile_type: pg.Surface | None


class GameState(State):
    def __init__(self, game):
        super().__init__()

        screen_size = get_screen_sz()
        input_filenames = get_input_filenames()
        input_filenames_sz = len(input_filenames)
        import_map_btn_rect = pg.Rect(10, 540, 160, 40)

        self.debug_mode = False

        self.game = game

        self.game_info = GameInfo(0, 0, show_fps=True)
        self.game_info.set_position(screen_size[0] - 195, 10)

        self.current_map_index = 1
        self.state_type = GameStateType.PLAYING

        self.start_simulating = False
        self.is_simulating = False
        self.simulate_algo: str | None = None
        self.current_simulation: Generator[bool, Any, None] | None = None

        self.undo_history: list[MoveData] = []
        self.redo_history: list[MoveData] = []

        self.minimap = MiniMap(self, 200, 150)

        self.map_import = MapImport(
            screen_size[0] // 2 - 200,
            screen_size[1] - 350,
            400,
            350,
            toggle_rect=import_map_btn_rect,
        )

        self.controllers = MediaController(
            10,
            60,
            show_play=True,
            show_speed=True,
            show_zoom=True,
            orientation=Orientation.VERTICAL,
            scale_factor=4,
            on_play=lambda: self.toggle_simulation(True),
            on_pause=lambda: self.toggle_simulation(False),
            on_speed_up=lambda _: self.game_info.update_simulation_speed(_),
            on_speed_down=lambda _: self.game_info.update_simulation_speed(_),
            on_prev=lambda: self.load_map(
                from_index=(self.current_map_index - 1 + input_filenames_sz)
                % input_filenames_sz
            ),
            on_next=lambda: self.load_map(
                from_index=(self.current_map_index + 1) % input_filenames_sz
            ),
            # on_backward=self.undo_move,
            # on_forward=self.redo_move,
            on_reset=self.reload_map,
            on_zoom_in=lambda: self.zoom_minimap(1),
            on_zoom_out=lambda: self.zoom_minimap(-1),
        )

        self.selects = {
            "algo": SelectComponent(
                120,
                10,
                Algorithm.get_labels(),
                -1,
                placeholder="Select algo",
                placeholder_empty="No algo found",
                height=240,
                on_select=lambda _: self.on_algo_select(Algorithm.get_labels()[_]),
            ),
            "map": SelectComponent(
                396,
                10,
                input_filenames,
                self.current_map_index,
                height=240,
                on_select=lambda _: self.load_map(from_index=_),
            ),
        }

        self.buttons = {
            "back": Button(
                10,
                10,
                100,
                40,
                "Back",
                self.back,
            ),
            "map_import": Button(
                import_map_btn_rect.x,
                import_map_btn_rect.y,
                import_map_btn_rect.width,
                import_map_btn_rect.height,
                "Import Map",
                self.map_import.toggle,
            ),
        }

        self.dialogs = {
            "victory": VictoryDialog(
                on_next_map=self.on_next_map, on_replay=self.reload_map
            ),
        }

        self.load_map(from_index=self.current_map_index)

    def responsive_handle(self):
        super().responsive_handle()

        screen_size = get_screen_sz()

        self.map_import.set_position(
            screen_size[0] // 2 - 200,
            screen_size[1] - 350,
            self.buttons["map_import"].rect,
        )
        self.game_info.set_position(screen_size[0] - 195, 10)
        [_.responsive_handle() for _ in list(self.dialogs.values())]

    def boot(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt: float):
        if self.current_simulation is not None and self.is_simulating:
            try:
                simulation_done = next(self.current_simulation)
                self.controllers.state["play"] = True

                if simulation_done:
                    self.is_simulating = False
                    self.controllers.state["play"] = False
            except StopIteration:
                self.is_simulating = False
                self.controllers.state["play"] = False

        cursor_handler(
            self.game,
            buttons=list(self.dialogs["victory"].buttons.values())
            + list(self.buttons.values())
            + list(self.controllers.components.values())
            + list(self.map_import.buttons.values()),
        )

        self.game_info.update(dt, self.game.clock)

        self.dialogs["victory"].update(dt)
        self.controllers.update(dt)
        [_.update() for _ in list(self.selects.values()) + list(self.buttons.values())]

        if self.map_import.is_shown():
            self.map_import.update()

        if self.state_type == GameStateType.PLAYING:
            self.update_camera()
            self.player.update(dt)

        if self.map.is_win():
            if not self.current_simulation:
                self.win_handler(False)

    def draw(self, screen: pg.Surface):
        screen.fill(BG_COLOR)

        self.map.draw(screen, self.camera, self.player.pixel_pos)
        self.player.draw(screen, self.camera)

        self.controllers.draw(screen)
        [
            _.draw(screen)
            for _ in list(self.selects.values()) + list(self.buttons.values())
        ]
        self.game_info.draw(screen)
        self.minimap.draw(screen)

        if self.map_import.is_shown():
            self.map_import.draw(screen)

        if self.state_type == GameStateType.VICTORY:
            self.dialogs["victory"].draw(screen)

        if self.debug_mode:
            self.draw_debug(screen)

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                self.debug_mode = not self.debug_mode

        self.dialogs["victory"].handle_event(event)
        self.minimap.handle_event(event)
        self.player.handle_event(event, on_move=self.on_player_move)
        self.controllers.handle_event(event)
        [
            _.handle_event(event)
            for _ in list(self.selects.values()) + list(self.buttons.values())
        ]

        if self.map.is_win():
            self.win_handler(True)

        if self.map_import.is_shown():
            self.map_import.handle_event(event)

    # Additional methods
    def draw_debug(self, screen: pg.Surface):
        self.player.draw_debug(screen, self.camera)

    def update_camera(self):
        if self.minimap.dragging:
            return

        screen_size = get_screen_sz()
        half_screen_w = screen_size[0] // 2
        half_screen_h = screen_size[1] // 2
        self.camera.x = self.player.pixel_pos.x - half_screen_w
        self.camera.y = self.player.pixel_pos.y - half_screen_h

        map_w, map_h = self.map.size[0], self.map.size[1]
        self.camera.x = max(0, min(self.camera.x, map_w - screen_size[0]))
        self.camera.y = max(0, min(self.camera.y, map_h - screen_size[1]))

        if map_w < screen_size[0]:
            self.camera.x = self.player.pixel_pos.x - screen_size[0] // 2
        if map_h < screen_size[1]:
            self.camera.y = self.player.pixel_pos.y - screen_size[1] // 2

    # Map methods
    def reset_level_state(self):
        self.state_type = GameStateType.PLAYING

        if self.minimap:
            self.minimap.reset_zoom()

        self.game_info.reset()
        self.selects["algo"].reset()
        self.dialogs["victory"].reset()

        self.reset_history()
        self.reset_simulation()

    def load_map(self, *, from_index: int = 1):
        self.reset_level_state()

        self.load_map_state(from_index)

        self.current_map_index = from_index
        self.selects["map"].change_selected_idx(self.current_map_index)

        self.selects["algo"].update_options(list(self.map_sol.keys()))
        self.selects["algo"].update_on_select(
            lambda _: self.on_algo_select(list(self.map_sol.keys())[_])
        )

    def load_map_state(self, from_index: int = 1):
        screen_size = get_screen_sz()
        weights, map_data = load_input_data(from_index=from_index)

        self.map = Map(map_data, stone_weights=weights)
        self.map_size = pg.Rect(0, 0, *self.map.size)
        self.map_sol = normalize_output_data(load_output_data(from_index=from_index))

        self.player = Player(pos=self.map.hero_start_pos, map=self.map)

        self.camera = pg.Vector2(
            (screen_size[0] - self.map_size.width) // 2,
            (screen_size[1] - self.map_size.height) // 2,
        )

    def reload_map(self):
        self.load_map(from_index=self.current_map_index)

    def reload_map_state(self):
        self.load_map_state(from_index=self.current_map_index)

    # History methods
    def reset_history(self):
        self.undo_history = []
        self.redo_history = []

    def add_move_to_history(self, next_move: MoveData, cur_move: MoveData):
        self.undo_history.append(next_move)
        self.redo_history.append(cur_move)

    def undo_move(self):
        if len(self.undo_history) == 0:
            return

        move = self.undo_history.pop()
        self.redo_history.append(move)

        # Revert player position
        self.player.grid_pos = move["player_pos"]
        self.player.pixel_pos = move["player_pos"] * GRID_SIZE
        self.player.rect.center = self.player.pixel_pos  # type: ignore

        # Revert stone position if applicable
        if move["stone_moved"] and move["stone_prev_pos"]:
            stone = next(
                (s for s in self.map.stones_pos if s["pos"] == move["stone_moved"]),
                None,
            )
            if stone:
                stone["pos"] = move["stone_prev_pos"]

                self.map.move_stone(
                    move["stone_moved"],
                    move["stone_prev_pos"],
                    restore_from_tile=move["to_tile_type"],
                    restore_to_tile=move["from_tile_type"],
                )

        # Update game info
        self.game_info.increment_step(move["weight"], is_reversed=True)

    def redo_move(self):
        if len(self.redo_history) == 0:
            return

        move = self.redo_history.pop()
        self.undo_history.append(move)

        # Apply player position
        self.player.grid_pos = move["player_pos"]
        self.player.pixel_pos = move["player_pos"] * GRID_SIZE
        self.player.rect.center = self.player.pixel_pos  # type: ignore

        # Apply stone position if applicable
        if move["stone_moved"] and move["stone_prev_pos"]:
            stone = next(
                (s for s in self.map.stones_pos if s["pos"] == move["stone_prev_pos"]),
                None,
            )
            if stone:
                stone["pos"] = move["stone_moved"]
                self.map.move_stone(
                    move["stone_prev_pos"],
                    move["stone_moved"],
                    restore_from_tile=move["from_tile_type"],
                    restore_to_tile=move["to_tile_type"],
                )

        # Update game info
        self.game_info.increment_step(move["weight"])

    # Simulation methods
    def reset_simulation(self):
        self.toggle_simulation(False)

        self.start_simulating = False
        self.is_simulating = False
        self.simulate_algo = None
        self.current_simulation = None
        self.controllers.state["play"] = False

    def toggle_simulation(self, value: bool | None = None):
        if value is not None:
            self.is_simulating = value
        else:
            self.is_simulating = not self.is_simulating

        if self.is_simulating and not self.start_simulating:
            self.reload_map_state()
            self.start_simulating = True

        if self.is_simulating and self.current_simulation is None:
            if self.simulate_algo:
                self.update_simulate_algo(self.simulate_algo)

    def update_simulate_algo(self, algo: str):
        if self.map_sol and algo in self.map_sol:
            self.simulate_algo = algo
            self.simulate_movement(self.map_sol[algo].path)
        else:
            self.reset_simulation()

    def simulate_movement(self, path: str):
        self.reset_simulation()

        __move_queue = [_.lower() for _ in path if _.lower() in "udlr"]

        def movement_generator():
            step_timer = 0.0
            current_step = 0
            base_delay = 0.5  # Base time between steps at 1x speed

            while current_step < len(__move_queue):
                if not self.is_simulating:
                    yield False

                step_timer += self.game.dt

                speed_factor = max(0.1, self.controllers.state.get("speed", 1.0))
                frame_delay = max(base_delay / speed_factor, 0.2)

                if step_timer >= frame_delay:
                    step_timer %= frame_delay

                    direction = Direction.from_char(__move_queue[current_step])
                    if direction:
                        self.player.try_move(direction, on_move=self.on_player_move)
                        current_step += 1

                    yield False
                else:
                    yield False

            self.is_simulating = False
            yield True

        self.current_simulation = movement_generator()

    # Event handlers
    def win_handler(self, with_dialog):
        self.game_info.stop_timer()
        self.state_type = GameStateType.VICTORY

        if with_dialog:
            self.dialogs["victory"].show()
            self.dialogs["victory"].toggle_confetti(True)

    def zoom_minimap(self, delta: int):
        zoom_level = max(
            0.1, min(1.0, (int(self.minimap.zoom_level * 10) + delta) / 10)
        )

        screen_size = get_screen_sz()
        if delta < 0 or (delta > 0 and self.minimap.width * 2 < screen_size[0]):
            self.minimap.zoom_level = zoom_level

        self.minimap.constrain_content()

    def on_next_map(self):
        self.load_map(from_index=self.current_map_index + 1)

        self.state_type = GameStateType.PLAYING

        self.dialogs["victory"].toggle_confetti(False)

    def on_algo_select(self, algo: str):
        self.simulate_algo = algo
        self.update_simulate_algo(algo)

        if self.map_sol and self.simulate_algo in self.map_sol:
            self.toggle_simulation(True)

    def on_player_move(
        self,
        step_weight: int = 0,
        *,
        stone_prev_pos: pg.Vector2 | None = None,
        stone_moved: pg.Vector2 | None = None,
        from_tile_type: pg.Surface | None = None,
        to_tile_type: pg.Surface | None = None,
    ):
        self.game_info.increment_step(step_weight)

        self.add_move_to_history(
            {
                "player_pos": self.player.grid_pos.copy(),
                "stone_prev_pos": stone_prev_pos,
                "stone_moved": stone_moved,
                "weight": step_weight,
                "from_tile_type": from_tile_type,
                "to_tile_type": to_tile_type,
            },
            {
                "player_pos": self.player.grid_pos.copy(),
                "stone_prev_pos": stone_prev_pos,
                "stone_moved": stone_moved,
                "weight": step_weight,
                "from_tile_type": from_tile_type,
                "to_tile_type": to_tile_type,
            },
        )
