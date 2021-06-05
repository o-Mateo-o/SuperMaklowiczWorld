"""
Widget classes for game gui.
"""
import arcade.gui
from arcade.gui import UIManager


class StandardButton(arcade.gui.UIImageButton):
    def __init__(self, center_x, center_y, normal_texture, hover_texture, press_texture,
                 text, callback=lambda: print('None')):
        super().__init__(center_x=center_x, center_y=center_y, normal_texture=normal_texture,
                         hover_texture=hover_texture, press_texture=press_texture, text=text)
        self.callback = callback
        self.init_center_x = center_x
        self.init_center_y = center_y

    def on_click(self):
        self.callback()

    def place_update(self, view_left, view_bottom):
        self.center_x = self.init_center_x + view_left
        self.center_y = self.init_center_y + view_bottom
