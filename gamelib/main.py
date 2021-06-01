#!/usr/bin/env python
"""
Game running module.
"""

import sys

sys.path.append(".")
import arcade

from gamelib import game

if __name__ == "__main__":
    window = game.Game()
    window.setup()
    arcade.run()
