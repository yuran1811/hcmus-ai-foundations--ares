from __future__ import annotations

import pygame as pg

from config import FPS, GAME_TITLE
from gui.components import Cursor
from states.menu_state import MenuState
from states.state import State
from utils import get_screen_sz

from .audio import Audio


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(GAME_TITLE)
        pg.mouse.set_visible(False)

        screen_size = get_screen_sz()
        self.screen = pg.display.set_mode(screen_size)

        self.clock = pg.time.Clock()
        self.audio = Audio()
        self.cursor = Cursor(scale_factor=4)

        self.dt = 0.0
        self.running = True
        self.state: State = MenuState(self)
        self.state_hist: set[State] = {self.state}
        self.state.enter()

    def run(self):
        while self.running:
            self.dt = max(0.005, self.clock.tick(FPS) / 1000)

            # State transition
            next_state = self.state.next()
            if next_state:
                if self.state:
                    self.state.exit()

                self.state = next_state
                self.state_hist.add(next_state)
                self.state.enter()

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if (
                    event.type == pg.VIDEORESIZE
                    or event.type == pg.WINDOWRESIZED
                    or event.type == pg.WINDOWSIZECHANGED
                ):
                    [_.responsive_handle(get_screen_sz()) for _ in self.state_hist]

                self.state.handle_event(event)

            # Update and draw
            for _ in [self.state, self.cursor]:
                _.update(self.dt)
                _.draw(self.screen)

            pg.display.flip()


def launch_game():
    Game().run()
    pg.quit()
