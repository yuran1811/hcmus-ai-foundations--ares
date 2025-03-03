import pygame as pg

from config import BG_COLOR, GAME_TITLE
from gui.components import Button, Text
from gui.handlers.cursor import cursor_handler
from utils import get_screen_sz

from .state import State


class MenuState(State):
    def __init__(self, game):
        super().__init__()

        screen_size = get_screen_sz()

        self.game = game

        self.title = Text(
            self.game,
            y=screen_size[1] // 2 - 120,
            center=True,
            text=GAME_TITLE,
            size=48,
            color=(255, 255, 255),
        )

        self.buttons = [
            Button(
                screen_size[0] // 2 - 100,
                screen_size[1] // 2,
                200,
                50,
                "Start Game",
                self.start_game,
            ),
            Button(
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
        self.game.bgms_controller.play()

    def enter(self):
        if self.game.bgms_controller.is_playing():
            self.game.bgms_controller.play()

    def exit(self):
        pass

    def update(self, dt: float):
        cursor_handler(self.game, buttons=self.buttons)

    def draw(self, screen: pg.Surface):
        screen.fill(BG_COLOR)
        self.title.draw(screen)

        [_.draw(screen) for _ in self.buttons]

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)

        [_.handle_event(event) for _ in self.buttons]

    # Additional methods
    def start_game(self):
        from .game_state import GameState

        self.set_next_state(GameState(self.game))

    def quit_game(self):
        self.game.running = False

    def setting_game(self):
        from .settings_state import SettingsState

        self.set_next_state(SettingsState(self.game))
