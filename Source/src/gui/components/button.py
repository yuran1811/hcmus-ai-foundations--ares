from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pygame as pg

from config import BUTTON_HOVER, BUTTON_NORMAL

from .decorators import WithFont


class Button(WithFont):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Callable[[], Any] | None = None,
        *,
        font_size=24,
        fit_content=False,
        fg: tuple[int, int, int] = (255, 255, 255),
        bg: tuple[int, int, int] = BUTTON_NORMAL,
        fg_hover: tuple[int, int, int] = (255, 255, 255),
        bg_hover: tuple[int, int, int] = BUTTON_HOVER,
        calc_rect: Callable[[Button, int, int, int, int], pg.Rect] | None = None,
    ):
        super().__init__(font_size=font_size)

        self.fg = fg
        self.bg = bg
        self.fg_hover = fg_hover
        self.bg_hover = bg_hover

        self.text = text
        self.text_width = self.font.render(text, True, fg).get_width() + 20

        self.width = width
        self.height = height

        self.fit_content = fit_content

        self.calc_rect = calc_rect
        if self.calc_rect:
            self.rect = self.calc_rect(
                self, x, y, self.text_width if fit_content else width, height
            )
        else:
            self.rect = pg.Rect(x, y, self.text_width if fit_content else width, height)

        self.callback = callback

        self.hovered = False
        self.clicked = False

    def get_position(self):
        return self.rect.topleft

    def set_position(self, x: int, y: int):
        if self.calc_rect:
            self.rect = self.calc_rect(
                self,
                x,
                y,
                self.text_width if self.fit_content else self.width,
                self.height,
            )
        else:
            self.rect.topleft = (x, y)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pg.Surface):
        text_surf = self.font.render(
            self.text, True, self.fg_hover if self.hovered else self.fg
        )
        text_rect = text_surf.get_rect(center=self.rect.center)
        if self.fit_content:
            text_rect.width = self.text_width

        pg.draw.rect(
            screen,
            self.bg_hover if self.hovered else self.bg,
            self.rect,
            border_radius=5,
        )

        screen.blit(text_surf, text_rect)

    def handle_event(self, event: pg.event.Event):
        self.update()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.clicked = True

            if self.callback:
                self.callback()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicked = False
