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
    def __init__(self, parent_view, center_x=2*TL, center_y=6*TL):
        super().__init__(scale=CHARACTER_SCALING)
        self.view = parent_view
        # figure properities
        self.facing = RIGHT_F
        self.sound_player_register = self.view.window.sound_player_register
        self.texture = image_maklowicz['idle'][self.facing]
        self.center_x = center_x
        self.center_y = center_y
        self.current_texture = 0
        self.animation_ratio = 5

        # sound players
        self.pepper_sound_player = media.Player()
        self.run_sound_player = media.Player()
        self.dill_sound_player = media.Player()
        self.pain_sound_player = media.Player()

        # characteer status
        self.run_state = False
        self.previous_q_run_state = False
        self.in_air = False
        self.previous_q_in_air = True
        self.jump_state = False
        self.item_collected = False
        self.hurt = False
        self.immunity = False
        self.immunity_counter = 0
        self.dead = False

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

    def hurt_action(self, lives):
        if not self.immunity:
            self.hurt = True
            self.center_x = self.center_x - MAKLOWICZ_KICKBACK
            self.change_y = MAKLOWICZ_JUMP_SPEED
            self.immunity = True
            return lives - 1
        else:
            return lives

    def update_texture(self):
        # textures for proper movement states - running animated
        if self.dead:
            self.texture = image_maklowicz['dead'][self.facing]
        elif self.in_air:
            self.texture = image_maklowicz['jump'][self.facing]
        elif self.run_state and not self.in_air:
            self.current_texture += 1
            if self.current_texture > self.animation_ratio * 2 - 1:
                self.current_texture = 0
            texture_key = 'run1' if self.current_texture > self.animation_ratio else 'run2'
            self.texture = image_maklowicz[texture_key][self.facing]
        else:
            self.texture = image_maklowicz['idle'][self.facing]

    def update_sound(self, jump_action):
        
        # laugh in the moment of dill picking
        if self.item_collected:
            self.dill_sound_player = auxfunctions.play_sound(
                sounds_roberto['hihihi'], self.dill_sound_player,
                volume=self.view.window.standard_sound_volume)
            self.item_collected = False

        if self.hurt:
            self.pain_sound_player = auxfunctions.play_sound(
                sounds_roberto['oaa'], self.pain_sound_player,
                volume=self.view.window.pain_volume)
            self.hurt = False

        # start looped run sound when he lands or begins movement; stop when he stops or jumps
        if (not self.previous_q_run_state and self.run_state and not self.in_air)\
                or (self.run_state and not self.in_air and self.previous_q_in_air):
            self.run_sound_player = auxfunctions.play_sound(
                sound_environ['running'], self.run_sound_player, volume=self.view.window.step_volume, loop=True)
        elif self.previous_q_run_state and not self.run_state or self.in_air:
            arcade.stop_sound(self.run_sound_player)
        elif not self.run_state:
            arcade.stop_sound(self.run_sound_player)

        # jump sounds in the moment of rebounding
        if jump_action:
            jump_sound = random.choice(list(sound_pepper.values()))
            self.pepper_sound_player = auxfunctions.play_sound(
                jump_sound, self.pepper_sound_player, 
                volume=self.view.window.standard_sound_volume)

        
        self.view.window.sound_player_register['pepper'] = self.pepper_sound_player
        self.view.window.sound_player_register['run'] = self.run_sound_player
        self.view.window.sound_player_register['dill'] = self.dill_sound_player
        self.view.window.sound_player_register['pain'] = self.pain_sound_player

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

        # immunity update
        if self.immunity:
            self.immunity_counter += 1
        if self.immunity_counter > MAKLOWICZ_IMMUNITY_TIME:
            self.immunity = False

        # call visual and audio update methods
        self.update_texture()
        self.update_sound(jump_action)

        # update previous quant variables to aquire differences
        self.previous_q_run_state = self.run_state
        self.previous_q_in_air = self.in_air


class PepperEnemy(arcade.Sprite):
    def __init__(self, parent_view):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view
        self.facing = RIGHT_F
        self.current_texture = 0
        self.killed = False
        self.killed_counter = 0
        self.animation_ratio = 6
        self.transform_to_item = False
        self.change_x = -PEPPER_SPEED

    def update_texture(self):
        # textures for proper movement states
        if not self.killed:
            self.current_texture += 1
            if self.current_texture > 4 * self.animation_ratio - 1:
                self.current_texture = 0
            if self.current_texture < self.animation_ratio:
                texture_key = 'live1'
            elif self.current_texture < 2 * self.animation_ratio:
                texture_key = 'live2'
            elif self.current_texture < 3 * self.animation_ratio:
                texture_key = 'live3'
            else:
                texture_key = 'live2'
            self.texture = image_pepper_enemy[texture_key][self.facing]
        else:
            self.texture = image_pepper_enemy['killed'][0]

    def update(self):
        if self.change_x < 0:
            self.facing = RIGHT_F
        else:
            self.facing = LEFT_F
        if self.current_texture == 0:
            self.change_y = PEPPER_JUMP_SPEED
        self.update_texture()
        if self.killed:
            self.killed_counter += 1
        if self.killed_counter == PEPPER_AGONY_TIME:
            self.transform_to_item = True
        if self.killed_counter > PEPPER_AGONY_TIME:
            for sprite_list in self.sprite_lists:
                sprite_list.remove(self)


class Pot(arcade.Sprite):
    def __init__(self, parent_view):
        super().__init__(scale=MAP_SCALING)
        # pot is picked after a collision and desactivetad after picking action
        self.view = parent_view
        self.picked = False
        self.active = True

    def pick_action(self):
        if not self.picked:
            self.change_y = POT_ACTION_SPEED
            self.init_center_y = self.center_y+1
            self.picked = True
            self.texture = image_pot['picked']
            pot_player = sound_environ['pot'].play(volume=self.view.window.standard_sound_volume)
            self.view.window.sound_player_register['pain'] = pot_player
        elif self.center_y >= self.init_center_y + POT_ACTION_HEIGHT:
            self.change_y = -POT_ACTION_SPEED

        elif self.center_y < self.init_center_y:
            self.change_y = 0
            self.center_y = self.init_center_y
            self.active = False


class PepperItem(arcade.Sprite):
    def __init__(self, parent_view, parent: arcade.Sprite = None):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view
        self.texture = image_collectable['pepper']
        if parent != None:
            self.position = parent.position


class Dill(arcade.Sprite):
    def __init__(self, parent_view, parent: arcade.Sprite = None):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view
        self.texture = image_collectable['dill']
        if parent != None:
            self.position = (parent.center_x, parent.center_y + TL)


class Knives(arcade.Sprite):
    def __init__(self, parent_view):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view

    def initial_move(self):
        self.center_y = self.center_y + KNIVES_DISLOCATION


class Fork(arcade.Sprite):
    def __init__(self, parent_view):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view
        self.init_height = self.center_y
        self.change_y = 5

    def adjust_hitbox(self):
        self.set_hit_box([[0.7*point[0], point[1]]
                         for point in self.get_hit_box()])

    def update(self):
        if self.center_y > self.init_height + 100:
            self.change_y = -2
        elif self.center_y < self.init_height:
            self.change_y = 2
        return super().update()


class MovingBlockSimple(arcade.Sprite):
    def __init__(self, parent_view):
        super().__init__(scale=MAP_SCALING)
        self.view = parent_view
    def start_movement(self):
        self.change_x = -MOVING_BLOCK_SPEED
