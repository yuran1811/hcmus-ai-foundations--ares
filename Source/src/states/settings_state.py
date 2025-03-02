from collections.abc import Callable

import pygame as pg

from config import BG_COLOR
from gui.components import Button, MediaController, SelectComponent
from gui.handlers.cursor import cursor_handler
from utils import get_screen_modes, get_screen_sz, update_screen_sz

from .state import State


class SettingsState(State):
    def __init__(
        self, game, *, on_res_change: Callable[[tuple[int, int]], None] | None = None
    ):
        super().__init__()

        screen_size = get_screen_sz()

        self.game = game

        self.resolutions = get_screen_modes()

        self.media_controller = MediaController(
            x=screen_size[0] // 2 - 200,
            y=80,
            label="BGM",
            show_label=True,
            show_play=True,
            show_mute=True,
            is_playing=self.game.bgms_controller.is_playing(),
            is_muted=self.game.bgms_controller.is_muted(),
            scale_factor=3,
            on_play=lambda: self.game.bgms_controller.play(),
            on_pause=lambda: self.game.bgms_controller.stop(),
            on_next=lambda: self.game.bgms_controller.next_track(),
            on_prev=lambda: self.game.bgms_controller.prev_track(),
            on_mute=self.toggle_mute,
            on_unmute=self.toggle_unmute,
        )

        self.bgms_selector = SelectComponent(
            screen_size[0] // 2 + 50,
            80,
            self.game.bgms_controller.bgm_files or [],
            0,
            show_label=False,
            height=80,
            on_select=lambda _: self.game.bgms_controller.set_current_track(_),
        )

        self.resolution_selector = SelectComponent(
            screen_size[0] // 2 - 150,
            200,
            [f"{w}x{h}" for w, h in self.resolutions],
            self.resolutions.index(screen_size)
            if screen_size in self.resolutions
            else 0,
            label="Change Resolution",
            show_label=True,
            height=160,
            on_select=lambda _: self.change_resolution(_, on_res_change),
        )

        self.back_button = Button(
            screen_size[0] // 2 - 50,
            10,
            100,
            40,
            "Back",
            self.back,
        )

    def responsive_handle(self):
        super().responsive_handle()

        screen_size = get_screen_sz()

        self.resolution_selector.update_rect_topleft(screen_size[0] // 2 - 150, 200)
        self.resolution_selector.change_selected_idx(
            0
            if screen_size not in self.resolutions
            else self.resolutions.index(screen_size)
        )

        self.bgms_selector.update_rect_topleft(screen_size[0] // 2 + 50, 80)

        self.media_controller.update_rect_topleft(screen_size[0] // 2 - 200, 80)

        self.back_button.set_position(screen_size[0] // 2 - 50, 10)

    def boot(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt: float):
        cursor_handler(
            self.game,
            buttons=[self.back_button]
            + list(self.media_controller.components.values()),
        )

        self.back_button.update()
        self.media_controller.update(dt)
        self.resolution_selector.update()
        self.bgms_selector.update()

    def draw(self, screen: pg.Surface):
        screen.fill(BG_COLOR)

        self.back_button.draw(screen)
        self.media_controller.draw(screen)
        self.resolution_selector.draw(screen)
        self.bgms_selector.draw(screen)

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)

        self.back_button.handle_event(event)
        self.media_controller.handle_event(event)
        self.resolution_selector.handle_event(event)
        self.bgms_selector.handle_event(event)

    # Additional methods
    def toggle_mute(self):
        self.game.bgms_controller.mute(True)

    def toggle_unmute(self):
        self.game.bgms_controller.mute(False)

    def change_resolution(self, res: int, on_res_change: Callable | None = None):
        w, h = get_screen_modes(res)[0]

        if isinstance(w, str) or isinstance(h, str):
            return

        if on_res_change:
            on_res_change((w, h))

        update_screen_sz((w, h))

        pg.display.set_mode((w, h))
