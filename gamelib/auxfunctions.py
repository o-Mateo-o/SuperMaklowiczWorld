"""
Helper functions module.
"""

import os
import sys

import arcade
from pyglet import media
from pytiled_parser.objects import TileMap

from gamelib.constants import *

sys.path.append(".")


def init_objects_from_map(object_class, parent_view, sprite_list: arcade.SpriteList, map_object: TileMap,
                          layer_name: str, use_spatial_hash: bool, obj_speed: float = None) -> arcade.SpriteList:
    """
    Initialize objects of various classes basing on the position from map layer.
    :param object_class: class of the desired objects
    :param parent_view: arcade View which displays given objects
    :param sprite_list: superior sprite list to add the objects to
    :param map_object: a map to read data from
    :param layer_name: name of the map layer with given objects
    :param use_spatial_hash: info about arcade spatial hashing - standard bool
    :param obj_speed: initial object speed - if they move
    """
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


def play_sound(sound: arcade.Sound, player: media.Player,
               volume: float, loop: bool = False) -> media.Player:
    """
    Play sound but stick with "one-per-player" rule
    :param sound: a processed audio file to be played
    :param player: pyglet media player considered as a sound layer
    :param volume: volume of the sound layer
    :param loop: info about found looping
    :return: new player to overrite the one which is currently on a given layer
    """
    new_player = sound.play(volume=volume, loop=loop)

    def _on_player_eos():
        pass
    new_player.on_player_eos = _on_player_eos
    if sound.is_playing(player):
        sound.stop(player)

    return new_player


def save_user_data(best_scores: dict, available_levels: dict):
    """
    Create or overrite the file with local user data - scores and levels.
    If the process fails - raise an error.
    :param best_scores: dictionary of user's best scores
    :param available_levels: dictionary of user's available levels
    """
    # create a dir - if needed
    if not os.path.isdir(os.path.dirname(USER_DATA_PATH)):
        os.mkdir(os.path.dirname(USER_DATA_PATH))
    lines = []
    max_level = 0
    # prepare data from variables
    for key in sorted(available_levels):
        if available_levels[key] == True:
            max_level = key
    lines.append('DO NOT MODIFY THIS FILE\n')
    lines.append('%\n')
    lines.append(str(max_level)+'\n')
    for key in sorted(best_scores):
        lines.append('#\n')
        lines.append(str(best_scores[key][0])+'\n')
        lines.append(str(best_scores[key][1])+'\n')
    lines.append('%\n')
    # save in file
    try:
        with open(USER_DATA_PATH, 'w') as file:
            file.writelines(lines)
    except:
        pass


def get_user_data() -> tuple:
    """
    Read local user data from file.
    If it fails - raise exceptions.
    :return: tuple of two dicts - (available_levels, best_scores)
    """
    data_start = False
    read_levels = False
    read_score = 0
    filelines = []
    available_level_max = 0
    best_scores_dill = []
    best_scores_pepper = []
    best_scores = {}
    available_levels = {}
    # read file
    try:
        with open(USER_DATA_PATH, 'r') as file:
            filelines = file.readlines()
    except:
        raise Exception("cannot read the file")
    # parse data
    for line in filelines:
        if data_start and line[0] == '%':
            break

        if data_start and read_levels:
            try:
                available_level_max = int(line[:-1])
            except:
                raise Exception('not int vals')
            read_levels = False

        if data_start and read_score in [1, 2] and not read_levels:

            if read_score > 2:
                read_score = 0
            try:
                if read_score == 1:
                    best_scores_dill.append(int(line[:-1]))
                if read_score == 2:
                    best_scores_pepper.append(int(line[:-1]))
            except:
                raise Exception('not int vals')
            read_score += 1
        if line[0] == '%':
            data_start = True
            read_levels = True
        if line[0] == '#' and data_start:
            read_score = 1
    if available_level_max < 1 or available_level_max > max(LEVEL_MAPS.keys()):
        raise Exception('false data')

    # save data to the variables
    for i in range(0, len(best_scores_pepper)):

        if best_scores_pepper[i] < 0 or best_scores_dill[i] < 0:
            raise Exception('false data')
        best_scores[i+1] = (best_scores_dill[i], best_scores_pepper[i])
        if i+1 <= available_level_max:
            available_levels[i+1] = True
        else:
            available_levels[i+1] = False

    return (available_levels, best_scores)
