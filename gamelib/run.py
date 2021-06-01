"""
Game running module.
"""

import sys
sys.path.append(".")

import arcade
from gamelib import game

def run_game(module_name):
    if module_name == "__main__":
        window = game.Game()
        window.setup()
        arcade.run()
    else:
        print("FILE ERROR - cannot open the game.")
