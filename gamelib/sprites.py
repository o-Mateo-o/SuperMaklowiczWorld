"""
Sprite classes of characters and special objects.
"""

import sys

import arcade
from arcade.key import RIGHT, T

from gamelib.constants import *

sys.path.append(".")


class Maklowicz(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(scale=CHARACTER_SCALING)
        self.facing = RIGHT_F
        self.texture = IMG_MAKLOWICZ_IDLE[self.facing]
        self.center_x = center_x
        self.center_y = center_y
        self.current_texture = 0

    def update_animation(self, delta_time: float):
        if all([engine.can_jump() for engine in self.physics_engines]):
            self.texture = IMG_MAKLOWICZ_IDLE[self.facing]
        else:
            self.texture = IMG_MAKLOWICZ_JUMP[self.facing]

        if self.change_x != 0 and self.change_y == 0:
            
            self.current_texture += 1
            if self.current_texture > 8:
                self.current_texture = 0
            self.texture = IMG_MAKLOWICZ_RUN[self.current_texture>3][self.facing]

            
        return super().update_animation(delta_time=delta_time)
    
    def process_keychange(self, keys_pressed):
        if keys_pressed['UP'] and all([engine.can_jump(y_distance = 10) for engine in self.physics_engines]):
            self.change_y = MAKLOWICZ_JUMP_SPEED
        if keys_pressed['RIGHT']:
            self.facing = RIGHT_F
            self.change_x = MAKLOWICZ_SPEED
        elif keys_pressed['LEFT']:
            self.change_x = -MAKLOWICZ_SPEED
            self.facing = LEFT_F
        elif not keys_pressed['RIGHT'] and not keys_pressed['LEFT']:
            self.change_x = 0

        
