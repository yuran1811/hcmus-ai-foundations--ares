import pygame as pg

from constants.paths import UI_PATH
from utils.asset_loader import get_frame_from_sprite


class Cursor:
    def __init__(self, *, scale_factor: int = 1):
        # Load sprite sheet
        self.sheet = pg.image.load(
            f"{UI_PATH}/cursors/micro-icon-pack/Sprite Sheet (10x10).png"
        ).convert_alpha()
        self.sheet = pg.transform.scale(
            self.sheet,
            (
                self.sheet.get_width() * scale_factor,
                self.sheet.get_height() * scale_factor,
            ),
        )

        # Grid configuration
        self.frame_size = 12 * scale_factor
        self.rows = 8
        self.cols = 8
        self.total_frames = self.rows * self.cols

        # State configuration
        self.states = {
            "normal": {"start": 0, "end": 0},
            "hover": {"start": 1, "end": 1},
            "click": {"start": 2, "end": 2},
            "drag": {"start": 3, "end": 3},
            "disabled": {"start": 5, "end": 5},
            "input": {"start": 6, "end": 6},
        }

        self.current_state = "normal"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.rect = pg.Rect(0, 0, self.frame_size, self.frame_size)

    def set_state(self, state_name: str):
        if state_name in self.states and state_name != self.current_state:
            self.current_state = state_name
            self.frame_index = self.states[state_name]["start"]

    def update(self, dt: float):
        state = self.states[self.current_state]
        self.frame_index += self.animation_speed * dt * 60

        if self.frame_index > state["end"]:
            self.frame_index = state["start"]
        elif self.frame_index < state["start"]:
            self.frame_index = state["start"]

        mouse_pos = pg.mouse.get_pos()
        self.rect.topleft = (
            mouse_pos[0] - 12,
            mouse_pos[1] - 12,
        )

    def draw(self, surface: pg.Surface):
        frame = get_frame_from_sprite(
            self.sheet, self.frame_index, self.frame_size, self.cols
        )

        surface.blit(frame, self.rect)
