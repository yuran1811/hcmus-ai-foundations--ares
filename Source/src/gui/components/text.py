import pygame as pg

<<<<<<< HEAD
from utils.config import get_screen_sz

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
=======

class TextSprite(pg.sprite.Sprite):
    """
    Sprite class for displaying text
    """

    def __init__(self, game, font_path, text="", size=10, color=(0, 0, 0)):
        super().__init__()

        self.game = game

        self.font_path = font_path
        self.draw_text(text, size, color)

    def draw_text(self, text, size=10, color=(0, 0, 0), alias=True):
        self.text = text
        self.image = self.get_font_size(size).render(text, alias, color)
        self.rect = self.image.get_rect()

    def get_font_size(self, size):
        return pg.font.Font(self.font_path, size)
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
