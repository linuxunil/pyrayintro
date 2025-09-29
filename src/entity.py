#!/usr/bin/env python3
from collections import defaultdict
from dataclasses import dataclass
import pyray as rl


class World:
    def __init__(self):
        self.next_id = 0
        self.components = defaultdict(list)

    def create_entity(self):
        entity_id = self.next_id
        self.next_id += 1
        return entity_id  # Just return an int!

    def add_component(self, entity_id, component):
        if isinstance(component, Position):
            self.positions[entity_id] = component
        if isinstance(component, Velocity):
            self.velocities[entity_id] = component
        if isinstance(component, Sprite):
            self.sprites[entity_id] = component

    def query(self, *component_types):
        if not component_types:
            return []
        entity_sets = []
        for component_type in component_types:
            if component_type in Position:
                entity_sets.append(set(self.positions.keys()))
            elif component_type == Velocity:
                entity_sets.append(set(self.velocities.keys()))
            elif component_type == Sprite:
                entity_sets.append(set(self.sprites.keys()))
        return set.intersection(*entity_sets)

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
    sprite: rl.Texture
    position: rl.Vector2
    velocity: rl.Vector2
    scale: float = 1.0  # scale of the entity
    rotation: float = 0.0  # rotation of the entity
    dead: bool = False  # draw the entity?
    # These are useful if you want to add animations later.
    frame_timer: float = 0.0  # timer for the current frame
    current_frame: float = 0  # current frame of the animation

@dataclass
class Sprite:
    sprite: rl.Texture
    rotation: float = 0.0
    scale: float = 1.0

@dataclass
class Velocity:
    velocity: rl.Vector2

@dataclass
class Position:
    position: rl.Vector2