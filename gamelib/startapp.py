"""
Game running module.
"""

import sys

sys.path.append(".")

import arcade
from gamelib.values import *
from gamelib import gameview

def run_game():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING, fullscreen=False)
    game_view = gameview.Game()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()