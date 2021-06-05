"""
Initial, pause and other additional view classes.
"""

from gamelib.values import STANDARD_CONTROLL_KEYSET, WINDOW_HEIGHT, WINDOW_WIDTH
import arcade
from gamelib.auxfunctions import sound_player_register

import arcade.gui as gui
from arcade.gui import UIManager
from gamelib.values import *
from gamelib import widgets


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.c_keys_pressed = STANDARD_CONTROLL_KEYSET.copy()
        self.c_keys_released = STANDARD_CONTROLL_KEYSET.copy()
        self.game_view = game_view
        self.previous_keyset = self.game_view.c_keys_pressed_gny
        for player in sound_player_register.values():
            player.pause()
        
        self.ui_manager = UIManager()


    def setup(self):
        y_slot = WINDOW_HEIGHT // 4
        left_column_x = WINDOW_WIDTH // 4
        right_column_x = 3 * WINDOW_WIDTH // 4
        self.ui_manager = UIManager()
        button_normal = image_maklowicz['idle'][0]
        hovered_texture = image_maklowicz['idle'][0]
        pressed_texture = image_maklowicz['idle'][0]

        button = widgets.StandardButton(
            center_x=left_column_x,
            center_y=y_slot * 2,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='UIImageButton'
        )
        self.ui_manager.add_ui_element(button)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.game_view.on_draw()
        arcade.draw_texture_rectangle(WINDOW_WIDTH / 2 + self.game_view.view_left,
         WINDOW_HEIGHT/2 + self.game_view.view_bottom,
         WINDOW_WIDTH*0.8, WINDOW_HEIGHT, texture=image_gui['board'])
        self.ui_manager.on_draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            for player in sound_player_register.values():
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

    def on_update(self, delta_time: float):
        for widget in self.ui_manager._ui_elements:
            widget.place_update(self.game_view.view_left, self.game_view.view_bottom)