"""
Game running module.
"""

import sys
sys.path.append(".")

import arcade
from gamelib import game

def run_game():
    window = game.Game()
    window.setup()
    arcade.run()