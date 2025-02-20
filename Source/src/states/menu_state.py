import os

import pygame as pg

from config import BG_COLOR, GAME_TITLE, SCREEN_WIDTH
from constants.paths import BGMS_PATH, FONTS_PATH
from gui.components import Button
from gui.handlers.cursor_handler import cursor_handler

from .state import State


class MenuState(State):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.title_font = pg.font.Font(
            os.path.join(FONTS_PATH, "Pixelify_Sans/static/PixelifySans-Regular.ttf"),
            48,
        )

        self.buttons = [
            Button(
                SCREEN_WIDTH // 2 - 100,
                200,
                200,
                50,
                "Start Game",
                self.start_game,
            ),
            Button(
                SCREEN_WIDTH // 2 - 100,
                280,
                200,
                50,
                "Quit",
                self.quit_game,
            ),
        ]

        self.boot()

    def boot(self):
        self.game.audio.load_sound("intro", f"{BGMS_PATH}/cave_theme_2.wav")

    def enter(self):
        self.game.audio.play("intro", -1)

    def exit(self):
        pass

    def update(self, dt: float):
        cursor_handler(self.game, buttons=self.buttons)

    def draw(self, screen: pg.Surface):
        title = self.title_font.render(GAME_TITLE, True, (255, 255, 255))

        screen.fill(BG_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for button in self.buttons:
            button.draw(screen)

    def prev(self):
        return super().prev()

    def next(self):
        return self.next_state

    def handle_event(self, event: pg.event.Event):
        for button in self.buttons:
            button.handle_event(event)

    # Additional methods
    def start_game(self):
        from .game_state import GameState

        self.set_next_state(GameState(self.game, map_size=pg.Rect(0, 0, 400, 400)))

    def quit_game(self):
        self.game.running = False
