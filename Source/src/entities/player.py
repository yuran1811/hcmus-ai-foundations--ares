from collections.abc import Callable

import pygame as pg

from config import GRID_SIZE, MOVEMENT_SPEED
from constants.enums import Direction
from utils import load_character_animations

from .map import Map


class Player(pg.sprite.Sprite):
    def __init__(self, *, pos: tuple[float, float] = (0.0, 0.0), map: Map):
        super().__init__()

        self.map = map

        self.animations = load_character_animations()
        self.animation_speed = 0.1

        self.state = "idle"
        self.direction = Direction.DOWN

        self.frame_index = 0
        self.image = self.get_current_frame()

        self.grid_pos = pg.Vector2(
            pos[0] // GRID_SIZE,
            pos[1] // GRID_SIZE,
        )
        self.pixel_pos = pg.Vector2(
            self.grid_pos.x * GRID_SIZE,
            self.grid_pos.y * GRID_SIZE,
        )
        self.target_pos = self.pixel_pos.copy()
        self.is_moving = False

        __sample_frame = self.animations["idle"][Direction.DOWN.value[1]][0]
        self.rect = __sample_frame.get_rect(center=self.pixel_pos)

        # Movement tracking
        self.movement_keys = {
            pg.K_w: Direction.UP,
            pg.K_s: Direction.DOWN,
            pg.K_a: Direction.LEFT,
            pg.K_d: Direction.RIGHT,
            # Arrow keys
            pg.K_UP: Direction.UP,
            pg.K_DOWN: Direction.DOWN,
            pg.K_LEFT: Direction.LEFT,
            pg.K_RIGHT: Direction.RIGHT,
        }
        self.active_keys = {}  # Tracks pressed movement keys with timestamps

        # Hitbox setup (smaller than visual sprite)
        self.hitbox_offset = pg.Vector2(0, 0)  # Adjust based on the sprite
        self.hitbox_size = pg.Vector2(40, 40)
        self.hitbox = pg.Rect(0, 0, self.hitbox_size.x, self.hitbox_size.y)
        self.update_hitbox()

    def get_current_frame(self):
        return self.animations[self.state][self.direction.value[1]][
            int(self.frame_index)
        ]

    def get_screen_center(self):
        return self.pixel_pos + pg.Vector2(GRID_SIZE // 2, GRID_SIZE // 2)

    def try_move(
        self,
        direction: Direction,
        *,
        on_move: Callable[..., None] | None = None,
    ):
        if self.is_moving:
            return

        dir_vec = Direction.get_vec(direction)
        new_grid_pos = self.grid_pos.copy() + dir_vec
        target_tile = self.map.get_tile_at(
            new_grid_pos.x * GRID_SIZE + GRID_SIZE // 2,
            new_grid_pos.y * GRID_SIZE + GRID_SIZE // 2,
        )

        if not target_tile:
            return

        if target_tile.passable:
            on_move() if on_move else None
            self.start_movement(new_grid_pos, direction)
        elif target_tile.tile_type == "stone" or target_tile.tile_type == "sos":
            push_pos = new_grid_pos + dir_vec
            push_tile = self.map.get_tile_at(
                push_pos.x * GRID_SIZE + GRID_SIZE // 2,
                push_pos.y * GRID_SIZE + GRID_SIZE // 2,
            )

            if push_tile and push_tile.passable:
                self.map.move_stone(
                    new_grid_pos,
                    push_pos,
                    on_move=on_move,
                )
                self.start_movement(new_grid_pos, direction)

    def start_movement(self, new_grid_pos: pg.Vector2, direction: Direction):
        self.direction = direction
        self.state = "walk"
        self.target_pos = new_grid_pos * GRID_SIZE
        self.is_moving = True

    def update_animation_frame(self):
        self.frame_index += self.animation_speed
        frames = self.animations[self.state][self.direction.value[1]]
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = self.get_current_frame()

    def update_hitbox(self):
        self.hitbox.center = self.pixel_pos + self.hitbox_offset  # type: ignore

    def update(self, dt: float):
        if self.is_moving:
            move_vec = self.target_pos - self.pixel_pos
            distance = move_vec.length() // 1

            if distance > 1:
                # Move with fixed speed
                move_vec.scale_to_length(MOVEMENT_SPEED * dt)
                self.pixel_pos += move_vec
                self.rect.center = self.pixel_pos  # type: ignore
                self.update_hitbox()
            else:
                # Snap to grid when reaching target
                self.pixel_pos = self.target_pos.copy()
                self.grid_pos = self.target_pos // GRID_SIZE
                self.is_moving = False
                self.state = "idle"

        self.update_animation_frame()

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        _screen = self.get_screen_center() - camera

        self.rect.center = (int(_screen.x), int(_screen.y))
        screen.blit(self.image, self.rect)

    def draw_debug(self, screen: pg.Surface, camera: pg.Vector2):
        # hitbox
        hitbox_screen_rect = self.hitbox.move(
            -camera.x + GRID_SIZE // 2, -camera.y + GRID_SIZE // 2
        )
        pg.draw.rect(screen, (255, 0, 0), hitbox_screen_rect, 1)

        # center
        _screen = self.get_screen_center() - camera
        pg.draw.circle(
            screen,
            (0, 255, 0),
            (int(_screen.x), int(_screen.y)),
            5,
        )

        # hitbox center
        hitbox_center_screen_pos = self.hitbox.center - camera
        pg.draw.circle(
            screen,
            (0, 0, 255),
            (
                int(hitbox_center_screen_pos.x + GRID_SIZE // 2),
                int(hitbox_center_screen_pos.y + GRID_SIZE // 2),
            ),
            3,
        )

    def handle_event(
        self, event: pg.event.Event, *, on_move: Callable[..., None] | None = None
    ):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_w, pg.K_UP]:
                self.try_move(Direction.UP, on_move=on_move)
            if event.key in [pg.K_s, pg.K_DOWN]:
                self.try_move(Direction.DOWN, on_move=on_move)
            if event.key in [pg.K_a, pg.K_LEFT]:
                self.try_move(Direction.LEFT, on_move=on_move)
            if event.key in [pg.K_d, pg.K_RIGHT]:
                self.try_move(Direction.RIGHT, on_move=on_move)

        if event.type in (pg.KEYDOWN, pg.KEYUP):
            if event.key in self.movement_keys:
                if event.type == pg.KEYDOWN:
                    self.active_keys[event.key] = pg.time.get_ticks()
                else:
                    if event.key in self.active_keys:
                        del self.active_keys[event.key]
