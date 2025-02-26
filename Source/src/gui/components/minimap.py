import pygame as pg

from config import GRID_SIZE
from utils import get_screen_sz


class MiniMap:
    def __init__(self, game_state, width: int, height: int):
        self.game_state = game_state

        self.width = width
        self.height = height
        self.padding = 10
        self.surface = pg.Surface((width, height))

        self.dragging = False
        self.drag_offset = pg.Vector2(0, 0)

        self.min_zoom = 0.1
        self.max_zoom = 1.0
        self.zoom_level = 0.25  # Initial zoom level (25% of original size)

        self.content_offset = pg.Vector2(0, 0)

    @property
    def position(self):
        screen_width, screen_height = get_screen_sz()

        return pg.Vector2(
            screen_width - self.width - self.padding,
            screen_height - self.height - self.padding,
        )

    def _is_in_minimap(self, pos: pg.Vector2) -> bool:
        """Check if position is within minimap bounds"""
        minimap_pos = self.position
        return pg.Rect(
            minimap_pos.x, minimap_pos.y, self.width, self.height
        ).collidepoint(pos)

    def _constrain_content(self):
        """Keep content within minimap bounds"""
        max_x = max(0, self.game_state.map.size[0] * self.zoom_level - self.width)
        max_y = max(0, self.game_state.map.size[1] * self.zoom_level - self.height)
        self.content_offset.x = max(0, min(self.content_offset.x, max_x))
        self.content_offset.y = max(0, min(self.content_offset.y, max_y))

    def get_tile_color(self, tile_type: str) -> tuple:
        return {
            "wall": (29, 41, 61),
            "floor": (3, 7, 18),
            "stone": (253, 199, 0),
            "switch": (80, 162, 255),
            "sos": (5, 223, 114),
        }.get(tile_type, (0, 0, 0))

    def world_to_minimap(self, pos: pg.Vector2) -> pg.Vector2:
        scale = self.zoom_level
        return pg.Vector2(
            (pos.x * scale) - self.content_offset.x,
            (pos.y * scale) - self.content_offset.y,
        )

    def draw(self, screen: pg.Surface):
        minimap_pos = self.position

        # Draw minimap background
        pg.draw.rect(
            screen,
            (30, 30, 46),
            (minimap_pos.x, minimap_pos.y, self.width, self.height),
            border_radius=5,
        )

        # Draw map tiles
        tile_size = max(1, int(GRID_SIZE * self.zoom_level))
        for y in range(len(self.game_state.map.tile_grid)):
            for x in range(len(self.game_state.map.tile_grid[y])):
                tile = self.game_state.map.tile_grid[y][x]
                screen_pos = self.world_to_minimap(pg.Vector2(x, y) * GRID_SIZE)

                abs_pos = minimap_pos + screen_pos

                if (
                    abs_pos.x + tile_size < minimap_pos.x
                    or abs_pos.x > minimap_pos.x + self.width
                ):
                    continue
                if (
                    abs_pos.y + tile_size < minimap_pos.y
                    or abs_pos.y > minimap_pos.y + self.height
                ):
                    continue

                pg.draw.rect(
                    screen,
                    self.get_tile_color(tile.tile_type),
                    (abs_pos.x, abs_pos.y, tile_size, tile_size),
                )

        # Draw viewport frame
        screen_size = get_screen_sz()
        frame_pos = self.world_to_minimap(self.game_state.camera) + minimap_pos
        frame_rect = pg.Rect(
            frame_pos.x,
            frame_pos.y,
            screen_size[0] * self.zoom_level,
            screen_size[1] * self.zoom_level,
        )
        pg.draw.rect(screen, (255, 255, 255), frame_rect, 2)

        # Draw player
        player_pos = (
            self.world_to_minimap(self.game_state.player.grid_pos * GRID_SIZE)
            + minimap_pos
        )
        pg.draw.circle(
            screen,
            (0, 255, 0),
            (
                int(player_pos.x + tile_size // 4),
                int(player_pos.y + tile_size // 4),
            ),
            max(2, int(4 * self.zoom_level)),
        )

    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        minimap_pos = self.position

        if event.type == pg.MOUSEBUTTONDOWN:
            if self._is_in_minimap(mouse_pos):
                if event.button == 1:  # Left click drag to pan
                    self.dragging = True
                    self.drag_offset = mouse_pos - minimap_pos
                elif event.button == 4:  # Mouse wheel up
                    self.zoom_level = min(self.max_zoom, self.zoom_level + 0.05)
                elif event.button == 5:  # Mouse wheel down
                    self.zoom_level = max(self.min_zoom, self.zoom_level - 0.05)
                self._constrain_content()

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_rel = pg.Vector2(event.rel) * (1 / self.zoom_level)
            self.content_offset -= mouse_rel
            self._constrain_content()
