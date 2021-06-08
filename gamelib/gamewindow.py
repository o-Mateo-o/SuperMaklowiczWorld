"""
Game window class.
"""

import arcade, sys
from gamelib.constants import *
from gamelib import auxfunctions
sys.path.append(".")

class GameWindow(arcade.Window):
    def __init__(self, width, height, heading):
        super().__init__(width, height, heading, fullscreen=True)
        # sound volumes
        self.sound_volume_factor = 1
        self.standard_sound_volume = STANDARD_SOUND_VOUME * self.sound_volume_factor
        self.step_volume = STEP_VOUME * self.sound_volume_factor
        self.pain_volume = PAIN_VOLUME * self.sound_volume_factor
        # background
        self.bg_move_x_extension = 1000
        self.bg_move_y_extension = 200
        # data containers
        self.sound_player_register = {}
        # level variable
        self.difficulty = 'normal'
        self.current_level = 1
        self.fork_speed = D_FORK_SPEED
        self.pepper_speed = D_PEPPER_SPEED
        self.moving_block_speed = D_MOVING_BLOCK_SPEED
        
        try:
            data = auxfunctions.get_user_data()
            
            self.available_levels = data[0]
            self.best_scores = data[1]
            
        except:
            
            self.available_levels = {1: True, 2: False, 3: False, 4: False}
            self.best_scores = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0)}

