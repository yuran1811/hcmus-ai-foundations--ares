import pygame as pg

from config import FPS, GAME_TITLE
from gui.components import BGMController, Cursor
from states.menu_state import MenuState
from states.state import State
from utils import get_screen_sz, update_screen_sz


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(GAME_TITLE)
        pg.mouse.set_visible(False)

        screen_size = get_screen_sz()
        self.screen = pg.display.set_mode(screen_size, pg.RESIZABLE)

        self.clock = pg.time.Clock()
        self.cursor = Cursor(scale_factor=4)
        self.bgms_controller = BGMController()

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

                if event.type == pg.VIDEORESIZE:
                    update_screen_sz(event.size)

                if (
                    event.type == pg.VIDEORESIZE
                    or event.type == pg.WINDOWRESIZED
                    or event.type == pg.WINDOWSIZECHANGED
                ):
                    pg.display.set_mode(get_screen_sz(), pg.RESIZABLE)
                    [_.responsive_handle() for _ in self.state_hist]

                self.state.handle_event(event)

            # Update and draw
            for _ in [self.state, self.cursor]:
                _.update(self.dt)
                _.draw(self.screen)

            pg.display.flip()


def launch_game():
    Game().run()
    pg.quit()
