"""
Sprite classes of characters and special objects.
"""

import sys

import arcade
import random
from pyglet import media
from pytiled_parser.objects import TileMap
from gamelib import auxfunctions
from gamelib.constants import *

sys.path.append(".")


class Maklowicz(arcade.Sprite):
    def __init__(self, center_x=2*TL, center_y=6*TL):
        super().__init__(scale=CHARACTER_SCALING)
        self.facing = RIGHT_F
        self.texture = image_maklowicz['idle'][self.facing]
        self.center_x = center_x
        self.center_y = center_y
        self.current_texture = 0
        self.pepper_sound_player = media.Player()

    def figure_mirror(self, facing):
        if self.facing == facing:
            ratio = 1
        else:
            ratio = -1
        self.set_hit_box([[ratio*point[0], point[1]] for point in self.get_hit_box()])
        self.facing = facing

    def update_animation(self, delta_time: float):
        if all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):
            self.texture = image_maklowicz['idle'][self.facing]
        else:
            self.texture = image_maklowicz['jump'][self.facing]

        if self.change_x != 0 and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):

            self.current_texture += 1
            if self.current_texture > 9:
                self.current_texture = 0
            texture_key = 'run1' if self.current_texture > 4 else 'run2'
            self.texture = image_maklowicz[texture_key][self.facing]
        return super().update_animation(delta_time=delta_time)

    def process_keychange(self, keys_pressed):
        if keys_pressed['UP'] and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):
            self.change_y = MAKLOWICZ_JUMP_SPEED
            jump_sound = random.choice(list(sound_pepper.values()))
            self.pepper_sound_player = auxfunctions.play_sound(jump_sound, self.pepper_sound_player)
        if keys_pressed['RIGHT']:
            self.figure_mirror(RIGHT_F)
            self.change_x = MAKLOWICZ_SPEED
        elif keys_pressed['LEFT']:
            self.change_x = -MAKLOWICZ_SPEED
            self.figure_mirror(LEFT_F)
        elif not keys_pressed['RIGHT'] and not keys_pressed['LEFT']:
            self.change_x = 0
    
class Pot(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=MAP_SCALING)
        self.picked = False
        self.active = True
    
    def pick_action(self):
        if not self.picked:
            self.change_y = POT_ACTION_SPEED
            self.init_center_y = self.center_y+1
            self.picked = True
            self.texture = image_pot['picked']
        
        elif self.center_y >= self.init_center_y + POT_ACTION_HEIGHT:
            self.change_y = -POT_ACTION_SPEED

        elif self.center_y < self.init_center_y:
            self.change_y = 0
            self.center_y = self.init_center_y
            self.active = False

class Dill(arcade.Sprite):
    def __init__(self, parent:arcade.Sprite=None):
        super().__init__(scale=MAP_SCALING)
        self.texture = image_collectable['dill']
        if parent != None:
            self.position = (parent.center_x, parent.center_y + TL)
        




    


