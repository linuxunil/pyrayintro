#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["raylib"]
# ///

import random
import math
from dataclasses import dataclass
from enum import Enum

import pyray as rl

MAX_ASTEROIDS = 10

class Screen(Enum):
    Initial = 0
    Running = 1
    End = 2

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

class Player(Entity):
    def fire(self):
        pass

def collision_check(pos1, radius1, pos2, radius2):
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    distance = math.sqrt(dx * dx + dy * dy)
    return distance < (radius1 + radius2)

def handle_input(entity, thrust_power, frame_time):
    # Handle input
    if rl.is_key_down(rl.KeyboardKey.KEY_A):  # rotate left
        entity.rotation -= 200 * frame_time
    if rl.is_key_down(rl.KeyboardKey.KEY_D):  # rotate right
        entity.rotation += 200 * frame_time
    if rl.is_key_down(rl.KeyboardKey.KEY_W):  # move forward
        # Convert rotation to radians and calculate thrust direction
        angle_rad = math.radians(entity.rotation)
        # Calculate thrust vector based on rotation
        thrust_x = math.cos(angle_rad) * thrust_power
        thrust_y = math.sin(angle_rad) * thrust_power
        # Apply thrust to velocity
        entity.velocity.x += thrust_x * frame_time
        entity.velocity.y += thrust_y * frame_time
    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE):  # attack
        entity.fire()

def update_game(entities: list[Entity], frame_time: float):
    handle_input(entities[0], 300, frame_time)
    # Apply friction to player
    friction = 0.98
    entities[0].velocity.x *= friction
    entities[0].velocity.y *= friction

    # Update positions
    for e in entities:
        e.position.x += e.velocity.x * frame_time
        e.position.y += e.velocity.y * frame_time

    # Wrap player around screen boundaries
    screen_width = rl.get_screen_width()
    screen_height = rl.get_screen_height()

    if entities[0].position.x < 0:
        entities[0].position.x = screen_width
    elif entities[0].position.x > screen_width:
        entities[0].position.x = 0

    if entities[0].position.y < 0:
        entities[0].position.y = screen_height
    elif entities[0].position.y > screen_height:
        entities[0].position.y = 0

    for asteroid in entities[1:]:
        if not asteroid.dead:
            if asteroid.position.x < 0:
                asteroid.dead = True
            elif asteroid.position.x > screen_width:
                asteroid.dead = True
            if asteroid.position.y < 0:
                asteroid.dead = True
            elif asteroid.position.y > screen_height:
                asteroid.dead = True
            if collision_check(entities[0].position, entities[0].sprite.width/2, asteroid.position, asteroid.sprite.width/2):
                entities[0].dead = True

def draw_screen(entities: list[Entity], frame_time: float):
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
def main():
    # Raylib initialization
    rl.init_window(1280, 720, "Asteroids")
    # rl.set_target_fps(60)
    random.seed()
    # Initialize entities list
    entities: list[Entity] = []
    # Initialize player (should remain at head of list)
    player = Player(
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
        update_game(entities, frame_time)
        draw_screen(entities, frame_time)
        # Draw FPS counter
        rl.draw_fps(10, 10)
        rl.end_drawing()

    # Cleanup
    rl.close_window()


if __name__ == "__main__":
    main()
