"""
Helper functions module.
"""

import sys

import arcade
from pyglet import media
from pytiled_parser.objects import TileMap

from gamelib.constants import *

sys.path.append(".")

def init_objects_from_map(object_class, sprite_list: list, map_object: TileMap,\
     layer_name: str, use_spatial_hash: bool):
    object_sub_list = arcade.tilemap.process_layer(
        map_object=map_object, layer_name=layer_name, scaling=MAP_SCALING,
        use_spatial_hash=use_spatial_hash)
    new_object_sub_list = arcade.SpriteList()
    for obj in object_sub_list:
        new_object = object_class()
        new_object.center_x = obj.center_x
        new_object.center_y = obj.center_y
        new_object.texture = obj.texture
        sprite_list.append(new_object)
        new_object_sub_list.append(new_object)
    return new_object_sub_list

def play_sound(sound: arcade.Sound, player: media.Player):
    if sound.is_playing(player):
        sound.stop(player)
    return sound.play()