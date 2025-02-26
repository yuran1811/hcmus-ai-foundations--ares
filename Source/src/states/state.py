from __future__ import annotations

from abc import ABC, abstractmethod

import pygame as pg


class State(ABC):
    def __init__(
        self, *, next_state: State | None = None, prev_state: State | None = None
    ):
        self.set_next_state(next_state)
        self.set_prev_state(prev_state)

    def set_prev_state(self, prev_state: State | None):
        self.prev_state = prev_state

        if prev_state:
            prev_state.next_state = self

    def set_next_state(self, next_state: State | None):
        self.next_state = next_state

        if next_state:
            next_state.prev_state = self

    def prev(self) -> State | None:
        return self.prev_state

    def next(self) -> State | None:
        return self.next_state

    def back(self):
        _prev_state = self.prev()
        if _prev_state:
            self.next_state = _prev_state
            self.next_state.next_state = None

    def responsive_handle(self):
        pass

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pg.Surface):
        pass

    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.back()
