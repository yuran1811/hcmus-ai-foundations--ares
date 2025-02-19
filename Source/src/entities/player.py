import pygame as pg

from config import GRID_SIZE, MOVEMENT_SPEED
from utils import load_character_animations


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.animations = load_character_animations()
        self.animation_speed = 0.15

        self.state = "idle"
        self.direction = "front"

        self.frame_index = 0
        self.image = self.get_current_frame()

        self.grid_pos = pg.Vector2(x // GRID_SIZE, y // GRID_SIZE)
        self.pixel_pos = pg.Vector2(
            self.grid_pos.x * GRID_SIZE, self.grid_pos.y * GRID_SIZE
        )
        self.target_pos = self.pixel_pos.copy()
        self.is_moving = False

        __sample_frame = self.animations["idle"]["front"][0]
        self.rect = __sample_frame.get_rect(center=self.pixel_pos)

        # Movement tracking
        self.movement_keys = {
            pg.K_w: "back",
            pg.K_s: "front",
            pg.K_a: "left",
            pg.K_d: "right",
            # Arrow keys
            pg.K_UP: "back",
            pg.K_DOWN: "front",
            pg.K_LEFT: "left",
            pg.K_RIGHT: "right",
        }
        self.active_keys = {}  # Tracks pressed movement keys with timestamps

        # Hitbox setup (smaller than visual sprite)
        self.hitbox_offset = pg.Vector2(0, 0)  # Adjust based on the sprite
        self.hitbox_size = pg.Vector2(40, 40)
        self.hitbox = pg.Rect(0, 0, self.hitbox_size.x, self.hitbox_size.y)
        self.update_hitbox()

    def get_current_frame(self):
        return self.animations[self.state][self.direction][int(self.frame_index)]

    def get_active_direction(self):
        """Determine direction based on most recent key press"""

        if not self.active_keys:
            return None

        # Get the most recently pressed key
        latest_key = max(self.active_keys, key=lambda k: self.active_keys[k])
        return self.movement_keys[latest_key]

    def try_move(self, direction: str):
        if not self.is_moving:
            self.direction = direction
            self.state = "walk"

            # Calculate target grid position
            new_grid_pos = self.grid_pos.copy()
            if direction == "left":
                new_grid_pos.x -= 1
            elif direction == "right":
                new_grid_pos.x += 1
            elif direction == "back":
                new_grid_pos.y -= 1
            elif direction == "front":
                new_grid_pos.y += 1

            # Add collision check here if needed

            self.target_pos = new_grid_pos * GRID_SIZE
            self.is_moving = True

    def handle_event(self, event: pg.event.Event):
        if event.type in (pg.KEYDOWN, pg.KEYUP):
            if event.key in self.movement_keys:
                if event.type == pg.KEYDOWN:
                    self.active_keys[event.key] = pg.time.get_ticks()
                else:
                    if event.key in self.active_keys:
                        del self.active_keys[event.key]

    def update_animation_frame(self, dt: float):
        self.frame_index += self.animation_speed
        frames = self.animations[self.state][self.direction]
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

        self.update_animation_frame(dt)

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        # Convert world position to screen space
        screen_pos = self.pixel_pos - camera
        self.rect.center = screen_pos  # type: ignore

        screen.blit(self.image, self.rect)

    def draw_debug(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw debug information (hitbox, position marker)"""

        # Draw hitbox
        hitbox_screen_rect = self.hitbox.move(-camera.x, -camera.y)
        pg.draw.rect(screen, (255, 0, 0), hitbox_screen_rect, 1)

        # Draw center point
        center_screen_pos = self.pixel_pos - camera
        pg.draw.circle(
            screen, (0, 255, 0), (int(center_screen_pos.x), int(center_screen_pos.y)), 3
        )

        # Draw hitbox center point
        hitbox_center_screen_pos = self.hitbox.center - camera
        pg.draw.circle(
            screen,
            (0, 0, 255),
            (int(hitbox_center_screen_pos.x), int(hitbox_center_screen_pos.y)),
            3,
        )
