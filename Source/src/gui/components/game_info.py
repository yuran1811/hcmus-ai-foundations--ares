import time

import pygame as pg

from config import INFO_BOX_COLOR

from .decorators import WithFont


class GameInfo(WithFont):
    TEXT_COLORS = {
        "default": (255, 255, 255),
        "fps": (255, 137, 4),
        "steps": (0, 166, 244),
        "weight": (5, 233, 144),
    }

    def __init__(self, x: int = 0, y: int = 0, *, font_size: int = 24, show_fps=False):
        super().__init__(font_size=font_size)

        self.pos = (x, y)

        self.steps = 0
        self.total_weight = 0
        self.current_fps = 0

        self.time_running = False
        self.start_time: float | None = None
        self.final_time = 0.0

        self.show = {
            "fps": show_fps,
        }

    def reset(self):
        self.steps = 0
        self.total_weight = 0
        self.timer_running = False
        self.start_time = time.time()
        self.final_time = 0.0

    def format_time(self, seconds: float) -> str:
        if seconds < 60:
            return f"{int(seconds)}s"

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}m {seconds}s"

    def start_timer(self):
        self.timer_running = True
        self.start_time = time.time()

    def stop_timer(self):
        if self.timer_running and self.start_time:
            self.timer_running = False
            self.final_time = time.time() - self.start_time

    def get_elapsed_time(self):
        if self.timer_running and self.start_time:
            return time.time() - self.start_time
        return self.final_time

    def increment_step(self, weight: int = 0, *, is_reversed=False):
        self.steps += 1 * (-1 if is_reversed else 1)
        self.total_weight += weight * (-1 if is_reversed else 1)

        if self.steps == 1 and not self.timer_running:
            self.start_timer()

    def update(self, dt: float, clock: pg.time.Clock):
        self.current_fps = int(clock.get_fps())

    def draw(self, screen: pg.Surface):
        lines = list(
            filter(
                lambda _: len(_) > 0,
                [
                    f"FPS: {self.current_fps}" if self.show["fps"] else "",
                    f"Steps: {self.steps}",
                    f"Weight: {self.total_weight}",
                    f"Time: {self.format_time(self.get_elapsed_time())}",
                ],
            )
        )

        # Calculate box size
        max_width = max(self.font.size(line)[0] for line in lines)
        total_height = len(lines) * self.font_size * 1.2

        # Create background surface
        info_surface = pg.Surface((max_width + 20, total_height + 10), pg.SRCALPHA)
        pg.draw.rect(
            info_surface, INFO_BOX_COLOR, info_surface.get_rect(), border_radius=5
        )

        # Draw text
        y_offset = 5
        for line in lines:
            text_color = GameInfo.TEXT_COLORS.get(
                line.split(":")[0].lower(), GameInfo.TEXT_COLORS["default"]
            )

            text_surf = self.font.render(line, True, text_color)
            info_surface.blit(text_surf, (10, y_offset))
            y_offset += self.font_size * 1.2

        # Blit to screen
        screen.blit(info_surface, self.pos)
