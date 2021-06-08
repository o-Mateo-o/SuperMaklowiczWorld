"""
Main menu class. (The one activated after the game starts.)
"""

from gamelib.constants import *
from gamelib import widgets, gameview


class MainMenuView(widgets.OptionView):
    """
    Main menu view. Visible eg when starting the game.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
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
            center_y=y_slot + move_up + self.height // 40,
            normal_texture=image_gui['std_0'],
            hover_texture=image_gui['std_1'],
            press_texture=image_gui['std_2'],
            text_label=image_gui['t_options'],
            callback=lambda: self.show_new_view(OptionsMenuView)
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
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        self.button_scrsize.textures_update()


class LevelChoiceView(widgets.OptionView):
    """
    Main menu view. Visible eg when starting the game.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()
        self.level_button_list = []

    def load_level(self, number: int):
        """
        Load the new level. If it is not allowed - show a proper view.
        :param number: level number
        """
        
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
            raise Exception('No such a level defined.')

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
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
            center_y=y_slot * 4,
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
            center_y=y_slot * 3,
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
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        for button in self.level_button_list:
            if button.locked:
                button.texture_0 = button.texture_1 = button.texture_2 = image_gui['locked']
        self.button_scrsize.textures_update()


class OptionsMenuView(widgets.OptionView):
    """
    Options view to change the difficulty.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def swap_difficulty(self):
        """
        Change the "global" difficulty attribute.
        """
        if self.window.difficulty == 'normal':
            self.window.difficulty = 'spicy'
        else:
            self.window.difficulty = 'normal'

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
        self.background = image_background[1]
        self.board = image_gui['board_options']
        y_slot = self.height // 6
        x_slot = self.width // 6
        self.button_diffic = widgets.StandardButton(
            self, 30,
            center_x=x_slot * 3,
            center_y=y_slot * 3,
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
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
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
    """
    Menu with info about the game and its author.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
        self.background = image_background[1]
        self.board = image_gui['board_about']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        self.button_scrsize.textures_update()


class ControlsMenuView(widgets.OptionView):
    """
    Instructions mentu.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
        self.background = image_background[1]
        self.board = image_gui['board_controls']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        """
        Handle the events in the menu. Update textures of tjespecial buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        self.button_scrsize.textures_update()


class ScoresMenuView(widgets.OptionView):
    """
    Best scores view. Shows the locally saved user data.
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
        self.background = image_background[1]
        self.board = image_gui['board_scores']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        self.button_scrsize.textures_update()

    def on_draw(self):
        """
        Draw parent's widgets and draw score numbers.
        """
        super().on_draw()

        arcade.draw_text(str(self.window.best_scores[1][0]),
                         self.width * 0.25, self.height*0.46,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)
        arcade.draw_text(str(self.window.best_scores[1][1]),
                         self.width * 0.25, self.height*0.34,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)

        arcade.draw_text(str(self.window.best_scores[2][0]),
                         self.width * 0.43, self.height*0.46,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)
        arcade.draw_text(str(self.window.best_scores[2][1]),
                         self.width * 0.43, self.height*0.34,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)

        arcade.draw_text(str(self.window.best_scores[3][0]),
                         self.width * 0.62, self.height*0.46,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)
        arcade.draw_text(str(self.window.best_scores[3][1]),
                         self.width * 0.62, self.height*0.34,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)

        arcade.draw_text(str(self.window.best_scores[4][0]),
                         self.width * 0.8, self.height*0.46,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)
        arcade.draw_text(str(self.window.best_scores[4][1]),
                         self.width * 0.8, self.height*0.34,
                         color=arcade.csscolor.BLACK, font_size=self.height//18, font_name=COMIC_SANS_FONT)


class DemoView(widgets.OptionView):
    """
    View with info about the vesion of the game. (If it is only 'demo').
    """

    def __init__(self):
        """
        Create a view and stop the previous sounds.
        """
        super().__init__()
        for player in self.window.sound_player_register.values():
            player.pause()

    def setup(self):
        """
        Set the widges on a layout and set the background.
        """
        self.background = image_background[1]
        self.board = image_gui['board_demo']

        self.button_return = widgets.ReturnButton(self, MainMenuView)
        self.button_list.append(self.button_return)

        self.button_scrsize = widgets.ResizeButton(self)
        self.button_list.append(self.button_scrsize)

        self.button_quit = widgets.QuitButton(self)
        self.button_list.append(self.button_quit)

    def on_update(self, delta_time: float):
        """
        Handle the events in the menu. Update textures of the special buttons.
        :param float delta_time: Time interval since the last time the function was called.
        """
        super().on_update(delta_time)
        self.button_scrsize.textures_update()
