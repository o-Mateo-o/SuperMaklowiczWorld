"""
Sprite classes of characters and special objects.
"""

import sys

import arcade

from gamelib.constants import *

sys.path.append(".")


class Maklowicz(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(filename=IMG_MAKLOWICZ_IDLE, scale=CHARACTER_SCALING)
        self.center_x = center_x
        self.center_y = center_y

    def update_animation(self, delta_time: float):
        if any([engine.can_jump() for engine in self.physics_engines]):
            self.texture = arcade.load_texture(IMG_MAKLOWICZ_IDLE)
        else:
            self.texture =arcade.load_texture(IMG_MAKLOWICZ_JUMP)
        return super().update_animation(delta_time=delta_time)

        
