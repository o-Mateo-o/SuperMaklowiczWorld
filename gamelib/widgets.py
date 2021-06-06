"""
Widget classes for game gui.
"""
import arcade
import arcade.gui
from arcade.key import B
from gamelib.constants import *

class OptionView(arcade.View):
    def __init__(self, parent_view=None, draw_parent=False, scrolling_parent=False):
        super().__init__()
        self.mouse = self.mouse = arcade.SpriteCircle(1, arcade.csscolor.BLACK)
        self.draw_parent = draw_parent
        self.button_list = []
        self.height = self.window.height
        self.width = self.window.width
        self.current_button = None

        if scrolling_parent:
            self.view_left = parent_view.view_left 
            self.view_bottom = parent_view.view_bottom
        else:
            self.view_left = 0
            self.view_bottom = 0

        self.background = None
        self.board = None
        self.widgets = []
        self.parent_view = parent_view
        self.mouse_pressed = False
        self.click = False

    def setup(self):
        self.current_button = None
        self.mouse_pressed = False
        self.click = False
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH


    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse.center_x = x
        self.mouse.center_y = y
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_pressed = True
        self.click = True
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_pressed = False
        
    def on_update(self, delta_time: float):
        for button in self.button_list:
            if arcade.check_for_collision(self.mouse, button):
                if self.click:
                    button.clicked = True
                    
                    if self.click:
                        button.on_click()
                if self.mouse_pressed and button.clicked:
                    button.texture_change(2)
       
                elif not self.mouse_pressed:
                    button.texture_change(1)
            else:
                button.clicked = False
                button.texture_change(0)
        self.click = False
    
    def on_draw(self):

        arcade.start_render()
        if self.draw_parent:
            self.parent_view.on_draw()
        arcade.draw_texture_rectangle(self.width / 2 + self.view_left, self.height/2 + + self.view_bottom,
         self.width*0.9, self.height, texture=self.board)
        for button in self.button_list:

            button.draw()

            if button.text_label:
                arcade.draw_scaled_texture_rectangle(button.center_x, button.center_y, button.text_label,
                button.scale)


class StandardButton(arcade.Sprite):
    def __init__(self, parent_view, percent_width, center_x, center_y,\
         normal_texture, hover_texture, press_texture,
                 text_label=None, callback=lambda: print('')):
        super().__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.callback = callback
        self.text_label = text_label
        self.texture_0 = normal_texture
        self.texture_1 = hover_texture
        self.texture_2 = press_texture
        self.init_center_x = center_x
        self.init_center_y = center_y
        
        self.texture = self.texture_0
        ratio = 1.5
        self.scale = ((percent_width * parent_view.width) / (100 * self.width)) * ratio
        self.clicked = False

    def on_click(self):
        self.callback()

    def texture_change(self, t_type):
        if t_type == 0:
            self.texture = self.texture_0
        if t_type == 1:
            self.texture = self.texture_1
        if t_type == 2:
            self.texture = self.texture_2

    
    

    
