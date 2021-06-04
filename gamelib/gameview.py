"""
Main game view module to handle all the actions in the gameplay and display it.
"""

from pyglet import media
from gamelib.values import *
from gamelib import sprites
from gamelib import auxfunctions
import arcade
import sys
import random

sys.path.append(".")


class GameLevel(arcade.View):

    def __init__(self):
        super().__init__()
        # keys handled and projection properities
        self.keys_pressed = {'jump': False, 'left': False, 'right': False}
        self.view_bottom = 0
        self.view_left = 0
        self.ttt = 0

        # counters
        self.level_end = None
        self.maklowicz_lives = None
        self.collectable_counters = None

        # sprites
        self.character_cont_list = None
        self.block_list = None
        self.pot_sublist = None
        self.pots_picked = None
        self.dill_list = None
        self.pepper_enemy_list = None
        self.pepper_item_list = None
        self.knives_list = None
        self.fork_list = None

        self.maklowicz = None
        self.maklowicz_head_collider = None
        self.maklowicz_shoes_collider = None
        self.maklowicz_shoes_collider2 = None
        self.pepper_physics_engines = None

        # sounds

        # map
        self.lvl_map = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        # counters
        self.level_end = 0  # 0 - not finished yet; 1 - won; -1 - lost
        self.maklowicz_lives = 3
        self.collectable_counters = {'dill': 0, 'pepper': 0}

        # sprite empty lists
        self.character_cont_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList(use_spatial_hash=True)
        self.limit_list = arcade.SpriteList(use_spatial_hash=True)
        self.pots_picked = set()
        self.dill_list = arcade.SpriteList()
        self.pepper_enemy_list = arcade.SpriteList()
        self.pepper_item_list = arcade.SpriteList()

        # sounds empty lists

        # main character and head-box
        self.maklowicz = sprites.Maklowicz(2*TL, 6*TL)
        self.maklowicz_head_collider = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x, center_y=self.maklowicz.center_y)
        self.maklowicz_shoes_collider = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x, center_y=self.maklowicz.center_y)
        self.maklowicz_shoes_collider2 = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x, center_y=self.maklowicz.center_y)
        self.maklowicz_head_collider.texture = image_maklowicz['box_h'][0]
        self.maklowicz_shoes_collider.texture = image_maklowicz['box_s'][0]
        self.maklowicz_shoes_collider2.texture = image_maklowicz['box_s'][0]

        self.character_cont_list.append(self.maklowicz)
        self.character_cont_list.append(self.maklowicz_head_collider)
        self.character_cont_list.append(self.maklowicz_shoes_collider)
        self.character_cont_list.append(self.maklowicz_shoes_collider2)

        # map static
        self.lvl_map = TEST_MAP
        self.block_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                       layer_name=MAP_LAYER['terrain1'],
                                                       scaling=MAP_SCALING,
                                                       use_spatial_hash=True)
        self.limit_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                       layer_name=MAP_LAYER['limits'],
                                                       scaling=MAP_SCALING,
                                                       use_spatial_hash=True)
        # map objects
        self.pot_sublist = auxfunctions.init_objects_from_map(sprites.Pot, self.block_list, self.lvl_map,
                                                              MAP_LAYER['pots'], True)
        self.dill_list = auxfunctions.init_objects_from_map(sprites.Dill, self.dill_list, self.lvl_map,
                                                            MAP_LAYER['dill'], False)
        self.pepper_enemy_list = auxfunctions.init_objects_from_map(sprites.PepperEnemy, self.pepper_enemy_list,
                                                                    self.lvl_map, MAP_LAYER['pepper_enemy'], False)
        self.knives_list = auxfunctions.init_objects_from_map(sprites.Knives, self.block_list,
                                                              self.lvl_map, MAP_LAYER['knives'], True)
        self.fork_list = auxfunctions.init_objects_from_map(sprites.Fork, self.block_list,
                                                            self.lvl_map, MAP_LAYER['forks'], False)
        for knives in self.knives_list:
            knives.initial_move()
        for fork in self.fork_list:
            fork.adjust_hitbox()

        # physic engines
        self.pepper_physics_engines = []
        self.physics_engine_maklowicz = arcade.PhysicsEnginePlatformer(self.maklowicz,
                                                                       self.block_list,
                                                                       GRAVITY)
        for papryka in self.pepper_enemy_list:
            self.pepper_physics_engines.append(
                arcade.PhysicsEnginePlatformer(papryka, self.block_list, GRAVITY))

        self.physics_engine_pymunk = arcade.PymunkPhysicsEngine(
            (0, PYMUNK_GRAVITY), PYMUNK_DAMP)

        # add objects to engines
        self.maklowicz.physics_engines.append(self.physics_engine_maklowicz)

        self.physics_engine_pymunk.add_sprite_list(
            self.block_list, body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine_pymunk.add_sprite_list(self.dill_list)
        self.physics_engine_pymunk.add_sprite_list(self.pepper_item_list)

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.keys_pressed['jump'] = True
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.keys_pressed['left'] = True
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.keys_pressed['right'] = True

        self.maklowicz.process_keychange(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.UP]:
            self.keys_pressed['jump'] = False
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.keys_pressed['left'] = False
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.keys_pressed['right'] = False

        self.maklowicz.process_keychange(self.keys_pressed)

    def on_draw(self):
        arcade.start_render()
        map_end_length = self.lvl_map.tile_size[0] * \
            MAP_SCALING*self.lvl_map.map_size[0]
        addit_x = WINDOW_WIDTH / 2
        bg_center_x = WINDOW_WIDTH / 2 + self.view_left * \
            (1 - (addit_x / (map_end_length + self.view_left)))
        arcade.draw_texture_rectangle(bg_center_x, WINDOW_HEIGHT/2+self.view_bottom,
                                      WINDOW_WIDTH + addit_x, WINDOW_HEIGHT, image_background[1])
        self.maklowicz.draw()
        self.block_list.draw()
        self.dill_list.draw()
        self.pepper_enemy_list.draw()
        self.pepper_item_list.draw()

        # current score info
        scores_place_x = self.view_left
        scores_place_y = self.view_bottom + WINDOW_HEIGHT
        arcade.draw_texture_rectangle(scores_place_x + 3*TL//2 + 10, scores_place_y - TL//2,
                                      3*TL*SCORE_SCALING, TL*SCORE_SCALING, image_hearts[self.maklowicz_lives])
        dill_text = str(self.collectable_counters['dill'])
        arcade.draw_text(dill_text, scores_place_x + TL + 20, scores_place_y - 2*TL - TL//2 + 10,
                         arcade.csscolor.MIDNIGHT_BLUE, 30*SCORE_SCALING, font_name=COMIC_SANS_FONT)

        arcade.draw_texture_rectangle(scores_place_x + TL//2 + 10, scores_place_y - 2*TL + 10,
                                      TL*SCORE_SCALING, TL*SCORE_SCALING, image_collectable['dill'])
        pepper_text = str(self.collectable_counters['pepper'])
        arcade.draw_text(pepper_text, scores_place_x + TL + 20, scores_place_y - 3*TL - TL//2 + 10,
                         arcade.csscolor.MIDNIGHT_BLUE, 30*SCORE_SCALING, font_name=COMIC_SANS_FONT)

        arcade.draw_texture_rectangle(scores_place_x + TL//2 + 10, scores_place_y - 3*TL + 10,
                                      TL*SCORE_SCALING, TL*SCORE_SCALING, image_collectable['pepper'])

        if self.maklowicz.hurt:
            self.ttt += 1
        if self.ttt > 0:
            self.ttt += 1
        if self.ttt > 8:
            self.ttt = 0
        if self.ttt != 0:
            arcade.draw_rectangle_filled(self.view_left+WINDOW_WIDTH/2, self.view_bottom+WINDOW_HEIGHT/2,
                                        WINDOW_WIDTH, WINDOW_HEIGHT, (255, 0, 0, 50))

    def on_update(self, delta_time):
        # physics update
        self.maklowicz.update()
        self.pepper_enemy_list.update()
        self.fork_list.update()
        self.physics_engine_maklowicz.update()
        self.physics_engine_pymunk.step()
        for engine in self.pepper_physics_engines:
            engine.update()

        # accomp hitbox move
        self.maklowicz_head_collider.position = (
            self.maklowicz.center_x, self.maklowicz.center_y + MAKLOWICZ_HEAD_EXTENSION)
        self.maklowicz_shoes_collider.position = (
            self.maklowicz.center_x, self.maklowicz.center_y + MAKLOWICZ_SHOES_EXTENSION)
        self.maklowicz_shoes_collider2.position = (
            self.maklowicz.center_x, self.maklowicz.center_y + MAKLOWICZ_SHOES_EXTENSION_ITEMS)

        # pots collisions and action
        self.pots_picked.update(set(arcade.check_for_collision_with_list(
            self.maklowicz_head_collider, self.pot_sublist)))

        for pot in self.pots_picked:
            if pot.active:
                if not pot.picked:
                    for _ in range(0, DILL_DROP):
                        new_dill = sprites.Dill(pot)
                        self.dill_list.append(new_dill)
                        self.physics_engine_pymunk.add_sprite(
                            new_dill, friction=1, collision_type="item")
                        self.physics_engine_pymunk.apply_force(new_dill, (random.randint(
                            -POPPING_X_FORCE_RANGE_LIMIT, POPPING_X_FORCE_RANGE_LIMIT), POPPING_Y_FORCE))
                pot.pick_action()

        # pepper enemy collsisions
        for pepper in self.pepper_enemy_list:
            if pepper.transform_to_item:
                new_pepper = sprites.PepperItem(pepper)
                self.pepper_item_list.append(new_pepper)
                self.physics_engine_pymunk.add_sprite(
                            new_pepper, friction=1, collision_type="item")
                pepper.transform_to_item = False
            # limit - reverse speed
            if arcade.check_for_collision_with_list(pepper, self.limit_list):
                pepper.change_x = -pepper.change_x
            # pepper kiled
            if arcade.check_for_collision(self.maklowicz_shoes_collider, pepper)\
                    and self.maklowicz.change_y < 0 and not pepper.killed:
                self.maklowicz.change_y = MAKLOWICZ_JUMP_SPEED
                pepper.killed = True
                # self.pepper_enemy_list.remove(pepper)
            # hurt maklowicz
            if arcade.check_for_collision(self.maklowicz, pepper) and not pepper.killed:
                self.maklowicz_lives = self.maklowicz.hurt_action(
                    self.maklowicz_lives)

        # knives and forks collision
        knives_collision = arcade.check_for_collision_with_list(
            self.maklowicz_shoes_collider2, self.knives_list)
        if knives_collision:
            self.maklowicz_lives = self.maklowicz.hurt_action(
                self.maklowicz_lives)

        fork_collision = arcade.check_for_collision_with_list(
            self.maklowicz_shoes_collider2, self.fork_list)
        if fork_collision:
            self.maklowicz_lives = self.maklowicz.hurt_action(
                self.maklowicz_lives)

        # dill collisions
        dill_collisions = arcade.check_for_collision_with_list(
            self.maklowicz, self.dill_list)
        for picked in dill_collisions:
            self.maklowicz.item_collected = True
            self.dill_list.remove(picked)
            self.collectable_counters['dill'] += 1
            
        # pepper item collision
        pepper_item_collisions = arcade.check_for_collision_with_list(
            self.maklowicz, self.pepper_item_list)
        for picked in pepper_item_collisions:
            self.maklowicz.item_collected = True
            self.pepper_item_list.remove(picked)
            self.collectable_counters['pepper'] += 1

        # SCREEN SCROLLING

        changed_flag = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN - 5
        right_boundary = self.view_left + WINDOW_WIDTH - RIGHT_VIEWPORT_MARGIN + 5
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        map_end_length = self.lvl_map.tile_size[0] * \
            MAP_SCALING*self.lvl_map.map_size[0]

        if self.maklowicz.center_x < left_boundary:
            self.view_left = max(
                self.view_left - left_boundary + self.maklowicz.center_x, 0)
            changed_flag = True
        if self.maklowicz.center_x > right_boundary:
            self.view_left = min(self.view_left - right_boundary +
                                 self.maklowicz.center_x, map_end_length-WINDOW_WIDTH)
            changed_flag = True
        if self.maklowicz.bottom < bottom_boundary:
            self.view_bottom = max(
                self.view_bottom - bottom_boundary + self.maklowicz.center_y, 0)
            changed_flag = True

        if changed_flag:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left, WINDOW_WIDTH + self.view_left,
                                self.view_bottom, WINDOW_HEIGHT + self.view_bottom)

        if self.maklowicz_lives <= 0:
            self.level_end = -1
        if self.level_end == -1:
            #self.window.close()
            print("PRZEGRAŁ HAHAHA!!!")
