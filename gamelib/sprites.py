"""
Sprite classes of characters and special objects.
"""

import sys

import arcade
from pytiled_parser.objects import TileMap

from gamelib.constants import *

sys.path.append(".")


def init_objects_from_map(object_class, sprite_list: list, map_object: TileMap,\
     layer_name: str, use_spatial_hash: bool):
    object_sub_list = arcade.tilemap.process_layer(
        map_object=map_object, layer_name=layer_name, scaling=MAP_SCALING,
        use_spatial_hash=use_spatial_hash)
    new_object_sub_list = []
    for obj in object_sub_list:
        new_object = object_class()
        new_object.center_x = obj.center_x
        new_object.center_y = obj.center_y
        new_object.texture = obj.texture
        sprite_list.append(new_object)
        new_object_sub_list.append(new_object)
    return new_object_sub_list


class Maklowicz(arcade.Sprite):
    def __init__(self, center_x=2*TL, center_y=6*TL):
        super().__init__(scale=CHARACTER_SCALING)
        self.facing = RIGHT_F
        self.texture = IMG_MAKLOWICZ['idle'][self.facing]
        self.center_x = center_x
        self.center_y = center_y
        self.current_texture = 0

    def figure_mirror(self, facing):
        if self.facing == facing:
            ratio = 1
        else:
            ratio = -1
        self.set_hit_box([[ratio*point[0], point[1]] for point in self.get_hit_box()])
        self.facing = facing

    def update_animation(self, delta_time: float):
        if all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):
            self.texture = IMG_MAKLOWICZ['idle'][self.facing]
        else:
            self.texture = IMG_MAKLOWICZ['jump'][self.facing]

        if self.change_x != 0 and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):

            self.current_texture += 1
            if self.current_texture > 9:
                self.current_texture = 0
            texture_key = 'run1' if self.current_texture > 4 else 'run2'
            self.texture = IMG_MAKLOWICZ[texture_key][self.facing]
        return super().update_animation(delta_time=delta_time)

    def process_keychange(self, keys_pressed):
        if keys_pressed['UP'] and all([engine.can_jump(y_distance=CAN_JUMP_DISTANCE)\
             for engine in self.physics_engines]):
            self.change_y = MAKLOWICZ_JUMP_SPEED

        if keys_pressed['RIGHT']:
            self.figure_mirror(RIGHT_F)
            self.change_x = MAKLOWICZ_SPEED
        elif keys_pressed['LEFT']:
            self.change_x = -MAKLOWICZ_SPEED
            self.figure_mirror(LEFT_F)
        elif not keys_pressed['RIGHT'] and not keys_pressed['LEFT']:
            self.change_x = 0
    
class Pot(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=MAP_SCALING)
        self.picked = False
        self.active = True
    
    def pick_action(self):
        if not self.picked:
            self.change_y = POT_ACTION_SPEED
            self.init_center_y = self.center_y*1
            self.picked = True
        
        if self.center_y >= self.init_center_y + POT_ACTION_HEIGHT:
            self.change_y = -POT_ACTION_SPEED

        if self.center_y < self.init_center_y:
            self.change_y = 0
            self.center_y = self.init_center_y
            #self.texture = cos
            self.active = False



    


