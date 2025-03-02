<<<<<<< HEAD
import pygame as pg

from config import BG_COLOR, GAME_TITLE
from constants.paths import BGMS_PATH
from gui.components import Button, Text
from gui.handlers.cursor import cursor_handler
from utils import get_screen_sz
=======
import os

import pygame as pg

from config import BG_COLOR, GAME_TITLE, SCREEN_WIDTH
from constants.paths import BGMS_PATH, FONTS_PATH
from gui.components import Button
from gui.handlers.cursor_handler import cursor_handler
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

from .state import State


class MenuState(State):
    def __init__(self, game):
        super().__init__()

<<<<<<< HEAD
        screen_size = get_screen_sz()

        self.game = game

        self.title = Text(
            self.game,
            y=screen_size[1] // 2 - 120,
            center=True,
            text=GAME_TITLE,
            size=48,
            color=(255, 255, 255),
=======
        self.game = game

        self.title_font = pg.font.Font(
            os.path.join(FONTS_PATH, "Pixelify_Sans/static/PixelifySans-Regular.ttf"),
            48,
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
        )

        self.buttons = [
            Button(
<<<<<<< HEAD
                screen_size[0] // 2 - 100,
                screen_size[1] // 2,
=======
                SCREEN_WIDTH // 2 - 100,
                200,
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
                200,
                50,
                "Start Game",
                self.start_game,
            ),
            Button(
<<<<<<< HEAD
                screen_size[0] // 2 - 100,
                screen_size[1] // 2 + 60,
                200,
                50,
                "Settings",
                self.setting_game,
            ),
            Button(
                screen_size[0] // 2 - 100,
                screen_size[1] // 2 + 120,
=======
                SCREEN_WIDTH // 2 - 100,
                280,
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
                200,
                50,
                "Quit",
                self.quit_game,
            ),
        ]

        self.boot()

    def responsive_handle(self):
        super().responsive_handle()

        screen_size = get_screen_sz()

        self.title.set_position(self.title.pos[0], screen_size[1] // 2 - 120)

        button_y = screen_size[1] // 2
        for _ in self.buttons:
            _.set_position(screen_size[0] // 2 - 100, button_y)
            button_y += 60

    def boot(self):
        self.game.audio.load_sound("intro", f"{BGMS_PATH}/cave_theme_2.wav")
        self.game.audio.play("intro", -1)

    def enter(self):
        if self.game.audio.is_playing("intro"):
            self.game.audio.play("intro", -1)

    def exit(self):
        pass

    def update(self, dt: float):
        cursor_handler(self.game, buttons=self.buttons)

    def draw(self, screen: pg.Surface):
<<<<<<< HEAD
        screen.fill(BG_COLOR)
        self.title.draw(screen)

        [_.draw(screen) for _ in self.buttons]

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)

        [_.handle_event(event) for _ in self.buttons]
=======
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
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d

    # Additional methods
    def start_game(self):
        from .game_state import GameState

<<<<<<< HEAD
        self.set_next_state(GameState(self.game))

    def quit_game(self):
        self.game.running = False

    def setting_game(self):
        from .settings_state import SettingsState

        self.set_next_state(SettingsState(self.game))
=======
        self.set_next_state(GameState(self.game, map_size=pg.Rect(0, 0, 400, 400)))

    def quit_game(self):
        self.game.running = False
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
