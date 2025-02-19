import pygame as pg

from config import BG_COLOR, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.player import Player
from gui.components.button import Button
from gui.handlers.cursor_handler import cursor_handler

from .state import State


class GameState(State):
    def __init__(self, game, *, map_size: pg.Rect):
        super().__init__()

        self.game = game
        self.player = Player(5 * GRID_SIZE, 5 * GRID_SIZE)
        self.camera = pg.Vector2(0, 0)

        self.map_size = map_size

        self.buttons = [
            Button(
                0,
                0,
                100,
                50,
                "Back",
                self.back,
            )
        ]

        self.debug_mode = False

    def boot(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt: float):
        cursor_handler(self.game, buttons=self.buttons)

        self.player.update(dt)

        # Update camera to follow player with bounds checking
        self.camera.x = self.player.pixel_pos.x - SCREEN_WIDTH // 2
        self.camera.y = self.player.pixel_pos.y - SCREEN_HEIGHT // 2

        # Clamp camera to map bounds
        self.camera.x = max(0, min(self.camera.x, self.map_size.width - SCREEN_WIDTH))
        self.camera.y = max(0, min(self.camera.y, self.map_size.height - SCREEN_HEIGHT))

    def draw(self, screen: pg.Surface):
        screen.fill(BG_COLOR)

        for button in self.buttons:
            button.draw(screen)

        self.player.draw(screen, self.camera)

        if self.debug_mode:
            self.player.draw_debug(screen, self.camera)

    def prev(self):
        return self.prev_state

    def next(self):
        return self.next_state

    def handle_event(self, event: pg.event.Event):
        for button in self.buttons:
            button.handle_event(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                self.debug_mode = not self.debug_mode

            if event.key == pg.K_ESCAPE:
                self.next_state = self.prev()

            if event.key in [pg.K_w, pg.K_UP]:
                self.player.try_move("back")
            if event.key in [pg.K_s, pg.K_DOWN]:
                self.player.try_move("front")
            if event.key in [pg.K_a, pg.K_LEFT]:
                self.player.try_move("left")
            if event.key in [pg.K_d, pg.K_RIGHT]:
                self.player.try_move("right")

        self.player.handle_event(event)
