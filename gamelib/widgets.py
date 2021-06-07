"""
Widget classes for game gui.
"""
import arcade
import arcade.gui
from arcade.key import B
from gamelib.constants import *
from time import sleep

class OptionView(arcade.View):
    def __init__(self, parent_view=None, draw_parent=False, scrolling_parent=False):
        super().__init__()
        self.mouse = self.mouse = arcade.SpriteCircle(1, arcade.csscolor.BLACK)
        self.draw_parent = draw_parent
        self.button_list = []
        self.parent_view = parent_view
        self.height = self.window.height
        self.width = self.window.width
        if parent_view == None:
            self.window.set_viewport(0, self.width, 0, self.height)
        self.current_button = None
        self.scrolling_parent = scrolling_parent
    
        self.background = None
        self.board = None
        self.parent_view = parent_view
        self.mouse_pressed = False
        self.click = False
        self.unclick = False
        if self.scrolling_parent:
            self.view_left = self.parent_view.view_left 
            self.view_bottom = self.parent_view.view_bottom
        else:
            self.view_left = 0
            self.view_bottom = 0

    def setup(self):
        self.current_button = None
        self.mouse_pressed = False
        self.click = False
        self.unclick = False
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.parent_view != None:
            if not self.window.fullscreen:
                ratio_x = ratio_y = 1
            else:
                ratio_x = self.width/self.parent_view.window.width
                ratio_y = self.height/self.parent_view.window.height
        else:
            if not self.window.fullscreen:
                ratio_x = self.width/WINDOW_WIDTH
                ratio_y = self.height/WINDOW_HEIGHT
            else:
                ratio_x = self.width/self.window.width
                ratio_y = self.height/self.window.height
        self.mouse.center_x = x * ratio_x + self.view_left
        self.mouse.center_y = y * ratio_y + self.view_bottom
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_pressed = True
        self.click = True
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_pressed = False
        self.unclick = True
        
    def on_update(self, delta_time: float):
        #self.viewport_limits_update()
        current_button_set = False
        for button in self.button_list:
            if arcade.check_for_collision(self.mouse, button):
                if not current_button_set:
                    self.current_button = button
                    current_button_set = True
                if self.click:
                    button.clicked = True
                if self.mouse_pressed and button.clicked and button == self.current_button:
                    button.texture_change(2)
       
                elif not self.mouse_pressed and button == self.current_button:
                    button.texture_change(1)
                else:
                    button.texture_change(0)
                if self.unclick:
                    button.on_click()

            else:
                button.clicked = False
                button.texture_change(0)
        self.click = False
        self.unclick = False

    def fullscreen_resize(self):
        
        self.window.set_fullscreen(not self.window.fullscreen)
        self.window.set_viewport(self.view_left, self.view_left+self.width, 
        self.view_bottom, self.view_bottom+self.height)

    def show_new_view(self, view_class):
        new_view = view_class()
        new_view.setup()
        self.window.show_view(new_view)
        
    def on_draw(self):

        arcade.start_render()
        if self.background != None:
            arcade.draw_texture_rectangle(self.width / 2 + self.view_left, self.height/2 + self.view_bottom,
            self.width, self.height, texture=self.background)
        if self.draw_parent:
            self.parent_view.on_draw()
        arcade.draw_texture_rectangle(self.width / 2 + self.view_left, self.height/2 + self.view_bottom,
         self.width*0.9, self.height, texture=self.board)
        for button in self.button_list:
            button.center_x = button.init_center_x + self.view_left
            button.center_y = button.init_center_y + self.view_bottom
            button.draw()
            if button.text_label:
                arcade.draw_scaled_texture_rectangle(button.center_x, button.center_y, button.text_label,
                button.scale)

        


class StandardButton(arcade.Sprite):
    def __init__(self, parent_view, percent_width, center_x, center_y,\
         normal_texture, hover_texture, press_texture,
                 text_label=None, callback=lambda: None):
        super().__init__()
        self.texture_0 = normal_texture
        self.texture_1 = hover_texture
        self.texture_2 = press_texture
        self.texture = self.texture_0
        ratio = 1.8 - parent_view.width/parent_view.height / 2.25
        self.scale = ((percent_width * parent_view.width) / (100 * self.width)) * ratio
        self.center_x = center_x
        self.center_y = center_y
        self.callback = callback
        self.text_label = text_label
        
        self.init_center_x = center_x
        self.init_center_y = center_y
        
        
        
        self.clicked = False

    def on_click(self, arg=None):
        if arg:
            self.callback(arg)
        else:
            self.callback()

    def texture_change(self, t_type):
        if t_type == 0:
            self.texture = self.texture_0
        elif t_type == 1:
            self.texture = self.texture_1
        elif t_type == 2:
            self.texture = self.texture_2

class ResizeButton(StandardButton):
    def __init__(self, parent_view, other_callback=None):
        super().__init__(parent_view, 13,
         parent_view.width // 6 * 4,
         parent_view.height * 0.15 + parent_view.height // 40,
         normal_texture=image_gui[f'full_{parent_view.window.fullscreen}_0'],
         hover_texture=image_gui[f'full_{parent_view.window.fullscreen}_1'],
         press_texture=image_gui[f'full_{parent_view.window.fullscreen}_2'],
         callback=lambda: parent_view.fullscreen_resize())
        if other_callback:
            self.callback = other_callback
        self.parent_view = parent_view

    def textures_update(self):
        self.texture_0 = image_gui[f'full_{self.parent_view.window.fullscreen}_0']
        self.texture_1 = image_gui[f'full_{self.parent_view.window.fullscreen}_1']
        self.texture_2 = image_gui[f'full_{self.parent_view.window.fullscreen}_2']

class QuitButton(StandardButton):
    def __init__(self, parent_view):
        super().__init__(parent_view, 13,
         parent_view.width // 6 * 5 - parent_view.width // 30,
         parent_view.height * 0.15 + parent_view.height // 40,
         normal_texture=image_gui['quit_0'],
         hover_texture=image_gui['quit_1'],
         press_texture=image_gui['quit_2'],
         callback=lambda: parent_view.window.close())
        self.parent_view = parent_view

class ReturnButton(StandardButton):
     def __init__(self, parent_view, return_view_class):
        super().__init__(parent_view, 22,
         parent_view.width // 6 * 2 + parent_view.width // 15,
         parent_view.height * 0.15 + parent_view.height // 40,
         normal_texture=image_gui['return_0'],
         hover_texture=image_gui['return_1'],
         press_texture=image_gui['return_2'],
         text_label=image_gui['t_return'],
         callback=lambda: parent_view.show_new_view(return_view_class))
        self.parent_view = parent_view


    
    

    
