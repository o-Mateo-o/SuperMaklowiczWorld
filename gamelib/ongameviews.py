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
from gamelib import auxfunctions


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
        self.button_scrsize.textures_update()



class GameOverView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        for player in self.window.sound_player_register.values():
            player.pause()
        sound_loose = sound_environ['loose'].play(
            volume=self.window.standard_sound_volume)
        self.window.sound_player_register['loose'] = sound_loose
        
        

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
        self.button_scrsize.textures_update()

class WinningView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        for player in self.window.sound_player_register.values():
            player.pause()
        self.game_view = game_view
        sound_win = sound_environ['win'].play(
                volume=self.window.standard_sound_volume)
        self.window.sound_player_register['win'] = sound_win
        self.counter_dill = 0
        self.counter_pepper = 0
        self.animation_tick = 0
        self.animation_done = False
        

    def show_post_win_view(self):
        if self.game_view.collectable_counters['dill']+self.game_view.collectable_counters['pepper'] \
            > self.window.best_scores[self.window.current_level][0]\
             + self.window.best_scores[self.window.current_level][1]:
            self.window.best_scores[self.window.current_level] = (
                self.game_view.collectable_counters['dill'],
                self.game_view.collectable_counters['pepper'])
            auxfunctions.save_user_data(self.window.best_scores, self.window.available_levels)

        self.window.best_scores[self.window.current_level]
        if self.window.current_level+1 in LEVEL_MAPS.keys():
            self.window.available_levels[self.window.current_level+1] = True
            new_view = PostWinningView(self.game_view)
            new_view.setup()
            self.window.show_view(new_view)
        else:
            new_view = menuviews.MainMenuView()
            new_view.setup()
            self.window.show_view(new_view)

    def setup(self):
        super().setup()
        self.counter_dill = 0
        self.counter_pepper = 0
        self.board = image_gui['board_win']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        move_up = self.height * 0.15


        self.button_back = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 4,
            center_y= y_slot * 3 - self.height // 40,
            normal_texture=image_gui[f'std_0'],
            hover_texture=image_gui[f'std_1'],
            press_texture=image_gui[f'std_2'],
            text_label=image_gui['t_accept'],
            callback=lambda: self.show_post_win_view()
        )
        self.button_list.append(self.button_back)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_draw(self):
        super().on_draw()
        arcade.draw_text(str(self.counter_dill), self.button_back.center_x - WINDOW_WIDTH*0.38,
          self.button_back.center_y, arcade.csscolor.BLACK, 40, font_name=COMIC_SANS_FONT)
        arcade.draw_text(str(self.counter_pepper), self.button_back.center_x - WINDOW_WIDTH*0.38,
          self.button_back.center_y - WINDOW_HEIGHT*0.17, arcade.csscolor.BLACK, 40, font_name=COMIC_SANS_FONT)

    def on_update(self, delta_time: float):
        self.animation_tick += 1
        if self.animation_tick > WIDGET_ANIMATION_SPEED:
            self.animation_tick = 0
        if self.animation_tick == 0:
            if self.counter_dill < self.game_view.collectable_counters['dill']:
                self.counter_dill += 1
            if self.counter_pepper < self.game_view.collectable_counters['pepper']:
                self.counter_pepper += 1

        if self.counter_pepper >= self.game_view.collectable_counters['pepper']\
            and self.counter_dill >= self.game_view.collectable_counters['dill']:
            self.animation_done = True

        current_button_set = False
        # mouse
        for button in self.button_list:
            if arcade.check_for_collision(self.mouse, button):
                if not current_button_set:
                    self.current_button = button
                    current_button_set = True
                if self.click:
                    button.clicked = True
                if self.mouse_pressed and button.clicked and button == self.current_button\
                    and self.animation_done:
                    button.texture_change(2)
       
                elif not self.mouse_pressed and button == self.current_button:
                    button.texture_change(1)
                else:
                    button.texture_change(0)
                if self.unclick and self.animation_done:
                    button.on_click()

            else:
                button.clicked = False
                button.texture_change(0)
        self.click = False
        self.unclick = False
        # size button 
        self.button_scrsize.textures_update()

class PostWinningView(widgets.OptionView):
    def __init__(self, game_view):
        super().__init__(game_view, draw_parent=True, scrolling_parent=True)
        
    def next_level(self):
        self.window.current_level += 1
        ###################################################################
        ###################          DEMO         #########################
        ###################################################################

        if self.window.current_level in FORBIDDEN_LEVELS:
            self.show_new_view(menuviews.DemoView)

        ##################################################################
        elif self.window.current_level in LEVEL_MAPS.keys():
            self.show_new_view(menuviews.MainMenuView)
        else:
            self.show_new_view(gameview.GameLevel)

    def setup(self):
        super().setup()
        self.board = image_gui['board']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        move_up = self.height * 0.05
        choice_scale = 28

        self.button_restart = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 4 - move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_restart'],
            callback=lambda: self.show_new_view(gameview.GameLevel)
        )

        self.button_list.append(self.button_restart)

        self.button_next_level = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 4 - move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_next_level'],
            callback=lambda: self.next_level()
        )

        self.button_list.append(self.button_next_level)

        self.button_levels = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 2 + 2 * move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_levels'],
            callback=lambda: self.show_new_view(menuviews.LevelChoiceView)
        )

        self.button_list.append(self.button_levels)

        self.button_menu = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 2 + 2 * move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_menu'],
            callback=lambda: self.show_new_view(menuviews.MainMenuView)
        )

        self.button_list.append(self.button_menu)


        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()
        


