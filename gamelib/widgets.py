"""
Widget classes for game gui.
"""
import arcade
import arcade.gui
from gamelib import constants, widgets

class OptionView(arcade.View):
    def __init__(self, parent_view=None):
        super().__init__()
        self.mouse = self.mouse = arcade.SpriteCircle(1, arcade.csscolor.BLACK)
        self.button_list = []
        self.height = self.window.height
        self.width = self.window.width
        self.background = None
        self.board = None
        self.widgets = []
        self.parent_view = parent_view
        self.mouse_pressed = False
        self.click = False

    def setup(self):
        self.mouse_pressed = False
        self.click = False
        self.height = self.window.height
        self.width = self.window.width


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

    def place_update(self, view_left, view_bottom):
        self.center_x = self.init_center_x + view_left
        self.center_y = self.init_center_y + view_bottom
        
    def on_update(self, delta_time: float):
        if self.parent_view:
            for widget in self.widgets:
                widget.place_update(self.parent_view.view_left, self.parent_view.view_bottom)
        for button in self.button_list:
            if arcade.check_for_collision(self.mouse, button):
                if self.click:
                    button.clicked = True
                if self.mouse_pressed and button.clicked:
                    button.texture_change(2)
                    if self.click:
                        button.on_click()
                elif not self.mouse_pressed:
                    button.texture_change(1)
            else:
                button.clicked = False
                button.texture_change(0)
        self.click = False
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width / 2, self.height/2,
         self.width*0.9, self.height, texture=self.board)
        for widget in self.widgets:
            widget.draw()
            arcade.draw_scaled_texture_rectangle(widget.center_x, widget.center_y, widget.text_label,
            widget.scale)



class StandardButton(arcade.Sprite):
    def __init__(self, parent_view, percent_width, center_x, center_y, normal_texture, hover_texture, press_texture,
                 text_label, callback=lambda: print('None')):
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
        self.scale = (percent_width * parent_view.width) / (100 * self.width)
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

    
    

    
