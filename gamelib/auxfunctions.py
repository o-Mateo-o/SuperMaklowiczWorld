"""
Helper functions module.
"""

import sys

import arcade
from pyglet import media
from pytiled_parser.objects import TileMap


from gamelib.constants import *

sys.path.append(".")


def init_objects_from_map(object_class, parent_view, sprite_list: list, map_object: TileMap,
                          layer_name: str, use_spatial_hash: bool, obj_speed:float = None):
    # raw objects from map
    object_sub_list = arcade.tilemap.process_layer(
        map_object=map_object, layer_name=layer_name, scaling=MAP_SCALING,
        use_spatial_hash=use_spatial_hash)

    new_object_sub_list = arcade.SpriteList()
    # create objects of given class in place of map objects
    # add them to the sub-container
    for obj in object_sub_list:
        new_object = object_class(parent_view)
        new_object.center_x = obj.center_x
        new_object.center_y = obj.center_y
        if obj_speed != None:
            new_object.obj_speed = obj_speed
            new_object.add_speed()
        new_object.texture = obj.texture
        sprite_list.append(new_object)
        new_object_sub_list.append(new_object)
    return new_object_sub_list



def play_sound(sound: arcade.Sound, player: media.Player,\
     volume: float, loop: bool = False):
    # play sound, but stick with one per audio-layer rule
    new_player = sound.play(volume=volume, loop=loop)
    def _on_player_eos():
        pass
    new_player.on_player_eos = _on_player_eos
    if sound.is_playing(player):
        sound.stop(player)

    return new_player

