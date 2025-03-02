import os
import re
import pygame as pg
from tkinter import filedialog, Tk

from constants.enums import MinimapTileColor
from constants.paths import INPUT_DIR
from utils.asset_loader import get_font

from .button import Button
from .decorators import WithFont


class MapImport(WithFont):
    def __init__(
        self, x: int, y: int, width: int, height: int, *, toggle_rect: pg.Rect
    ):
        super().__init__()
        self.textarea_font = get_font(size=20, font_name="firacode")

        self.active = False

        self.rect = pg.Rect(x, y, width, height)

        self.save_dir = os.path.join(INPUT_DIR, "users")

        self.status_timer = 0
        self.status_message = ""

        self.cursor_pos = 0
        self.text = ""
        self.text_scroll = 0
        self.text_rect = pg.Rect(0, 0, 0, 0)  # Will be set in draw
        self.text_surface = pg.Surface((width - 20, height // 2 - 50))
        self.max_text_lines = 20
        self.preview_zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 4.0
        self.preview_offset = pg.Vector2(0, 0)
        self.dragging_preview = False

        self.tile_size = 16
        self.preview_map = None
        self.preview_surface = pg.Surface((width - 20, height // 2 - 10))

        self.tk_root = Tk()
        self.tk_root.withdraw()

        self.toggle_rect = toggle_rect
        __align_left = toggle_rect.left
        __align_top = toggle_rect.top + 50
        self.buttons = {
            "browse": Button(
                __align_left,
                __align_top,
                0,
                40,
                "Browse",
                self.choose_directory,
                bg=(80, 80, 120),
                fit_content=True,
                calc_rect=lambda _, x, y, w, h: pg.Rect(x, y, w, h),
            ),
            "save": Button(
                __align_left,
                __align_top,
                0,
                40,
                "Save",
                self.save_map,
                bg=(80, 80, 80),
                fit_content=True,
                calc_rect=lambda _, x, y, w, h: pg.Rect(x, y + 50, w, h),
            ),
            "clear": Button(
                __align_left,
                __align_top,
                0,
                40,
                "Clear",
                self.clear_input,
                bg=(150, 0, 0),
                fit_content=True,
                calc_rect=lambda _, x, y, w, h: pg.Rect(x, y + 100, w, h),
            ),
        }

    def is_shown(self):
        return self.active

    def toggle(self):
        self.active = not self.active

    def set_position(self, x: int, y: int, toggle_rect: pg.Rect):
        self.rect.topleft = (x, y)
        self.toggle_rect = toggle_rect

    def choose_directory(self):
        path = filedialog.askdirectory(initialdir=self.save_dir)
        if path:
            self.save_dir = path
            self.status_message = f"Save directory: {os.path.basename(path)}"
            self.status_timer = pg.time.get_ticks()

    def clear_input(self):
        self.text = ""
        self.cursor_pos = 0
        self.text_scroll = 0
        self.preview_map = None
        self.status_message = "Input cleared"
        self.status_timer = pg.time.get_ticks()

    def id_valid_char(self, char: str):
        return char in {"#", " ", ".", "@", "$", "+", "*", "\n"} or bool(
            re.search(r"^\d$", char)
        )

    def parse_map(self):
        try:
            lines = [line for line in self.text.split("\n") if line.strip()]
            if not lines:
                self.preview_map = None
                return

            for line in lines:
                if any(not self.id_valid_char(c) for c in line):
                    raise ValueError("Invalid characters in map")

            self.preview_map = lines
            self.status_message = ""
        except Exception as e:
            self.status_message = f"Error: {str(e)}"
            self.preview_map = None

    def save_map(self):
        if not self.preview_map:
            return

        try:
            file_path = filedialog.asksaveasfilename(
                initialdir=self.save_dir,
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
            )

            if file_path:
                with open(file_path, "w") as f:
                    f.write("\n".join(self.preview_map))
                self.status_message = f"Map saved to {os.path.basename(file_path)}!"
                self.status_timer = pg.time.get_ticks()
        except Exception as e:
            self.status_message = f"Save failed: {str(e)}"
            self.status_timer = pg.time.get_ticks()

    def _ensure_cursor_visible(self):
        """Adjust text scroll to keep cursor in view"""
        cursor_line = self.text[: self.cursor_pos].count("\n")
        text_rect_height = self.rect.height // 2 - 50
        line_height = self.font.get_linesize()
        visible_lines = text_rect_height // line_height

        # Calculate new scroll position
        if cursor_line < self.text_scroll:
            self.text_scroll = max(0, cursor_line)
        elif cursor_line >= self.text_scroll + visible_lines:
            self.text_scroll = max(0, cursor_line - visible_lines + 1)

    def draw(self, screen: pg.Surface):
        # Main container
        pg.draw.rect(screen, (30, 30, 46), self.rect, border_radius=5)
        pg.draw.rect(
            screen, (128, 128, 128), self.rect.inflate(-2, -2), 2, border_radius=4
        )

        # Text input area
        text_rect = self.rect.inflate(-20, -20)
        text_rect.height = self.rect.height // 2 - 50
        screen.blit(self.text_surface, (text_rect.x, text_rect.y))
        self.draw_text_input(screen, text_rect)

        # Preview area
        preview_rect = pg.Rect(
            self.rect.x + 10,
            self.rect.y + self.rect.height // 2 - 30,
            self.rect.width - 20,
            self.rect.height // 2 - 10,
        )
        pg.draw.rect(screen, (20, 20, 30), preview_rect, border_radius=5)
        self.draw_preview(screen, preview_rect)

        # Buttons
        self.draw_buttons(screen)

        # Status message
        if self.status_message:
            status_text = self.font.render(self.status_message, True, (255, 255, 255))
            screen.blit(status_text, (self.rect.x + 10, self.rect.bottom - 40))

    def draw_preview(self, screen: pg.Surface, rect: pg.Rect):
        if not self.preview_map:
            return

        # Apply zoom
        tile_size = int(16 * self.preview_zoom)
        map_width = max(len(line) for line in self.preview_map) * tile_size
        map_height = len(self.preview_map) * tile_size

        # Calculate visible area
        start_x = max(0, min(self.preview_offset.x, map_width - rect.width))
        start_y = max(0, min(self.preview_offset.y, map_height - rect.height))

        # Draw visible portion
        for y, row in enumerate(self.preview_map):
            for x, char in enumerate(row):
                screen_x = rect.x + x * tile_size - start_x
                screen_y = rect.y + y * tile_size - start_y

                if screen_x + tile_size < rect.left or screen_x > rect.right:
                    continue
                if screen_y + tile_size < rect.top or screen_y > rect.bottom:
                    continue

                color = MinimapTileColor.get_color_by_char(char)
                pg.draw.rect(
                    screen, color, (screen_x, screen_y, tile_size - 1, tile_size - 1)
                )

    def draw_text_input(self, screen: pg.Surface, rect: pg.Rect):
        # Set clipping region
        original_clip = screen.get_clip()
        screen.set_clip(rect)

        lines = self.text.split("\n")
        line_height = self.textarea_font.get_linesize()
        visible_lines = rect.height // line_height

        # Calculate vertical scroll limits
        max_scroll = max(0, len(lines) - visible_lines)
        self.text_scroll = max(0, min(self.text_scroll, max_scroll))

        y_offset = 0

        # Render visible lines with horizontal clipping
        for line in lines[self.text_scroll : self.text_scroll + visible_lines]:
            text_surf = self.textarea_font.render(line, True, (255, 255, 255))

            # Calculate horizontal visibility
            text_width = text_surf.get_width()
            if text_width > rect.width - 10:  # Account for scrollbar
                # Create subsurface for horizontal clipping
                visible_text = text_surf.subsurface(
                    (0, 0, rect.width - 15, line_height)
                )
            else:
                visible_text = text_surf

            screen.blit(visible_text, (rect.x + 5, rect.y + 5 + y_offset))
            y_offset += line_height

        # Draw cursor (clipped to input area)
        if self.active:
            cursor_line = self.text[: self.cursor_pos].count("\n")
            cursor_col = len(self.text[: self.cursor_pos].split("\n")[-1])
            visible_lines = rect.height // line_height

            # Only draw if cursor is in visible area
            if self.text_scroll <= cursor_line < self.text_scroll + visible_lines:
                line = lines[cursor_line] if cursor_line < len(lines) else ""
                text_before_cursor = line[:cursor_col]
                cursor_x = self.textarea_font.size(text_before_cursor)[0]
                cursor_y = (cursor_line - self.text_scroll) * line_height

                # Clip cursor to input width
                if cursor_x < rect.width - 15:
                    pg.draw.line(
                        screen,
                        (255, 255, 255),
                        (rect.x + 5 + cursor_x, rect.y + 5 + cursor_y),
                        (rect.x + 5 + cursor_x, rect.y + 5 + cursor_y + line_height),
                        2,
                    )

        # Draw scrollbar (if needed)
        total_lines = len(lines)
        if total_lines > visible_lines:
            scroll_height = rect.height * (visible_lines / total_lines)
            scroll_pos = rect.y + (self.text_scroll / total_lines - 1) * rect.height
            pg.draw.rect(
                screen,
                (80, 80, 120),
                (
                    rect.right - 8,
                    scroll_pos,
                    5,
                    scroll_height,
                ),
                border_radius=2,
            )

        # Reset clipping region
        screen.set_clip(original_clip)

    def draw_buttons(self, screen: pg.Surface):
        self.buttons["save"].bg = (0, 150, 0) if self.preview_map else (80, 80, 80)

        for btn in self.buttons.values():
            btn.draw(screen)

    def update(self):
        for btn in self.buttons.values():
            btn.update()

        # Clear status message after 3 seconds
        if self.status_timer and pg.time.get_ticks() - self.status_timer > 3000:
            self.status_message = ""
            self.status_timer = 0

    def handle_event(self, event: pg.event.Event):
        for btn in self.buttons.values():
            btn.handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())

            preview_rect = pg.Rect(
                self.rect.x + 10,
                self.rect.y + self.rect.height // 2 - 30,
                self.rect.width - 20,
                self.rect.height // 2 - 10,
            )
            if preview_rect.collidepoint(mouse_pos):
                self.dragging_preview = True
                self.drag_start_pos = mouse_pos
                self.drag_start_offset = self.preview_offset.copy()

            self.active = (
                self.toggle_rect.collidepoint(event.pos)
                or self.rect.collidepoint(mouse_pos)
                or any(x.clicked or x.hovered for x in self.buttons.values())
            )

        if event.type == pg.MOUSEBUTTONUP:
            self.dragging_preview = False

        if event.type == pg.MOUSEMOTION and self.dragging_preview:
            delta = pg.Vector2(pg.mouse.get_pos()) - self.drag_start_pos
            self.preview_offset = self.drag_start_offset - delta * self.preview_zoom
            self.preview_offset.x = max(
                0,
                min(
                    self.preview_offset.x,
                    max(
                        0,
                        (
                            max(len(line) for line in (self.preview_map or [""]))
                            * 16
                            * self.preview_zoom
                        )
                        - (self.rect.width - 20),
                    ),
                ),
            )
            self.preview_offset.y = max(
                0,
                min(
                    self.preview_offset.y,
                    max(
                        0,
                        (len(self.preview_map or []) * 16 * self.preview_zoom)
                        - (self.rect.height // 2 - 10),
                    ),
                ),
            )

        if event.type == pg.MOUSEWHEEL:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())

            if self.rect.collidepoint(mouse_pos):
                if mouse_pos.y < self.rect.y + self.rect.height // 2 - 50:  # Text area
                    self.text_scroll = max(0, self.text_scroll - event.y)
                else:
                    # Zoom with Ctrl/Cmd
                    if pg.key.get_mods() & (pg.KMOD_CTRL | pg.KMOD_META):
                        self.preview_zoom = max(
                            self.min_zoom,
                            min(
                                self.max_zoom,
                                self.preview_zoom * (1.1 if event.y > 0 else 0.9),
                            ),
                        )
                    else:
                        # Pan
                        self.preview_offset.y += event.y * 20

        if self.active and event.type == pg.KEYDOWN:
            if event.key == pg.K_v and (
                event.mod & pg.KMOD_CTRL or event.mod & pg.KMOD_META
            ):
                try:
                    # Get clipboard content
                    clipboard_text = self.tk_root.clipboard_get()
                    filtered_text = "".join(
                        [c for c in clipboard_text if self.id_valid_char(c)]
                    )

                    self.text = (
                        self.text[: self.cursor_pos]
                        + filtered_text
                        + self.text[self.cursor_pos :]
                    )
                    self.cursor_pos += len(filtered_text)
                    self.parse_map()
                except Exception as _:
                    self.status_message = "Clipboard error"
                    self.status_timer = pg.time.get_ticks()
                return

            match event.key:
                case pg.K_RETURN:
                    if len(self.text) and self.text[-1] != "\n":
                        self.text = f"{self.text[: self.cursor_pos]}\n{self.text[self.cursor_pos :]}"
                        self.cursor_pos += 1

                case pg.K_HOME:
                    start = self.text.rfind("\n", 0, self.cursor_pos) + 1
                    self.cursor_pos = max(0, start)
                case pg.K_END:
                    end = self.text.find("\n", self.cursor_pos)
                    self.cursor_pos = end if end != -1 else len(self.text)

                case pg.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = f"{self.text[: self.cursor_pos - 1]}{self.text[self.cursor_pos :]}"
                        self.cursor_pos -= 1
                case pg.K_DELETE:
                    if self.cursor_pos >= 0 and self.cursor_pos < len(self.text):
                        self.text = f"{self.text[: self.cursor_pos]}{self.text[self.cursor_pos + 1 :]}"

                case pg.K_UP:
                    lines = self.text[: self.cursor_pos].split("\n")
                    if len(lines) > 1:
                        cur_line_len = len(lines[-1])
                        prev_line_len = len(lines[-2])
                        offset = (
                            prev_line_len
                            if cur_line_len < prev_line_len
                            else cur_line_len
                        )

                        self.cursor_pos = max(
                            0,
                            self.cursor_pos - 1 - offset,
                        )
                case pg.K_DOWN:
                    all_lines = self.text.split("\n")
                    current_line_index = self.text[: self.cursor_pos].count("\n")

                    if current_line_index < len(all_lines) - 1:
                        lines_to_skip = all_lines[:current_line_index]
                        previous_lines_length = sum(
                            len(line) + 1 for line in lines_to_skip
                        )  # +1 for \n

                        next_line = all_lines[current_line_index + 1]
                        next_line_length = len(next_line)

                        current_column = self.cursor_pos - previous_lines_length
                        if current_column < 0:
                            current_column = len(all_lines[current_line_index])
                        else:
                            current_column -= 1

                        new_column = min(current_column, next_line_length)

                        self.cursor_pos = min(
                            len(self.text),
                            self.cursor_pos
                            - current_column
                            + len(all_lines[current_line_index])
                            + bool(new_column != next_line_length)
                            + new_column,
                        )
                case pg.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                case pg.K_RIGHT:
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)

                case _:
                    if self.id_valid_char(event.unicode):
                        self.text = (
                            self.text[: self.cursor_pos]
                            + event.unicode
                            + self.text[self.cursor_pos :]
                        )
                        self.cursor_pos += len(event.unicode)

            self.parse_map()
            self._ensure_cursor_visible()
