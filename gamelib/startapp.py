"""
Game running module.
"""

from pyglet.media.exceptions import MediaDecodeException

import arcade, sys

sys.path.append(".")

# in case of eg windows decoder error (sometimes happens)
# - try to load the game three times
# if fails, throw an error
decode_error_counter = 1
while decode_error_counter < 5:
    try:
        from gamelib.constants import *
        break
    except MediaDecodeException:
        if decode_error_counter == 1:
            print("OS decoding error. Trying to import assets again.")
        if decode_error_counter < 4:
            print(f"... {decode_error_counter}/3")
        else:
            raise Exception("OS decoding error cannot be fixed. Please restart the app.")
        decode_error_counter += 1       

from gamelib import gamewindow, menuviews


def run_game():
    """
    Run the game - create a window and show a menu.
    """
    window = gamewindow.GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEADING)
    menu_view = menuviews.MainMenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()