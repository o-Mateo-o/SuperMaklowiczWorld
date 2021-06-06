"""
Main menu class. (The one activated after the game starts.)
"""

import arcade

from gamelib.constants import *
from gamelib import widgets
    

class MainMenuView(widgets.OptionView):
    def __init__(self):
        super().__init__()
    def show_level_list(self):
        level_list = LevelChoiceView()
        level_list.setup()
        self.window.show_view(level_list)

    def setup(self):
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
            callback=lambda: self.show_level_list()
        )

        self.button_list.append(self.button_start)

        self.button_scores = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot * 2 + move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_scores']
        )

        self.button_list.append(self.button_scores)

        self.button_controls = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot * 2 + move_up,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_controls']
        )

        self.button_list.append(self.button_controls)

        self.button_options = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot + move_up + self.height //40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options']
        )

        self.button_list.append(self.button_options)

        self.button_about = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot + move_up + self.height // 40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_about']
        )

        self.button_list.append(self.button_about)

        self.button_scrsize = widgets.StandardButton(
            self, 13,
            center_x=x_slot * 4,
            center_y= move_up + self.height // 40,
            normal_texture=image_gui['full_true_0'],
            hover_texture=image_gui['full_true_1'],
            press_texture=image_gui['full_true_2'],
            callback=lambda: self.fullscreen_resize()
            
        )

        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.StandardButton(
            self, 13,
            center_x=x_slot * 5 - self.width // 30,
            center_y= move_up + self.height // 40,
            normal_texture=image_gui['quit_0'],
            hover_texture=image_gui['quit_1'],
            press_texture=image_gui['quit_2'],
            callback=lambda: self.window.close()
        )

        self.button_list.append(self.button_quit)

    

class LevelChoiceView(widgets.OptionView):
    def return_to_main(self):
        menu_view = MainMenuView()
        menu_view.setup()
        self.window.show_view(menu_view)
    def setup(self):
        self.board = image_gui['board']
        y_slot = self.height // 5 
        x_slot = self.width // 6
        choice_scale = 28
        move_up = self.height * 0.15

        self.button_l1 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 3,
            center_y=y_slot * 3,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options']
        )
        self.button_list.append(self.button_l1)

        self.button_l2 = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 3,
            center_y=y_slot * 2 ,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options']
        )
        self.button_list.append(self.button_l2)


        self.button_return = widgets.StandardButton(
            self, 24,
            center_x=x_slot * 2,
            center_y=move_up + self.height // 40,
            normal_texture=image_gui['return_0'],
            hover_texture=image_gui['return_1'],
            press_texture=image_gui['return_2'],
            text_label=image_gui['t_return'],
            callback=lambda: self.return_to_main()
        )
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.StandardButton(
            self, 13,
            center_x=x_slot * 4,
            center_y= move_up + self.height // 40,
            normal_texture=image_gui['full_true_0'],
            hover_texture=image_gui['full_true_1'],
            press_texture=image_gui['full_true_2'],
            callback=lambda: self.fullscreen_resize()
            
        )

        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.StandardButton(
            self, 13,
            center_x=x_slot * 5 - self.width // 30,
            center_y= move_up + self.height // 40,
            normal_texture=image_gui['quit_0'],
            hover_texture=image_gui['quit_1'],
            press_texture=image_gui['quit_2'],
            callback=lambda: self.window.close()
        )

        self.button_list.append(self.button_quit)

        
    
    
       
