"""
Game running module.
"""

import sys
from pyglet.media.exceptions import MediaDecodeException

import arcade

sys.path.append(".")

decode_error_counter = 1
while decode_error_counter < 5:
    try:
        from gamelib.constants import *
        break
    except MediaDecodeException:
        if decode_error_counter == 1:
            print("Windows decoding error. Trying to import assets again.")
        if decode_error_counter < 4:
            print(f"... {decode_error_counter}/3")
        else:
            raise Exception("Windows decode error cannot be fixed. Please restart the app.")
        decode_error_counter += 1       

from gamelib import gamewindow
from gamelib import menuview



def run_game():
    window = gamewindow.GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING)
    menu_view = menuview.MainMenuView()
    window.show_view(menu_view)
    arcade.run()