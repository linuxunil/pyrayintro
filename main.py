#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["raylib"]
# ///

import random
import math
from dataclasses import dataclass

import pyray as rl

MAX_ASTEROIDS = 100

@dataclass
class Entity:
    """
    Container class for anything that you want to draw on the screen.
    It doesn't have good cache locality, but leaves us flexible to move to a better system.
   sprite_path: location for the entity sprite.
   pos: position of the entity.
   vel: velocity of the entity.
   scale: scale of the entity's sprite.
    """
    def __init__(
        self,
        sprite_path: str,
        pos: tuple[float, float],
        vel: tuple[float, float],
        scale: float,
    ):
        self.position: rl.Vector2 = rl.Vector2(
            pos[0], pos[1]
        )  # [x, y] position of the entity
        self.velocity: rl.Vector2 = rl.Vector2(
            vel[0], vel[1]
        )  # [x, y] velocity of the entity
        self.sprite: rl.Texture = rl.load_texture(sprite_path)
        self.scale: float = scale  # scale of the entity
        self.rotation: float = 0.0  # rotation of the entity
        self.dead: bool = False # draw the entity?
        # These are useful if you want to add animations later.
        self.frame_timer: float = 0.0  # timer for the current frame
        self.current_frame: float = 0  # current frame of the animation


def main():
    # Raylib initialization
    rl.init_window(1280, 720, "Asteroids")
    # rl.set_target_fps(60)
    random.seed()

    alive_count = MAX_ASTEROIDS
    dead_count = 0
    thrust_power = 300
    # Initialize entities list
    entities: list[Entity] = []

    # Initialize player (should remain at head of list)
    player = Entity(
        "images/spaceship.png",
        (rl.get_screen_width() / 2, rl.get_screen_height() / 2),
        (0, 0),
        1.0,
    )
    entities.append(player)

    # Initialize asteroids
    for i in range(1, MAX_ASTEROIDS):
        asteroid = Entity(
            "images/asteroid.png",
            (
                random.randrange(0, rl.get_screen_width()),
                random.randrange(0, rl.get_screen_height()),
            ),
            (random.randrange(-100, 100), random.randrange(-100, 100)),
            0.25,
        )
        entities.append(asteroid)


    # Main game loop
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        frame_time = rl.get_frame_time()

        # Handle input
        if rl.is_key_down(rl.KeyboardKey.KEY_A):  # rotate left
            player.rotation -= 200 * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_D):  # rotate right
            player.rotation += 200 * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_W):  # move forward
            # Convert rotation to radians and calculate thrust direction
            angle_rad = math.radians(player.rotation)
            # Calculate thrust vector based on rotation
            thrust_x = math.cos(angle_rad) * thrust_power
            thrust_y = math.sin(angle_rad) * thrust_power
            # Apply thrust to velocity
            player.velocity.x += thrust_x * frame_time
            player.velocity.y += thrust_y * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_SPACE):  # attack
            pass

        # Apply friction to player
        friction = 0.98
        player.velocity.x *= friction
        player.velocity.y *= friction

        # Update positions
        for e in entities:
            e.position.x += e.velocity.x * frame_time
            e.position.y += e.velocity.y * frame_time

        # Wrap player around screen boundaries
        screen_width = rl.get_screen_width()
        screen_height = rl.get_screen_height()

        if player.position.x < 0:
            player.position.x = screen_width
        elif player.position.x > screen_width:
            player.position.x = 0

        if player.position.y < 0:
            player.position.y = screen_height
        elif player.position.y > screen_height:
            player.position.y = 0

        for asteroid in entities[1:]:
            if not asteroid.dead:
                if asteroid.position.x < 0:
                    asteroid.dead = True
                    alive_count -= 1
                    dead_count += 1
                elif asteroid.position.x > screen_width:
                    alive_count -= 1
                    dead_count += 1
                    asteroid.dead = True
                if asteroid.position.y < 0:
                    asteroid.dead = True
                    alive_count -= 1
                    dead_count += 1
                elif asteroid.position.y > screen_height:
                    alive_count -= 1
                    dead_count += 1
                    asteroid.dead = True

        # Update animation timer
        player.frame_timer += frame_time

        if player.frame_timer > 0.06:
            player.current_frame += 1
            player.frame_timer = 0

        # Render all entities
        for entity in entities:
            if entity.dead:
               continue
            # Calculate center point for rotation
            origin = rl.Vector2(entity.sprite.width / 2, entity.sprite.height / 2)

            rl.draw_texture_pro(
                entity.sprite,
                rl.Rectangle(0, 0, entity.sprite.width, entity.sprite.height),  # source rectangle
                rl.Rectangle(
                    entity.position.x + origin.x,
                    entity.position.y + origin.y,
                    entity.sprite.width * entity.scale,
                    entity.sprite.height * entity.scale
                ),  # destination rectangle
                origin,  # rotation origin (center of sprite)
                entity.rotation,
                rl.WHITE,
            )

        # Draw FPS counter
        rl.draw_fps(10, 10)
        rl.draw_text("Alive: {}".format(alive_count), 10,30, 20, rl.WHITE)
        rl.draw_text("Dead: {}".format(dead_count), 10,60, 20, rl.WHITE)
        rl.end_drawing()

    # Cleanup
    rl.close_window()


if __name__ == "__main__":
    main()
