"""
Main menu class. (The one activated after the game starts.)
"""

import arcade

from gamelib.constants import *
from gamelib import widgets
from gamelib import gameview
    

class MainMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board']
        y_slot = self.height // 5 
        x_slot = self.width // 6
        choice_scale = 28
        move_up = self.height * 0.15

        self.button_start = widgets.StandardButton(
            self, 50,
            center_x=x_slot * 3,
            center_y=y_slot * 3 + move_up,
            normal_texture=image_gui['start_0'],
            hover_texture=image_gui['start_1'],
            press_texture=image_gui['start_2'],
            text_label=image_gui['t_start'],
            callback=lambda: self.show_new_view(LevelChoiceView)
        )

        self.button_list.append(self.button_start)

        self.button_scores = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 2 + move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_scores'],
            callback=lambda: self.show_new_view(ScoresMenuView)

        )

        self.button_list.append(self.button_scores)

        self.button_controls = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 2 + move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_controls'],
            callback=lambda: self.show_new_view(ControlsMenuView)
        )

        self.button_list.append(self.button_controls)

        self.button_options = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot + move_up + self.height //40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options'],
            callback= lambda: self.show_new_view(OptionsMenuView)
        )

        self.button_list.append(self.button_options)

        self.button_about = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot + move_up + self.height // 40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_about'],
            callback=lambda: self.show_new_view(AboutMenuView)
        )

        self.button_list.append(self.button_about)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()

    

class LevelChoiceView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
        self.level_button_list = []

    def load_level(self, number):
        ###################################################################
        ###################          DEMO         #########################
        ###################################################################

        if number in FORBIDDEN_LEVELS:
            self.show_new_view(DemoView)

        ##################################################################
        elif number in LEVEL_MAPS.keys():
            self.window.current_level = number
            self.show_new_view(gameview.GameLevel)
        else:
            print('No such a level defined.')

    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        choice_scale = 25

        self.button_l1 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 4,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_level1'],
            callback=lambda: self.load_level(1)
        )
        self.button_list.append(self.button_l1)
        self.level_button_list.append(self.button_l1)

        self.button_l2 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 4 ,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_level2'],
            callback=lambda: self.load_level(2)
        )
        self.button_list.append(self.button_l2)
        self.level_button_list.append(self.button_l2)

        self.button_l3 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 3,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_level3'],
            callback=lambda: self.load_level(3)
        )
        self.button_list.append(self.button_l3)
        self.level_button_list.append(self.button_l3)

        self.button_l4 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 3 ,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_level4'],
            callback=lambda: self.load_level(4)
        )
        self.button_list.append(self.button_l4)
        self.level_button_list.append(self.button_l4)
        for idx, button in enumerate(self.level_button_list):
            button.locked = not self.window.available_levels[idx+1]
        

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        for button in self.level_button_list:
            if button.locked:
                button.texture_0 = button.texture_1 = button.texture_2 = image_gui['locked']
        self.button_scrsize.textures_update()

class OptionsMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def swap_difficulty(self):
        if self.window.difficulty == 'normal':
            self.window.difficulty = 'spicy'
        else:
            self.window.difficulty = 'normal'
    
    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board_options']
        y_slot = self.height // 6 
        x_slot = self.width // 6
        self.button_diffic = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 3,
            center_y=y_slot * 3 ,
            normal_texture=image_gui['diff_normal_0'],
            hover_texture=image_gui['diff_normal_1'],
            press_texture=image_gui['diff_normal_2'],
            callback=lambda: self.swap_difficulty()
        )
        self.button_list.append(self.button_diffic)

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.window.difficulty == 'normal':
            self.button_diffic.texture_0 = image_gui['diff_normal_0']
            self.button_diffic.texture_2 = image_gui['diff_normal_1']
            self.button_diffic.texture_1 = image_gui['diff_normal_2']
        else:
            self.button_diffic.texture_0 = image_gui['diff_spicy_0']
            self.button_diffic.texture_2 = image_gui['diff_spicy_1']
            self.button_diffic.texture_1 = image_gui['diff_spicy_2']

        self.button_scrsize.textures_update()

class AboutMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board_about']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()

class ControlsMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board_controls']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()

class ScoresMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board_scores']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()
    
class DemoView(widgets.OptionView):
    def __init__(self):
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
    def setup(self):
        self.background = image_background[1]
        self.board = image_gui['board_demo']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.button_scrsize.textures_update()
    
    


        
    
    
       
