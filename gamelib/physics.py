"""
Classes for additional pyhsics features.
"""

import arcade

class PhysicsEngineEnemy(arcade.PhysicsEngineSimple):
    def __init__(self, player_sprite: arcade.Sprite,
     walls: arcade.SpriteList, gravity: float = 1):
        super().__init__(player_sprite, walls)
        self.gravity_constant = gravity

    def update(self):
        self.player_sprite.change_y -= self.gravity_constant
        super().update()