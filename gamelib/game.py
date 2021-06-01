"""
Main game class module. Initialize the game and handle all the actions.
"""

from arcade.key import T
from gamelib.constants import *
from gamelib import sprites
import sys

import arcade
from pyglet.window.key import N

sys.path.append(".")


class Game(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING)

        #keys handled and projection properities
        self.keys_pressed = {'UP': False, 'LEFT': False, 'RIGHT': False}
        self.view_bottom = 0
        self.view_left = 0

        # sprites
        self.character_cont_list = None
        self.block_list = None
        
        self.maklowicz = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        self.character_cont_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList(use_spatial_hash=True)

        self.maklowicz = sprites.Maklowicz(2*TL, 6*TL)
        self.character_cont_list.append(self.maklowicz)

        test_lvl_map = arcade.tilemap.read_tmx(TEST_MAP)
        self.block_list = arcade.tilemap.process_layer(map_object=test_lvl_map,
                                                      layer_name=TEST_BLOCK_LAYER,
                                                      scaling=BLOCK_SCALING,
                                                      use_spatial_hash=True)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.maklowicz,
                                                             self.block_list,
                                                             GRAVITY)
        self.maklowicz.physics_engines.append(self.physics_engine)


      
            
    def on_key_press(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.keys_pressed['UP'] = True
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.keys_pressed['LEFT'] = True
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.keys_pressed['RIGHT'] = True

        self.maklowicz.process_keychange(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.keys_pressed['UP']= False
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.keys_pressed['LEFT'] = False
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.keys_pressed['RIGHT'] = False

        self.maklowicz.process_keychange(self.keys_pressed)
        

    def on_draw(self):
        arcade.start_render()

        self.character_cont_list.draw()
        self.block_list.draw()

    def on_update(self, delta_time):
        
        self.maklowicz.update_animation(delta_time)
        self.physics_engine.update()

        # SCREEN SCROLLING
        
        changed_flag = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN - 5
        right_boundary = self.view_left + WINDOW_WIDTH - RIGHT_VIEWPORT_MARGIN + 5
        top_boundary = self.view_bottom + WINDOW_HEIGHT - TOP_VIEWPORT_MARGIN
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN

        if self.maklowicz.center_x < left_boundary:
            self.view_left -= left_boundary - self.maklowicz.center_x
            changed_flag = True
        if self.maklowicz.center_x > right_boundary:
            self.view_left += self.maklowicz.center_x - right_boundary
            changed_flag = True
        if self.maklowicz.top > top_boundary:
            self.view_bottom += self.maklowicz.top - top_boundary
            changed_flag= True
        if self.maklowicz.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.maklowicz.bottom
            changed_flag = True

        if changed_flag:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left, WINDOW_WIDTH + self.view_left,
                                self.view_bottom, WINDOW_HEIGHT + self.view_bottom)
        