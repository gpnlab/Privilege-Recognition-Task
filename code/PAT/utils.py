#This file will handle images of objects and loading of them.

#IMPORTS
import random
from pygame.image import load
from pygame.math import Vector2
import os

def load_sprite(name, with_alpha=True):
    path = f"PAT/assets/sprites/{name}"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )
