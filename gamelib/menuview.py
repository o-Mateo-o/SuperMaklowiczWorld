"""
Main menu class. (The one activated after the game starts.)
"""

import arcade

from gamelib.constants import *
from gamelib import widgets


class MainMenuView(widgets.OptionView):
    def setup(self):
        self.board = image_gui['board']
        y_slot = self.window.height // 5
        x_slot = self.window.width // 6


        self.button_start = widgets.StandardButton(
            self, 100,
            center_x=x_slot * 3,
            center_y=y_slot * 4 - 50,
            
            normal_texture=image_gui['start_0'],
            hover_texture=image_gui['start_1'],
            press_texture=image_gui['start_2'],
            text_label=image_gui['t_options']
            
        )

        self.button_list.append(self.button_start)
        self.widgets.append(self.button_start)

    
       
