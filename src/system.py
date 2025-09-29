from src.entity import Entity
import pyray as rl
from src.context import Context
import math

class Collisions:
    @staticmethod
    def check(entity_a, entity_b: Entity) -> bool:
        """Check collision between two axis-aligned rectangles"""
        return (
            entity_a.position.x < entity_b.position.x + entity_b.sprite.width
            and entity_a.position.x + entity_a.sprite.width > entity_b.position.x
            and entity_a.position.y < entity_b.position.y + entity_b.sprite.height
            and entity_a.position.y + entity_a.sprite.height > entity_b.position.y
    )


class Input:
    @staticmethod
    def keyboard(entity: Entity, ctx: Context):
        # Handle input
        if rl.is_key_down(rl.KeyboardKey.KEY_A):  # rotate left
            entity.rotation -= 200 * ctx.frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_D):  # rotate right
            entity.rotation += 200 * ctx.frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_W):  # move forward
            # Convert rotation to radians and calculate thrust direction
            angle_rad = math.radians(entity.rotation)
            # Calculate thrust vector based on rotation
            thrust_x = math.cos(angle_rad) * ctx.thrust_power
            thrust_y = math.sin(angle_rad) * ctx.thrust_power
            # Apply thrust to velocity
            entity.velocity.x += thrust_x * ctx.frame_time
            entity.velocity.y += thrust_y * ctx.frame_time


class Screen:
    @staticmethod
    def check_bounds(entity: Entity) -> tuple[bool, bool]:
        res = [False, False]
        if entity.position.x < 0.0 or entity.position.x > rl.get_screen_width():
            res[0] = True
        if entity.position.y < 0 or entity.position.y > rl.get_screen_height():
            res[1] = True
        return tuple(res)

class Update:
    @staticmethod
    def tick(ctx: Context):
        Input.keyboard(ctx.entities[0], ctx)
        # Apply friction to player
        ctx.entities[0].velocity.x *= ctx.friction
        ctx.entities[0].velocity.y *= ctx.friction

        # Check player bounds
        x, y = Screen.check_bounds(ctx.entities[0])
        if x:
            ctx.entities[0].velocity.x = 0
        if y:
            ctx.entities[0].velocity.y = 0

        for asteroid in ctx.entities[1:]:
            if not asteroid.dead:
                x, y = Screen.check_bounds(asteroid)
                if x or y:
                    asteroid.dead = True
                if Collisions.check(ctx.entities[0], asteroid):
                    ctx.entities[0].dead = True
            # Update positions
            for e in ctx.entities:
                e.position.x += e.velocity.x * ctx.frame_time
                e.position.y += e.velocity.y * ctx.frame_time

class Draw:
    @staticmethod
    def entities(entities: list[Entity]):
        # Render all entities
        for entity in entities:
            if entity.dead:
                continue
            # Calculate center point for rotation
            origin = rl.Vector2(entity.sprite.width / 2, entity.sprite.height / 2)

            rl.draw_texture_pro(
                entity.sprite,
                rl.Rectangle(
                    0, 0, entity.sprite.width, entity.sprite.height
                ),  # source rectangle
                rl.Rectangle(
                    entity.position.x + origin.x,
                    entity.position.y + origin.y,
                    entity.sprite.width * entity.scale,
                    entity.sprite.height * entity.scale,
                ),  # destination rectangle
                origin,  # rotation origin (center of sprite)
                entity.rotation,
                rl.WHITE,
            )
