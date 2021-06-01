"""
Main game class module. Initialize the game and handle all the actions.
"""

from gamelib.constants import *
import sys

import arcade
from pyglet.window.key import N

sys.path.append(".")


class Game(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING)

        self.character_cont_list = None
        self.block_list = None

        self.maklowicz = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.character_cont_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList(use_spatial_hash=True)

        self.maklowicz = arcade.Sprite(MAKLOWICZ_IDLE, CHARACTER_SCALING)
        self.maklowicz.center_x = 2*TL
        self.maklowicz.center_y = 5*TL
        self.character_cont_list.append(self.maklowicz)

        test_lvl_map = arcade.tilemap.read_tmx(TEST_MAP)
        self.block_list = arcade.tilemap.process_layer(map_object=test_lvl_map,
                                                      layer_name=TEST_BLOCK_LAYER,
                                                      scaling=BLOCK_SCALING,
                                                      use_spatial_hash=True)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.maklowicz,
                                                             self.block_list,
                                                             GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.character_cont_list.draw()
        self.block_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
