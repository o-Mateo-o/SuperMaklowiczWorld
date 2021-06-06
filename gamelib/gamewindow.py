"""
Game window class.
"""

import arcade

class GameWindow(arcade.Window):
    def __init__(self, width, height, heading):
        super().__init__(width, height, heading, fullscreen=True)
        # sound volumes
        self.sound_volume_factor = 1
        self.standard_sound_volume = 1 * self.sound_volume_factor
        self.step_volume = 0.5 * self.sound_volume_factor
        self.pain_volume = 0.8*self.sound_volume_factor
        # background
        self.bg_move_x_extension = 1000
        self.bg_move_y_extension = 200
        # data containers
        self.sound_player_register = {}