from collections.abc import Callable
from typing import Any

import pygame as pg

from constants.enums import Direction

from .decorators import WithLabel


class SelectComponent(WithLabel):
    def __init__(
        self,
        x: float,
        y: float,
        options: list[str],
        default_index=0,
        *,
        placeholder="Select an option",
        label="",
        show_label: bool = False,
        direction: Direction = Direction.DOWN,
        width: int | None = None,
        height=400,
        option_height=40,
        on_select: Callable[[Any], Any] | None = None,
    ):
        super().__init__(label=label)

        self.placeholder = placeholder

        self.show_label = show_label
        self.direction = direction

        self.options = options
        self.option_rects: list[pg.Rect] = []

        self.expanded = False
        self.default_index = default_index
        self.selected_index = default_index

        self.width = width if width else max(len(option) for option in options) * 14
        self.height = height
        self.option_height = option_height
        self.origin_rect = pg.Rect(x, y, self.width, option_height)
        self.rect = self.origin_rect.copy()

        self.scroll_offset = 0

        self.num_options = len(options)
        self.visible_options = min(self.num_options, self.height // self.option_height)

        self.on_select = on_select

    def reset(self):
        self.selected_index = self.default_index

    def change_selected_idx(self, selected_index: int | None = None):
        if selected_index is not None:
            self.selected_index = selected_index

    def update_rect_topleft(self, x: int, y: int):
        self.origin_rect.topleft = (x, y)

    def update(self):
        pass

    def draw(self, screen: pg.Surface):
        self.rect = self.origin_rect.copy()

        if self.show_label:
            label_rect = self.draw_label(screen, center=self.rect.center)

            if self.direction == Direction.UP:
                self.rect.centery -= self.height
            self.rect.centerx += label_rect.width

        # Draw main selection box
        bg_color = (106, 106, 149) if self.expanded else (30, 30, 46)
        pg.draw.rect(screen, bg_color, self.rect, border_radius=5)

        # Draw selected item
        selected_text = self.font.render(
            self.options[self.selected_index]
            if self.selected_index > -1
            else self.placeholder,
            True,
            (255, 255, 255),
        )
        screen.blit(selected_text, selected_text.get_rect(center=self.rect.center))

        if self.expanded:
            # Calculate visible range
            start_index = self.scroll_offset // self.option_height
            end_index = start_index + self.visible_options

            # Create scrollable area surface
            options_surface = pg.Surface((self.rect.width, self.height), pg.SRCALPHA)
            options_surface.fill((0, 0, 0, 0))

            # Draw visible options
            for i in range(start_index, min(end_index, len(self.options))):
                option_rect = pg.Rect(
                    0,
                    i * self.option_height - self.scroll_offset,
                    self.rect.width,
                    self.option_height,
                )

                color = (80, 80, 100) if i == self.selected_index else (50, 50, 70)
                pg.draw.rect(options_surface, color, option_rect, border_radius=5)

                option_text = self.font.render(self.options[i], True, (255, 255, 255))
                text_rect = option_text.get_rect(center=option_rect.center)
                options_surface.blit(option_text, text_rect)

            # Draw scrollbar if needed
            if self.num_options > self.visible_options:
                scrollbar_width = 8
                scrollbar_height = (
                    self.visible_options / self.num_options
                ) * self.height
                scrollbar_y = (
                    self.scroll_offset / (self.num_options * self.option_height)
                ) * self.height

                pg.draw.rect(
                    options_surface,
                    (100, 100, 120),
                    (
                        self.rect.width - scrollbar_width - 2,
                        scrollbar_y,
                        scrollbar_width,
                        scrollbar_height,
                    ),
                    border_radius=4,
                )

            # Determine position based on direction
            if self.direction == Direction.UP:
                options_pos = (self.rect.x, self.rect.y - self.height)
            else:
                options_pos = (self.rect.x, self.rect.y + self.rect.height)

            screen.blit(options_surface, options_pos)

    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.mouse.get_pos()

        # Calculate expanded area based on direction
        expanded_rect = self.rect.copy()
        expanded_rect.height += self.height
        if self.direction == Direction.UP:
            expanded_rect.y -= self.height

        # Check if mouse is outside of component
        if not expanded_rect.collidepoint(mouse_pos):
            if self.expanded and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.expanded = False
            return

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                self.scroll_offset = 0
            elif self.expanded:
                if self.direction == Direction.UP:
                    options_top = self.rect.y - self.height
                else:
                    options_top = self.rect.y + self.rect.height

                rel_y = event.pos[1] - options_top
                clicked_index = (rel_y + self.scroll_offset) // self.option_height

                if 0 <= clicked_index < len(self.options):
                    self.selected_index = clicked_index
                    self.expanded = False

                    if self.on_select:
                        self.on_select(clicked_index)

        if event.type == pg.MOUSEWHEEL and self.expanded:
            max_offset = max(0, self.num_options * self.option_height - self.height)
            self.scroll_offset = max(
                0, min(self.scroll_offset - event.y * self.option_height, max_offset)
            )
