<<<<<<< HEAD
from collections.abc import Callable
from typing import Any

import pygame as pg

from config import BUTTON_HOVER, BUTTON_NORMAL

from .decorators import WithFont


class Button(WithFont):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str,
        callback: Callable[[], Any] | None = None,
        *,
        font_size=24,
    ):
        super().__init__(font_size=font_size)

        self.text = text

        self.rect = pg.Rect(x, y, width, height)

=======
import pygame as pg

from config import BUTTON_HOVER, BUTTON_NORMAL
from constants.paths import FONTS_PATH


class Button:
    def __init__(self, x, y, width, height, text: str, callback):
        self.text = text
        self.font = pg.font.Font(
            f"{FONTS_PATH}/Pixelify_Sans/static/PixelifySans-Regular.ttf",
            24,
        )
        self.rect = pg.Rect(x, y, width, height)
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
        self.callback = callback

        self.hovered = False
        self.clicked = False

<<<<<<< HEAD
    def set_position(self, x: int, y: int):
        self.rect.topleft = (x, y)
=======
    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN and self.hovered:
            self.clicked = True
            self.callback()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicked = False
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pg.Surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_NORMAL
        pg.draw.rect(screen, color, self.rect, border_radius=5)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)
<<<<<<< HEAD

    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.clicked = True

            if self.callback:
                self.callback()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicked = False
=======
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
