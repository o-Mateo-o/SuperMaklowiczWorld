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

        self.right_pressed = False
        self.left_pressed = False
        self.up_pressed = False

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



    def process_keychange(self):
        if self.up_pressed and self.physics_engine.can_jump():
            self.maklowicz.change_y = MAKLOWICZ_JUMP_SPEED
        if self.right_pressed:
            self.maklowicz.change_x = MAKLOWICZ_SPEED
        elif self.left_pressed:
            self.maklowicz.change_x = -MAKLOWICZ_SPEED
        elif not self.right_pressed and not self.left_pressed:
            self.maklowicz.change_x = 0
        
            
    def on_key_press(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.up_pressed = True
        if key in [arcade.key.A, arcade.key.LEFT]:
            self.left_pressed = True
        if key in [arcade.key.D, arcade.key.RIGHT]:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.up_pressed = False
        if key in [arcade.key.A, arcade.key.LEFT]:
            self.left_pressed = False
        if key in [arcade.key.D, arcade.key.RIGHT]:
            self.right_pressed = False

        self.process_keychange()
        

    def on_draw(self):
        arcade.start_render()

        self.character_cont_list.draw()
        self.block_list.draw()

    def on_update(self, delta_time):

        self.maklowicz.update_animation(delta_time)
        self.physics_engine.update()
