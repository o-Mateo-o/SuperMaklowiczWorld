"""
Initial, pause and other additional view classes.
"""

import arcade

import arcade.gui as gui
from arcade.gui import UIManager
from gamelib.constants import *
from gamelib import widgets


class PauseView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        self.c_keys_pressed = STANDARD_CONTROLL_KEYSET.copy()
        self.c_keys_released = STANDARD_CONTROLL_KEYSET.copy()
        self.game_view = game_view
        self.previous_keyset = self.game_view.c_keys_pressed_gny
        for player in self.window.sound_player_register.values():
            player.pause()
        self.board = image_gui['board']
        
        self.widgets.append(self.board)


    def setup(self):
        super().setup()


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            for player in self.window.sound_player_register.values():
                player.play()
            for key in self.game_view.c_keys_pressed_gny.keys():
                self.game_view.c_keys_pressed_gny[key] = self.c_keys_pressed[key]\
                 or (self.previous_keyset[key] and not self.c_keys_released[key])
            
        elif key == arcade.key.ENTER:
            self.game_view.setup()
            self.window.show_view(self.game_view)

        if key in [arcade.key.W, arcade.key.UP]:
            self.c_keys_pressed['jump'] = True
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.c_keys_pressed['left'] = True
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.c_keys_pressed['right'] = True


    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.c_keys_pressed['jump'] = False
            self.c_keys_released['jump'] = True
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.c_keys_pressed['left'] = False
            self.c_keys_released['left'] = True
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.c_keys_pressed['right'] = False
            self.c_keys_released['right'] = True



class GameOverView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        for player in self.window.sound_player_register.values():
            player.pause()
        self.board = image_gui['board']
        self.widgets.append(self.board)

    def setup(self):
        super().setup()

