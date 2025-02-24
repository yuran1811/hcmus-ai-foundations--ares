from collections.abc import Callable

import pygame as pg

from config import BG_COLOR, SCREEN_RES
from gui.components.button import Button
from gui.components.media import MediaController
from gui.components.select import SelectComponent
from gui.handlers.cursor import cursor_handler
from utils import get_screen_sz, update_screen_sz

from .state import State


class SettingsState(State):
    def __init__(
        self, game, *, on_res_change: Callable[[tuple[int, int]], None] | None = None
    ):
        super().__init__()

        screen_size = get_screen_sz()

        self.game = game

        self.resolutions = SCREEN_RES

        self.media_controller = MediaController(
            x=screen_size[0] // 2 - 50,
            y=80,
            label="BGM",
            show_label=True,
            show_play=True,
            show_mute=True,
            is_playing=self.game.audio.is_playing("intro"),
            is_muted=self.game.audio.is_muted("intro"),
            scale_factor=3.0,
            on_play=lambda: self.game.audio.play("intro", -1),
            on_pause=lambda: self.game.audio.stop("intro"),
            on_mute=self.toggle_mute,
            on_unmute=self.toggle_unmute,
        )

        self.resolution_selector = SelectComponent(
            screen_size[0] // 2 - 150,
            140,
            [f"{w}x{h}" for w, h in self.resolutions],
            self.resolutions.index(screen_size),
            label="Change Resolution",
            show_label=True,
            height=200,
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

        self.media_controller.update(dt)
        self.resolution_selector.update()
        self.back_button.update()

    def draw(self, screen: pg.Surface):
        screen.fill(BG_COLOR)

        self.media_controller.draw(screen)
        self.resolution_selector.draw(screen)
        self.back_button.draw(screen)

    def responsive_handle(self, screen_size: tuple[int, int]):
        self.media_controller.update_rect_topleft(screen_size[0] // 2 - 50, 80)
        self.resolution_selector.update_rect_topleft(screen_size[0] // 2 - 150, 140)
        self.back_button.set_position(screen_size[0] // 2 - 50, 10)

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)

        self.media_controller.handle_event(event)
        self.resolution_selector.handle_event(event)
        self.back_button.handle_event(event)

    # Additional methods
    def toggle_mute(self):
        self.game.audio.mute("intro", True)

    def toggle_unmute(self):
        self.game.audio.mute("intro", False)

    def change_resolution(
        self, res: str, on_res_change: Callable[[tuple[int, int]], None] | None = None
    ):
        w, h = map(int, res.split("x"))

        if on_res_change:
            on_res_change((w, h))

        update_screen_sz((w, h))

        pg.display.set_mode((w, h))
