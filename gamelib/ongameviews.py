"""
Initial, pause and other additional view classes.
"""

import time
import arcade

import arcade.gui as gui
from arcade.gui import UIManager
from gamelib.constants import *
from gamelib import widgets
from gamelib import menuviews
from gamelib import gameview


class PauseView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        self.c_keys_pressed = STANDARD_CONTROLL_KEYSET.copy()
        self.c_keys_released = STANDARD_CONTROLL_KEYSET.copy()
        self.game_view = game_view
        self.previous_keyset = self.game_view.c_keys_pressed_gny
        for player in self.window.sound_player_register.values():
            player.pause()
        self.game_view.paused = True

    def resume_game(self):
        self.game_view.paused = False
        self.window.show_view(self.game_view)
        for player in self.window.sound_player_register.values():
            player.play()
        for key in self.game_view.c_keys_pressed_gny.keys():
            self.game_view.c_keys_pressed_gny[key] = self.c_keys_pressed[key]\
                or (self.previous_keyset[key] and not self.c_keys_released[key])

    def resize_pause(self):
        self.window.show_view(self.game_view)
        self.fullscreen_resize()
        
        self.game_view.last_ch_view = self
        self.game_view.reshow = True
        

    def setup(self):
        super().setup()
        self.board = image_gui['board']
        y_slot = WINDOW_HEIGHT // 5 
        x_slot = WINDOW_WIDTH // 6
        move_up = self.height * 0.15

        self.button_back = widgets.StandardButton(
            self, 28,
            center_x=x_slot * 2,
            center_y= y_slot * 3,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_menu'],
            callback=lambda: self.show_new_view(menuviews.MainMenuView)
        )
        self.button_list.append(self.button_back)

        self.button_retry = widgets.StandardButton(
            self, 28,
            center_x=x_slot * 4,
            center_y= y_slot * 3,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_restart'],
            callback=lambda: self.show_new_view(gameview.GameLevel)
        )
        self.button_list.append(self.button_retry)

        self.button_resume = widgets.StandardButton(
            self, 32,
            center_x=x_slot * 3,
            center_y= y_slot * 2,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_resume'],
            callback=lambda: self.resume_game()
        )
        self.button_list.append(self.button_resume)

        self.button_scrsize = widgets.ResizeButton(self, self.resize_pause)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    

    def on_key_press(self, key, _modifiers):
        print(self.mouse.center_y, self.button_quit.center_y, "--", self.mouse.center_x, self.button_quit.center_x)
        if key == arcade.key.ESCAPE:
            self.resume_game()
            
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
        super().on_update(delta_time)
        self.button_scrsize.texture_0 = image_gui[f'full_{self.window.fullscreen}_0']
        self.button_scrsize.texture_1 = image_gui[f'full_{self.window.fullscreen}_1']
        self.button_scrsize.texture_2 = image_gui[f'full_{self.window.fullscreen}_2']



class GameOverView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        super().setup()
        self.board = image_gui['board_loose']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        move_up = self.height * 0.15

        self.button_back = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 2,
            center_y= y_slot * 3 - self.height // 40,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_menu'],
            callback=lambda: self.show_new_view(menuviews.MainMenuView)
        )
        self.button_list.append(self.button_back)

        self.button_retry = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 4,
            center_y= y_slot * 3 - self.height // 40,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_restart'],
            callback=lambda: self.show_new_view(gameview.GameLevel)
        )
        self.button_list.append(self.button_retry)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.texture_0 = image_gui[f'full_{self.window.fullscreen}_0']
        self.button_scrsize.texture_1 = image_gui[f'full_{self.window.fullscreen}_1']
        self.button_scrsize.texture_2 = image_gui[f'full_{self.window.fullscreen}_2']

class WinningView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        super().setup()
        self.board = image_gui['board_win']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        move_up = self.height * 0.15

        self.button_back = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 2,
            center_y= y_slot * 3 - self.height // 40,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_menu'],
            callback=lambda: self.show_new_view(menuviews.MainMenuView)
        )
        self.button_list.append(self.button_back)


        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()
        


