"""
Classes for additional pyhsics features.
"""

import arcade

class PhysicsEngineEnemy(arcade.PhysicsEngineSimple):
    """
    Enemy physics. The same a simple engine
                     but with gravity added.
    Don't allow to go through walls and add jump gravity.
    """
    def __init__(self, player_sprite: arcade.Sprite,
     walls: arcade.SpriteList, gravity: float = 1):
        """
        Create a physic engine.
        :param player_sprite: sprite od an enemy.
        :param walls: block that a character can't move through.
        :param gravity: gravity constant.
        """
        super().__init__(player_sprite, walls)
        self.gravity_constant = gravity

    def update(self):
        """
        Update character's velocity and position.
        """
        self.player_sprite.change_y -= self.gravity_constant
        super().update()