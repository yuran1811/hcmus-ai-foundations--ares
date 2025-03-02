from collections.abc import Callable
from typing import Any

import pygame as pg

from constants.enums import Orientation
from constants.paths import UI_PATH
from utils import get_speed
from utils.asset_loader import get_frame_from_sprite

from .button import Button
from .decorators import WithLabel


class MediaController(WithLabel):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        *,
        label="",
        show_label: bool = False,
        show_play: bool = False,
        show_speed: bool = False,
        show_mute: bool = False,
        show_zoom: bool = False,
        is_playing: bool = False,
        is_muted: bool = False,
        orientation=Orientation.HORIZONTAL,
        scale_factor: int = 1,
        on_home: Callable | None = None,
        on_backward: Callable | None = None,
        on_forward: Callable | None = None,
        on_play: Callable | None = None,
        on_pause: Callable | None = None,
        on_speed_down: Callable | None = None,
        on_speed_up: Callable | None = None,
        on_prev: Callable | None = None,
        on_next: Callable | None = None,
        on_unmute: Callable | None = None,
        on_mute: Callable | None = None,
        on_loop: Callable | None = None,
        on_reset: Callable | None = None,
        on_zoom_in: Callable | None = None,
        on_zoom_out: Callable | None = None,
    ):
        super().__init__(label=label)

        self.show_label = show_label
        self.show_play = show_play
        self.show_speed = show_speed
        self.show_mute = show_mute
        self.show_zoom = show_zoom
        self.orientation = orientation

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

        self.state = {
            "play": is_playing or False,
            "loop": False,
            "mute": is_muted or False,
            "speed": 1,
        }

        self.rows = 8
        self.cols = 8
        self.animation_speed = 0.15
        self.frame_size = 12 * scale_factor
        self.gap = self.frame_size / 4

        self.origin_rect = pg.Rect(x, y, self.frame_size, self.frame_size)
        self.rect = self.origin_rect.copy()

        self.callbacks = {
            "on_play": on_play,
            "on_pause": on_pause,
            "on_speed_down": on_speed_down,
            "on_speed_up": on_speed_up,
            "on_mute": on_mute,
            "on_unmute": on_unmute,
        }

        self.controllers = {
            "home": self.create_controller_item(20, on_home),
            "backward": self.create_controller_item(36, on_backward),
            "forward": self.create_controller_item(37, on_forward),
            "play_pause": self.create_controller_item(
                45 if self.state["play"] else 44,
                self.toggle_play_pause,
            ),
            "speed_down": self.create_controller_item(46, self.handle_speed_down),
            "speed_up": self.create_controller_item(47, self.handle_speed_up),
            "prev": self.create_controller_item(48, on_prev),
            "next": self.create_controller_item(49, on_next),
            "unmute": self.create_controller_item(
                51 if self.state["mute"] else 50, self.toggle_mute
            ),
            "loop": self.create_controller_item(54, on_loop),
            "reset": self.create_controller_item(23, on_reset),
            "zoom_in": self.create_controller_item(30, on_zoom_in),
            "zoom_out": self.create_controller_item(31, on_zoom_out),
        }
        self.components: dict[str, Any] = {}

        self.init_components(x, y)

    def create_controller_item(self, frame_idx: int, callback: Callable | None):
        return {
            "frame": get_frame_from_sprite(
                self.sheet, frame_idx, self.frame_size, self.cols
            ),
            "on_click": callback,
        }

    def init_components(self, x: int = 0, y: int = 0):
        count: int = 0
        base_x = x
        base_y = y

        # Calculate label offset
        if self.show_label:
            label_size = self.font.size(self.label)
            if self.orientation == Orientation.HORIZONTAL:
                base_x += label_size[0] + self.gap
            else:
                base_y += label_size[1] + self.gap

        for name, component in self.controllers.items():
            if (
                not component["on_click"]
                or (name.startswith("speed") and not self.show_speed)
                or (name == "unmute" and not self.show_mute)
                or (name == "play_pause" and not self.show_play)
                or ((name == "zoom_in" or name == "zoom_out") and not self.show_zoom)
            ):
                continue

            # Calculate component position based on orientation
            if self.orientation == Orientation.HORIZONTAL:
                pos = (base_x + count * (self.frame_size + self.gap), base_y)
            else:
                pos = (base_x, base_y + count * (self.frame_size + self.gap))

            self.components[name] = Button(
                int(pos[0]),
                int(pos[1]),
                self.frame_size,
                self.frame_size,
                "",
                component["on_click"],
            )
            count += 1

    def toggle_state(self, key: str, events: tuple[Callable | None, Callable | None]):
        self.state[key] = not self.state[key]
        if self.state[key]:
            if events[0]:
                events[0]()
        else:
            if events[1]:
                events[1]()

    def toggle_play_pause(self):
        self.toggle_state(
            "play", (self.callbacks["on_play"], self.callbacks["on_pause"])
        )

    def toggle_mute(self):
        self.toggle_state(
            "mute", (self.callbacks["on_mute"], self.callbacks["on_unmute"])
        )

    def handle_speed_down(self):
        self.state["speed"] = get_speed(self.state["speed"], False)
        if self.callbacks["on_speed_down"]:
            self.callbacks["on_speed_down"](int(self.state["speed"]))

    def handle_speed_up(self):
        self.state["speed"] = get_speed(self.state["speed"], True)
        if self.callbacks["on_speed_up"]:
            self.callbacks["on_speed_up"](int(self.state["speed"]))

    def get_play_pause_frame(self):
        return get_frame_from_sprite(
            self.sheet, 45 if self.state["play"] else 44, self.frame_size, self.cols
        )

    def get_unmute_frame(self):
        return get_frame_from_sprite(
            self.sheet, 50 if not self.state["mute"] else 51, self.frame_size, self.cols
        )

    def update_rect_topleft(self, x: int, y: int):
        self.origin_rect.topleft = (x, y)

    def update(self, dt: float):
        [_.update() for _ in self.components.values()]

    def draw(self, screen: pg.Surface):
        self.rect = self.origin_rect.copy()

        current_pos = [self.origin_rect.x, self.origin_rect.y]

        # Draw label
        if self.show_label:
            label_rect = self.draw_label(
                screen,
                center=(
                    self.origin_rect.centerx
                    if self.orientation == Orientation.VERTICAL
                    else current_pos[0],
                    self.origin_rect.centery
                    if self.orientation == Orientation.HORIZONTAL
                    else current_pos[1],
                ),
            )
            if self.orientation == Orientation.HORIZONTAL:
                current_pos[0] += label_rect.width + self.gap  # type: ignore
            else:
                current_pos[1] += label_rect.height + self.gap  # type: ignore

        # Draw components and icons
        for name in self.components:
            if self.orientation == Orientation.HORIZONTAL:
                self.components[name].rect.topleft = (current_pos[0], current_pos[1])
            else:
                self.components[name].rect.topleft = (current_pos[0], current_pos[1])

            if (
                (name.startswith("speed") and not self.show_speed)
                or (name == "unmute" and not self.show_mute)
                or (name == "play_pause" and not self.show_play)
                or ((name == "zoom_in" or name == "zoom_out") and not self.show_zoom)
            ):
                continue

            self.components[name].draw(screen)

            # Get appropriate frame
            if name == "play_pause":
                frame = self.get_play_pause_frame()
            elif name == "unmute":
                frame = self.get_unmute_frame()
            else:
                frame = self.controllers[name]["frame"]

            # Draw icon
            screen.blit(frame, self.components[name].rect.topleft)

            # Update position for next component
            if self.orientation == Orientation.HORIZONTAL:
                current_pos[0] += self.frame_size + self.gap  # type: ignore
            else:
                current_pos[1] += self.frame_size + self.gap  # type: ignore

    def handle_event(self, event: pg.event.Event):
        [_.handle_event(event) for _ in self.components.values()]
