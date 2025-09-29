# 🚀 Asteroids Game

A classic Asteroids-style space game built with Python and [Raylib](https://www.raylib.com/) using the [pyray](https://github.com/electronstudio/raylib-python-cffi) bindings.

## ✨ Features

- **Spaceship Control**: Navigate your spaceship using WASD controls
- **Physics Simulation**: Realistic momentum and friction mechanics
- **Asteroid Field**: Dynamic asteroid spawning and collision boundaries
- **Screen Wrapping**: Player ship wraps around screen edges for continuous gameplay
- **Real-time Statistics**: Live tracking of alive/dead asteroids
- **Smooth Animation**: Frame-based movement and rotation system

## Todo
- [ ] Collisions
- [ ] Difficulty Scaling
- [ ] Game Screens
- [ ] Shoot asteroids
- 
## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` | Thrust forward |
| `A` | Rotate left |
| `D` | Rotate right |
| `Space` | Attack (coming soon) |

## 🚦 Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation & Running

This project uses uv's inline script dependencies. Simply run:

```bash
python main.py
```

Or with uv directly:

```bash
uv run main.py
```

The game will automatically install the required `raylib` dependency and launch.

## 🎯 Gameplay

- Control your spaceship in a field of moving asteroids
- Use thrust to navigate while managing momentum and friction
- Asteroids disappear when they leave the screen boundaries
- Watch the live counter to track remaining asteroids

## 🖼️ Assets

The game includes custom sprite assets:
- `spaceship.png` - Player ship sprite
- `asteroid.png` - Asteroid sprite
- `laser.png` - Laser projectile (future feature)

## 🛠️ Technical Details

- **Engine**: Raylib via pyray Python bindings
- **Architecture**: Entity-based system with flexible sprite rendering
- **Performance**: Optimized for 60 FPS gameplay
- **Resolution**: 1280x720 windowed mode

## 📝 Development

The project uses a simple Entity system where all game objects are a base `Entity` class containing:
- Position and velocity vectors
- Sprite rendering with rotation and scaling
- Animation frame timing system
- Lifecycle management (alive/dead states)

## 🔮 Future Enhancements

- Laser shooting mechanics
- Asteroid collision detection
- Score system and high scores
- Sound effects and background music
- Particle effects for explosions
- Multiple asteroid sizes
- Power-ups and upgrades

## 📄 License
`Code by Matthew Leonberger Assets by Jakobie Brown`

This project is open source and available under standard licensing terms.
