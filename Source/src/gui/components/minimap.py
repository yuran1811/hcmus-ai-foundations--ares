import pygame as pg

from config import GRID_SIZE, MINIMAP_BG_COLOR, MINIMAP_PADDING
from constants.enums import MinimapTileColor
from utils import get_screen_sz


class MiniMap:
    def __init__(self, game_state, width: int, height: int, *, enable_zoom=False):
        self.game_state = game_state
        self.width = width
        self.height = height
        self.padding = MINIMAP_PADDING
        self.surface = pg.Surface((width, height))

        self.dragging = False
        self.last_mouse_pos = pg.Vector2(0, 0)
        self.min_zoom = 0.1
        self.max_zoom = 1.5
        self.zoom_level = 0.2
        self.content_offset = pg.Vector2(0, 0)
        self.fixed_position = pg.Vector2(0, 0)

        self.enable_zoom = enable_zoom

    @property
    def position(self):
        screen_w, screen_h = get_screen_sz()
        self.fixed_position = pg.Vector2(
            screen_w - self.width - self.padding, screen_h - self.height - self.padding
        )

        return self.fixed_position

    def reset_zoom(self):
        self.zoom_level = 0.2

    def is_in_minimap(self, pos: pg.Vector2) -> bool:
        return pg.Rect(
            self.position.x, self.position.y, self.width, self.height
        ).collidepoint(pos)

    def world_to_minimap(self, pos: pg.Vector2) -> pg.Vector2:
        """Convert game world coordinates to minimap coordinates"""
        return (pos * self.zoom_level) - self.content_offset + self.position

    def screen_to_minimap_space(self, screen_pos: pg.Vector2) -> pg.Vector2:
        """Convert screen coordinates to minimap content space"""
        return (screen_pos - self.position + self.content_offset) / self.zoom_level

    def get_tile_color(self, tile_type: str, grid_pos: pg.Vector2) -> tuple:
        base_colors = {
            "wall": MinimapTileColor.get_color(MinimapTileColor.WALL),
            "floor": MinimapTileColor.get_color(MinimapTileColor.FLOOR),
            "stone": MinimapTileColor.get_color(MinimapTileColor.STONE),
            "switch": MinimapTileColor.get_color(MinimapTileColor.SWITCH),
            "sos": MinimapTileColor.get_color(MinimapTileColor.STONE_ON_SWITCH),
        }

        if tile_type == "switch":
            player_grid_pos = self.game_state.player.grid_pos
            if (grid_pos.x, grid_pos.y) == (player_grid_pos.x, player_grid_pos.y):
                return (*base_colors["switch"][:3], 128)

        return base_colors.get(tile_type, (255, 255, 255, 255))

    def draw_map_content(self, screen: pg.Surface):
        tile_size = max(1, int(GRID_SIZE * self.zoom_level))
        map_row, map_col = self.game_state.map.size

        if not self.enable_zoom:
            self.width = (tile_size + 0.2) * map_col // GRID_SIZE
            self.height = (tile_size + 0.4) * map_row // GRID_SIZE

        for y in range(
            int(self.content_offset.y // GRID_SIZE),
            int((self.content_offset.y + self.height) / GRID_SIZE / self.zoom_level),
        ):
            for x in range(
                int(self.content_offset.x // GRID_SIZE),
                int((self.content_offset.x + self.width) / GRID_SIZE / self.zoom_level),
            ):
                if 0 <= y < len(self.game_state.map.tile_grid) and 0 <= x < len(
                    self.game_state.map.tile_grid[y]
                ):
                    tile = self.game_state.map.tile_grid[y][x]
                    minimap_pos = self.world_to_minimap(
                        pg.Vector2(x * GRID_SIZE, y * GRID_SIZE)
                    )
                    if self.bg_rect.collidepoint(minimap_pos):
                        color = self.get_tile_color(tile.tile_type, pg.Vector2(x, y))
                        temp_surf = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
                        temp_surf.fill(color)
                        screen.blit(temp_surf, (minimap_pos.x, minimap_pos.y))

    def draw_viewport_frame(self, screen: pg.Surface):
        if not self.enable_zoom:
            return

        screen_w, screen_h = get_screen_sz()
        frame_size = pg.Vector2(screen_w, screen_h) * self.zoom_level

        game_center = self.game_state.camera + pg.Vector2(screen_w, screen_h) / 2
        minimap_center = self.world_to_minimap(game_center)

        frame_pos = minimap_center - frame_size / 2

        frame_rect = pg.Rect(
            max(
                self.position.x,
                min(frame_pos.x, self.position.x + self.width - frame_size.x),
            ),
            max(
                self.position.y,
                min(frame_pos.y, self.position.y + self.height - frame_size.y),
            ),
            frame_size.x,
            frame_size.y,
        )

        pg.draw.rect(screen, (255, 255, 255), frame_rect, 2)

    def draw_player(self, screen: pg.Surface):
        tile_size = max(1, int(GRID_SIZE * self.zoom_level))
        player_pos = self.world_to_minimap(self.game_state.player.pixel_pos)
        pg.draw.circle(
            screen,
            (0, 255, 0),
            (int(player_pos.x + tile_size / 2), int(player_pos.y + tile_size / 2)),
            int(tile_size * 0.35),
        )

    def draw(self, screen: pg.Surface):
        self.bg_rect = pg.Rect(
            self.position.x,
            self.position.y,
            self.width,
            self.height,
        )
        pg.draw.rect(screen, MINIMAP_BG_COLOR, self.bg_rect, border_radius=5)

        self.draw_map_content(screen)
        self.draw_viewport_frame(screen)
        self.draw_player(screen)

    def handle_event(self, event: pg.event.Event):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_in_minimap(mouse_pos):
                if event.button == 1:  # Left click
                    self.start_drag(mouse_pos)
                elif event.button in (4, 5):  # Mouse wheel
                    if self.enable_zoom:
                        self.handle_zoom(event.button == 4)

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.end_drag()

        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.handle_drag(mouse_pos)

    def start_drag(self, mouse_pos: pg.Vector2):
        self.dragging = True
        self.drag_start_camera = self.game_state.camera.copy()
        self.drag_start_mouse = self.screen_to_minimap_space(mouse_pos)

    def handle_drag(self, mouse_pos: pg.Vector2):
        current_pos = self.screen_to_minimap_space(mouse_pos)
        delta = (current_pos - self.drag_start_mouse) * self.zoom_level

        self.game_state.camera = self.drag_start_camera + delta
        self.constrain_camera()

    def end_drag(self):
        self.dragging = False

        screen_size = pg.Vector2(get_screen_sz())
        viewport_center = self.game_state.camera + screen_size / 2

        self.game_state.camera = viewport_center - screen_size / 2
        self.constrain_camera()

    def handle_zoom(self, zoom_in: bool):
        old_zoom = self.zoom_level
        self.zoom_level += 0.2 if zoom_in else -0.2
        self.zoom_level = max(self.min_zoom, min(self.zoom_level, self.max_zoom))

        # Adjust content offset to keep center position
        zoom_ratio = self.zoom_level / old_zoom
        self.content_offset = (
            self.content_offset + pg.Vector2(self.width / 2, self.height / 2)
        ) * zoom_ratio
        self.content_offset -= pg.Vector2(self.width / 2, self.height / 2)
        self.constrain_content()

    def constrain_camera(self):
        """Keep camera within map bounds"""
        map_w, map_h = self.game_state.map.size
        screen_w, screen_h = get_screen_sz()

        self.game_state.camera.x = max(
            0, min(self.game_state.camera.x, map_w * GRID_SIZE - screen_w)
        )
        self.game_state.camera.y = max(
            0, min(self.game_state.camera.y, map_h * GRID_SIZE - screen_h)
        )

    def constrain_content(self):
        """Keep minimap content within bounds"""
        map_w, map_h = self.game_state.map.size
        max_x = max(0, map_w * self.zoom_level - self.width)
        max_y = max(0, map_h * self.zoom_level - self.height)
        self.content_offset.x = max(0, min(self.content_offset.x, max_x))
        self.content_offset.y = max(0, min(self.content_offset.y, max_y))
