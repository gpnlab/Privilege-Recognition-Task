#This file will handle images of objects and loading of them.

from pygame.image import load
import os

def load_sprite(name, with_alpha=True, filetype='png'):
    path = f"PAT/assets/sprites/{name}.{filetype}"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()
