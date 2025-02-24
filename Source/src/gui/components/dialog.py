import random
from collections.abc import Callable

import pygame as pg

from utils.config import get_screen_sz

from .button import Button
from .decorators import WithFont


class VictoryDialog(WithFont):
    def __init__(
        self,
        *,
        on_replay: Callable[[], None] | None = None,
        on_next_map: Callable[[], None] | None = None,
    ):
        super().__init__()

        screen_size = get_screen_sz()

        self.rect = pg.Rect(0, 0, 400, 200)
        self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)

        self.replay_button = (
            Button(
                self.rect.centerx - 105,
                self.rect.centery + 40,
                120,
                40,
                "Replay",
                on_replay,
            )
            if on_replay
            else None
        )
        self.next_button = Button(
            self.rect.centerx - (-25 if on_replay else 40),
            self.rect.centery + 40,
            80,
            40,
            "Next",
            on_next_map,
        )
        self.buttons = {
            "replay": self.replay_button,
            "next": self.next_button,
        }

        self.confetti_fire = False
        self.max_confetti = 100
        self.default_max_confetti_shots = 5
        self.max_confetti_shots = 5
        self.confetti = []
        self.confetti_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
        ]

    def reset(self):
        self.confetti_fire = False
        self.confetti = []
        self.max_confetti_shots = 5

    def toggle_confetti(self, value: bool | None = None):
        self.confetti_fire = value if value is not None else not self.confetti_fire

        if (not self.confetti_fire) and self.confetti:
            self.confetti = []
            self.max_confetti_shots = self.default_max_confetti_shots

    def generate_confetti(self):
        if not self.confetti_fire:
            return

        screen_width, screen_height = get_screen_sz()
        for _ in range(self.max_confetti):
            self.confetti.append(
                {
                    "pos": pg.Vector2(screen_width // 2, screen_height // 2),
                    "velocity": pg.Vector2(
                        random.uniform(-5, 5), random.uniform(-10, 0)
                    ),
                    "rotation": random.uniform(0, 360),
                    "rotation_speed": random.uniform(-5, 5),
                    "color": random.choice(self.confetti_colors),
                    "size": random.randint(4, 8),
                    "lifetime": random.uniform(1.5, 3.0),
                    "timer": 0.0,
                    "alpha": 255,
                    # Add flip properties
                    "flip_time": random.uniform(0.1, 0.3),
                    "flip_timer": 0.0,
                    "flip_x": random.choice([True, False]),
                    "flip_y": random.choice([True, False]),
                }
            )

    def update_confetti(self, dt):
        for p in self.confetti:
            # Update physics
            p["velocity"].y += 9.8 * dt
            p["pos"] += p["velocity"] * 60 * dt
            p["rotation"] += p["rotation_speed"]
            p["timer"] += dt
            p["flip_timer"] += dt

            # Update flip state
            if p["flip_timer"] >= p["flip_time"]:
                p["flip_x"] = not p["flip_x"] if random.random() < 0.5 else p["flip_x"]
                p["flip_y"] = not p["flip_y"] if random.random() < 0.5 else p["flip_y"]
                p["flip_timer"] = 0.0

            # Fade out
            alpha = 255 * (1 - (p["timer"] / p["lifetime"]))
            p["alpha"] = max(0, min(255, int(alpha)))

    def draw_confetti(self, screen):
        for p in self.confetti:
            if p["timer"] < p["lifetime"]:
                # Create base surface
                surf = pg.Surface((p["size"], p["size"]), pg.SRCALPHA)
                surf.fill((*p["color"], p["alpha"]))

                # Apply transformations
                rotated_surf = pg.transform.rotate(surf, p["rotation"])
                flipped_surf = pg.transform.flip(rotated_surf, p["flip_x"], p["flip_y"])

                # Draw to screen
                screen.blit(flipped_surf, flipped_surf.get_rect(center=p["pos"]))

    def update(self, dt: float):
        self.update_confetti(dt)
        if (
            self.confetti_fire
            and self.max_confetti_shots > 0
            and all(p["timer"] >= p["lifetime"] - 2.25 for p in self.confetti)
        ):
            self.max_confetti_shots -= 1
            self.generate_confetti()

        self.replay_button.update() if self.replay_button else None
        self.next_button.update()

    def draw(self, screen: pg.Surface):
        screen_size = get_screen_sz()

        # Dark background overlay
        overlay = pg.Surface((screen_size[0], screen_size[1]), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Dialog box
        pg.draw.rect(screen, (30, 30, 46), self.rect, border_radius=10)
        text = self.font.render("Level Complete!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery - 30))
        screen.blit(text, text_rect)

        self.draw_confetti(screen)
        self.replay_button.draw(screen) if self.replay_button else None
        self.next_button.draw(screen)

    def handle_event(self, event: pg.event.Event):
        self.replay_button.handle_event(event) if self.replay_button else None
        self.next_button.handle_event(event)
