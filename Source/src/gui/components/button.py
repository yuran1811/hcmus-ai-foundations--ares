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
        self.callback = callback

        self.hovered = False
        self.clicked = False

    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN and self.hovered:
            self.clicked = True
            self.callback()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicked = False

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pg.Surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_NORMAL
        pg.draw.rect(screen, color, self.rect, border_radius=5)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)
