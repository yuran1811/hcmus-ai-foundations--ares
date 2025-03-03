import pygame as pg

from utils import get_screen_sz

from .decorators import WithFont


class Text(WithFont):
    def __init__(
        self,
        game,
        *,
        x: int = 0,
        y: int = 0,
        center=True,
        text="",
        size=10,
        color=(0, 0, 0),
    ):
        super().__init__(font_size=size)

        self.game = game

        self.pos = (x, y)
        self.center = center

        self.text = text
        self.size = size
        self.color = color

    def set_position(self, x: int, y: int):
        self.pos = (x, y)

    def draw(self, screen: pg.Surface):
        screen_size = get_screen_sz()

        self.image = self.font.render(self.text, True, self.color)

        pos = self.pos
        if self.center:
            pos = (screen_size[0] // 2 - self.image.get_width() // 2, self.pos[1])

        screen.blit(self.image, pos)
