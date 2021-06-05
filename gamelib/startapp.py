"""
Game running module.
"""

import sys
from pyglet.media.exceptions import MediaDecodeException

sys.path.append(".")

import arcade

decode_error_counter = 1
while decode_error_counter < 5:
    try:
        from gamelib.values import *
        break
    except MediaDecodeException:
        if decode_error_counter == 1:
            print("Windows decoding error. Trying to import assets again.")
        if decode_error_counter < 4:
            print(f"... {decode_error_counter}/3")
        else:
            raise Exception("Windows decode error cannot be fixed. Please restart the app.")
        decode_error_counter += 1       

from gamelib import gameview


def run_game():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING, fullscreen=False)
    game_view = gameview.GameLevel()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()