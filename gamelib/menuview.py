"""
Main menu class. (The one activated after the game starts.)
"""

import arcade

from gamelib.constants import *
from gamelib import widgets


class MainMenuView(widgets.OptionView):
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
            text_label=image_gui['t_start']
        )

        self.button_list.append(self.button_start)
        self.widgets.append(self.button_start)

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
        self.widgets.append(self.button_scores)

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
        self.widgets.append(self.button_controls)

        self.button_options = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 2,
            center_y=y_slot + move_up + self.height*1//40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options']
        )

        self.button_list.append(self.button_options)
        self.widgets.append(self.button_options)

        self.button_about = widgets.StandardButton(
            self, choice_scale,
            center_x=x_slot * 4,
            center_y=y_slot + move_up + self.height*1//40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_about']
        )

        self.button_list.append(self.button_about)
        self.widgets.append(self.button_about)

        self.button_scrsize = widgets.StandardButton(
            self, 13,
            center_x=x_slot * 4,
            center_y= move_up + self.height*1//40,
            normal_texture=image_gui['full_true_0'],
            hover_texture=image_gui['full_true_1'],
            press_texture=image_gui['full_true_2'],
        )

        self.button_list.append(self.button_scrsize)
        self.widgets.append(self.button_scrsize)

    
    
       
