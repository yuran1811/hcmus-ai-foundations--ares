import pygame as pg

from config import FPS, GAME_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH
from core.audio import Audio
from gui.components import Cursor
from states.menu_state import MenuState
from states.state import State


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(GAME_TITLE)
        pg.mouse.set_visible(False)

        self.running = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

        self.audio = Audio()
        self.cursor = Cursor(scale_factor=4)

        self.state: State = MenuState(self)
        self.state.enter()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.cursor.update(dt)

            # State transition
            next_state = self.state.next()
            if next_state:
                if self.state:
                    self.state.exit()

                self.state = next_state
                self.state.enter()

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

                self.state.handle_event(event)

            # Update and draw
            self.state.update(dt)
            self.state.draw(self.screen)
            self.cursor.draw(self.screen)

            pg.display.flip()


def launch_game():
    Game().run()
    pg.quit()
