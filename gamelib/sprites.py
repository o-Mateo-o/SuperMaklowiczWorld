"""
Sprite classes of characters and special objects.
"""

import sys

import arcade
import random
from pyglet import media
from pytiled_parser.objects import TileMap
from gamelib import auxfunctions
from gamelib.values import *

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
        self.in_air = False
        self.previous_q_in_air = True
        self.jump_state = False
        self.dill_collected = False

    def figure_mirror(self, facing):
        if self.facing == facing:
            ratio = 1
        else:
            ratio = -1
        # character hitbox symmetry and facing variable update
        self.set_hit_box([[ratio*point[0], point[1]]
                         for point in self.get_hit_box()])
        self.facing = facing

    def process_keychange(self, keys_pressed):
        # character actions depending on user controll
        if keys_pressed['jump'] and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)
                                       for engine in self.physics_engines]):
            self.change_y = MAKLOWICZ_JUMP_SPEED
            self.jump_state = True
        if keys_pressed['right']:
            self.figure_mirror(RIGHT_F)
            self.change_x = MAKLOWICZ_SPEED
        elif keys_pressed['left']:
            self.change_x = -MAKLOWICZ_SPEED
            self.figure_mirror(LEFT_F)
        elif not keys_pressed['right'] and not keys_pressed['left']:
            self.change_x = 0

    def update_texture(self):
        # textures for proper movement states - running animated
        if self.in_air:
            self.texture = image_maklowicz['jump'][self.facing]
        elif self.run_state and not self.in_air:
            self.current_texture += 1
            if self.current_texture > 9:
                self.current_texture = 0
            texture_key = 'run1' if self.current_texture > 4 else 'run2'
            self.texture = image_maklowicz[texture_key][self.facing]
        else:
            self.texture = image_maklowicz['idle'][self.facing]

    def update_sound(self, jump_action):
        # laugh in the moment of dill picking
        if self.dill_collected:
            self.dill_sound_player = auxfunctions.play_sound(
                sounds_roberto['hihihi'], self.dill_sound_player)
            self.dill_collected = False

        # start looped run sound when he lands or begins movement; stop when he stops or jumps
        if (not self.previous_q_run_state and self.run_state and not self.in_air)\
            or (self.run_state and not self.in_air and self.previous_q_in_air):
            self.run_sound_player = auxfunctions.play_sound(
                sound_environ['running'], self.run_sound_player, volume=step_volume, loop=True)
        elif self.previous_q_run_state and not self.run_state or self.in_air:
            arcade.stop_sound(self.run_sound_player)

        # jump sounds in the moment of rebounding
        if jump_action:
            jump_sound = random.choice(list(sound_pepper.values()))
            self.pepper_sound_player = auxfunctions.play_sound(
                jump_sound, self.pepper_sound_player)
    
    def update(self):
        # update the info about the movement - running and jumping
        if all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)
                for engine in self.physics_engines]):
            self.in_air = False
        else:
            self.in_air = True
        if self.change_x == 0:
            self.run_state = False
        else:
            self.run_state = True

        jump_action = False
        if not self.previous_q_in_air and self.in_air and self.jump_state:
            jump_action = True
            self.jump_state = False
            
        # call visual and audio update methods
        self.update_texture() 
        self.update_sound(jump_action)       

        # update previous quant variables to aquire differences
        self.previous_q_run_state = self.run_state
        self.previous_q_in_air = self.in_air
        
        


class Pot(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=MAP_SCALING)
        # pot is picked after a collision and desactivetad after picking action
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
