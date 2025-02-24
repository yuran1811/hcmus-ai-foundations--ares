import pygame as pg

from utils import get_font


class WithFont:
    def __init__(self, *, font_size: int = 24):
        self.font = get_font(size=font_size)
        self.font_size = font_size


class WithLabel(WithFont):
    def __init__(self, *, font_size: int = 24, label: str = ""):
        super().__init__(font_size=font_size)

        self.label = label

    def draw_label(
        self,
        screen: pg.Surface,
        *,
        center: tuple[int, int] = (0, 0),
    ):
        self.text = self.font.render(self.label, True, (255, 255, 255))
        text_rect = self.text.get_rect(center=center)

        screen.blit(self.text, text_rect)

        return text_rect
