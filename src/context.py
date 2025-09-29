#!/usr/bin/env python3


from dataclasses import dataclass
from src.entity import Entity


@dataclass
class Context:
    """Context stores shared game objects"""
    entities: list[Entity]
    frame_time: float = 0
    friction: float = 0.98
    thrust_power: int = 300
    MAX_ASTEROIDS: int = 100
