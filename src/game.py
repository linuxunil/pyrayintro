from src.context import Context
from src.entity import *
from src.system import *
import pyray as rl
import random

def start_game (ctx =Context([]), width=1280, height=720, fps=60):
    """Initialize and run the Asteroids game.

    Args:
        ctx: Game context containing entities and configuration (default: empty Context)
        width: Window width in pixels (default: 1280)
        height: Window height in pixels (default: 720)
        fps: Target frames per second (default: 60)
    """
    # Raylib initialization
    rl.init_window(width, height, "Asteroids")
    rl.set_target_fps(fps)
    random.seed()
    # Initialize player (should remain at head of list)
    world = World()
    world.create_entity()
    player = Entity(
        rl.load_texture("images/spaceship.png"),
        rl.Vector2(rl.get_screen_width() / 2, rl.get_screen_height() / 2),
        rl.Vector2(0, 0),
    )
    ctx.entities.append(player)
    # Initialize asteroids
    for i in range(1, ctx.MAX_ASTEROIDS):
        asteroid = Entity(
            rl.load_texture("images/asteroid.png"),
            rl.Vector2(
                random.randrange(0, rl.get_screen_width()),
                random.randrange(0, rl.get_screen_height()),
            ),
            rl.Vector2(random.randrange(-100, 100), random.randrange(-100, 100)),
        )
        ctx.entities.append(asteroid)

    # Main game loop
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        ctx.frame_time = rl.get_frame_time()
        Update.tick(ctx)
        Draw.entities(ctx.entities)
        # Draw FPS counter
        rl.draw_fps(10, 10)
        rl.end_drawing()

    # Cleanup
    rl.close_window()