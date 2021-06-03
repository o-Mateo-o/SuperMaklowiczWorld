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
        # figure properities
        self.facing = RIGHT_F
        self.texture = image_maklowicz['idle'][self.facing]
        self.center_x = center_x
        self.center_y = center_y
        self.current_texture = 0

        #sound players
        self.pepper_sound_player = media.Player()
        self.run_sound_player = media.Player()
        self.dill_sound_player = media.Player() 

        # characteer status
        self.run_state = False
        self.previous_q_run_state = False
        self.jump_state = False
        self.previous_q_jump_state = False
        self.dill_collected = False

    def figure_mirror(self, facing):
        if self.facing == facing:
            ratio = 1
        else:
            ratio = -1
        self.set_hit_box([[ratio*point[0], point[1]]
                         for point in self.get_hit_box()])
        self.facing = facing

    def process_keychange(self, keys_pressed):
        if keys_pressed['UP'] and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)
                                       for engine in self.physics_engines]):
            self.change_y = MAKLOWICZ_JUMP_SPEED
            jump_sound = random.choice(list(sound_pepper.values()))
            self.pepper_sound_player = auxfunctions.play_sound(
                jump_sound, self.pepper_sound_player)
        if keys_pressed['RIGHT']:
            self.figure_mirror(RIGHT_F)
            self.change_x = MAKLOWICZ_SPEED
        elif keys_pressed['LEFT']:
            self.change_x = -MAKLOWICZ_SPEED
            self.figure_mirror(LEFT_F)
        elif not keys_pressed['RIGHT'] and not keys_pressed['LEFT']:
            self.change_x = 0

    def update_texture(self):
        if self.jump_state:
            self.texture = image_maklowicz['jump'][self.facing]
        elif self.run_state and not self.jump_state:
            self.current_texture += 1
            if self.current_texture > 9:
                self.current_texture = 0
            texture_key = 'run1' if self.current_texture > 4 else 'run2'
            self.texture = image_maklowicz[texture_key][self.facing]
        else:
            self.texture = image_maklowicz['idle'][self.facing]

    def update_sound(self):
        # if self.run_state and not self.jump_state:
        #     self.run_sound_player = auxfunctions.play_sound_looped(
        #         sound_environ['running'], self.run_sound_player)
        if self.dill_collected:
            self.dill_sound_player = auxfunctions.play_sound(
                sounds_roberto['hihihi'], self.dill_sound_player)
            self.dill_collected = False
    
    def update(self):
        if all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)
                for engine in self.physics_engines]):
            self.jump_state = False     
        else:
            self.jump_state = True
        if self.change_x == 0:
            self.run_state = False
        else:
            self.run_state = True

        if (not self.previous_q_run_state and self.run_state and not self.jump_state)\
            or (self.run_state and not self.jump_state and self.previous_q_jump_state):
            self.run_sound_player = auxfunctions.play_sound(
                sound_environ['running'], self.run_sound_player, volume=0.5, loop=True)
        elif self.previous_q_run_state and not self.run_state or self.jump_state:
            arcade.stop_sound(self.run_sound_player)

        self.previous_q_run_state = self.run_state
        self.previous_q_jump_state = self.jump_state

        self.update_texture() 
        self.update_sound()


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
    def __init__(self, parent: arcade.Sprite = None):
        super().__init__(scale=MAP_SCALING)
        self.texture = image_collectable['dill']
        if parent != None:
            self.position = (parent.center_x, parent.center_y + TL)
