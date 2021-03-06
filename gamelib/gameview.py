"""
Main game view module to handle all the actions in the gameplay and display it.
"""


import random
import sys

import arcade

from gamelib import auxfunctions, ongameviews, physics, sprites, widgets
from gamelib.constants import *

sys.path.append(".")


class GameLevel(arcade.View):
    """
    Level class. Prepare a level, handle all the events in the game and display it.
    """

    def __init__(self):
        """
        Create an arcade view. Prepare blank attributes and pause sounds.
        """
        super().__init__()
        # pause previous sounds
        for player in self.window.sound_player_register.values():
            player.pause()
        # keys handled and projection properities
        self.c_keys_pressed_gny = STANDARD_CONTROLL_KEYSET.copy()
        self.view_bottom = 0
        self.view_left = 0
        self.hurt_warn_counter = 0
        self.mouse_button_colliding = False

        # counters
        self.level_end = None
        self.level_ended_action = None
        self.maklowicz_lives = None
        self.collectable_counters = None
        self.final_time_counter = None

        # sprites
        self.character_cont_list = None
        self.bg_block_list = None
        self.block_list = None
        self.noncoll_block_list = None
        self.win_block_list = None
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

        self.last_ch_view = None
        self.reshow = False
        self.paused = False
        self.button_list = None

        # map
        self.lvl_map = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def pause(self):
        """
        Pause the game and show a pause view.
        """
        pause = ongameviews.PauseView(self)
        pause.setup()
        self.window.show_view(pause)

    def setup(self):
        """
        Prepare the objects on the map, set the game physics and properities -
                        according to the chosen level number and difficulty.
        """
        if self.window.difficulty == 'normal':
            self.window.fork_speed = D_FORK_SPEED
            self.window.pepper_speed = D_PEPPER_SPEED
            self.window.moving_block_speed = D_MOVING_BLOCK_SPEED
        else:
            self.window.fork_speed = D_FORK_SPEED * SPICY_RATIO
            self.window.pepper_speed = D_PEPPER_SPEED * SPICY_RATIO
            self.window.moving_block_speed = D_MOVING_BLOCK_SPEED * SPICY_RATIO

        self.button_list = []
        self.mouse_button_colliding = True
        self.mouse_pressed = False
        self.current_button = None
        self.click = False
        self.unclick = False
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.mouse = self.mouse = arcade.SpriteCircle(1, arcade.csscolor.BLACK)

        # counters
        self.level_end = 0  # 0 - not finished yet; 1 - won; -1 - lost
        self.level_ended_action = False
        self.maklowicz_lives = LIVES_NUMBER
        self.collectable_counters = {'dill': 0, 'pepper': 0}
        self.final_time_counter = 0

        # sprite empty lists
        self.character_cont_list = arcade.SpriteList()
        self.bg_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.block_list = arcade.SpriteList(use_spatial_hash=True)
        self.noncoll_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.win_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.limit_list = arcade.SpriteList(use_spatial_hash=True)
        self.pots_picked = set()
        self.dill_list = arcade.SpriteList()
        self.pepper_enemy_list = arcade.SpriteList()
        self.pepper_item_list = arcade.SpriteList()

        # main character and head-box
        self.maklowicz = sprites.Maklowicz(self, 4*TL, 7*TL)
        self.maklowicz_head_collider = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x,
            center_y=self.maklowicz.center_y)
        self.maklowicz_shoes_collider = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x,
            center_y=self.maklowicz.center_y)
        self.maklowicz_shoes_collider2 = arcade.Sprite(
            scale=CHARACTER_SCALING, center_x=self.maklowicz.center_x,
            center_y=self.maklowicz.center_y)
        self.maklowicz_head_collider.texture = image_maklowicz['box_h'][0]
        self.maklowicz_shoes_collider.texture = image_maklowicz['box_s'][0]
        self.maklowicz_shoes_collider2.texture = image_maklowicz['box_s'][0]

        self.character_cont_list.append(self.maklowicz)
        self.character_cont_list.append(self.maklowicz_head_collider)
        self.character_cont_list.append(self.maklowicz_shoes_collider)
        self.character_cont_list.append(self.maklowicz_shoes_collider2)

        # map static
        self.lvl_map = LEVEL_MAPS[self.window.current_level]

        self.bg_block_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                          layer_name=MAP_LAYER['terrain0'],
                                                          scaling=MAP_SCALING,
                                                          use_spatial_hash=True)
        self.block_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                       layer_name=MAP_LAYER['terrain1'],
                                                       scaling=MAP_SCALING,
                                                       use_spatial_hash=True)
        self.noncoll_block_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                               layer_name=MAP_LAYER['terrain2'],
                                                               scaling=MAP_SCALING,
                                                               use_spatial_hash=True)
        self.win_block_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                           layer_name=MAP_LAYER['win'],
                                                           scaling=MAP_SCALING,
                                                           use_spatial_hash=True)
        self.limit_list = arcade.tilemap.process_layer(map_object=self.lvl_map,
                                                       layer_name=MAP_LAYER['limits'],
                                                       scaling=MAP_SCALING,
                                                       use_spatial_hash=True)

        # map objects
        self.pot_sublist = auxfunctions.init_objects_from_map(sprites.Pot, self,
                                                              self.block_list, self.lvl_map,
                                                              MAP_LAYER['pots'], True)
        self.moving_block_sublist = auxfunctions.init_objects_from_map(sprites.MovingBlockSimple,
                                                                       self, self.block_list, self.lvl_map,
                                                                       MAP_LAYER['mterrain'], True,
                                                                       self.window.moving_block_speed)
        self.dill_list = auxfunctions.init_objects_from_map(sprites.Dill, self, self.dill_list, self.lvl_map,
                                                            MAP_LAYER['dill'], False)
        self.pepper_enemy_list = auxfunctions.init_objects_from_map(sprites.PepperEnemy, self,
                                                                    self.pepper_enemy_list,
                                                                    self.lvl_map, MAP_LAYER['pepper_enemy'],
                                                                    False, self.window.pepper_speed)
        self.knives_list = auxfunctions.init_objects_from_map(sprites.Knives, self, self.block_list,
                                                              self.lvl_map, MAP_LAYER['knives'], True)
        self.fork_list = auxfunctions.init_objects_from_map(sprites.Fork, self, self.block_list,
                                                            self.lvl_map, MAP_LAYER['forks'], False,
                                                            self.window.fork_speed)
        for knives in self.knives_list:
            knives.initial_move()
        for fork in self.fork_list:
            fork.adjust_hitbox()

        # pause button add
        self.button_pause = widgets.StandardButton(
            self, 10,
            center_x=self.width * 0.93,
            center_y=self.height * 0.9,
            normal_texture=image_gui['pause_0'],
            hover_texture=image_gui['pause_1'],
            press_texture=image_gui['pause_2'],
            callback=lambda: self.pause()
        )
        self.button_list.append(self.button_pause)

        # physic engines
        self.pepper_physics_engines = []
        self.physics_engine_maklowicz = arcade.PhysicsEnginePlatformer(self.maklowicz,
                                                                       self.block_list,
                                                                       GRAVITY)
        for papryka in self.pepper_enemy_list:
            self.pepper_physics_engines.append(
                physics.PhysicsEngineEnemy(papryka, self.block_list, GRAVITY))

        self.physics_engine_pymunk = arcade.PymunkPhysicsEngine(
            (0, PYMUNK_GRAVITY), PYMUNK_DAMP)

        # add objects to engines
        self.maklowicz.physics_engines.append(self.physics_engine_maklowicz)

        self.physics_engine_pymunk.add_sprite_list(
            self.block_list, body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine_pymunk.add_sprite_list(self.dill_list)
        self.physics_engine_pymunk.add_sprite_list(self.pepper_item_list)

    def on_key_press(self, key, modifiers):
        """
        Handle the key press events - 'AWD' or '<^> arrows' and 'ESC' allowed.
        Use them to move and pause.
        Send the movement info to character class.
        :param key: pressed key
        :param modifiers: key modifiers
        """
        if key in [arcade.key.W, arcade.key.UP]:
            self.c_keys_pressed_gny['jump'] = True
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.c_keys_pressed_gny['left'] = True
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.c_keys_pressed_gny['right'] = True
        elif key == arcade.key.ESCAPE and self.level_end == 0:
            self.pause()

        if self.level_end == 0:
            self.maklowicz.process_keychange(self.c_keys_pressed_gny)

    def on_key_release(self, key, modifiers):
        """
        Handle the key release events - 'AWD' or '<^> arrows'.
        Use them to move.
        Send the movement info to character class.
        :param key: released key
        :param modifiers: key modifiers
        """
        if key in [arcade.key.W, arcade.key.UP]:
            self.c_keys_pressed_gny['jump'] = False
        elif key in [arcade.key.A, arcade.key.LEFT]:
            self.c_keys_pressed_gny['left'] = False
        elif key in [arcade.key.D, arcade.key.RIGHT]:
            self.c_keys_pressed_gny['right'] = False

        if self.level_end == 0:
            self.maklowicz.process_keychange(self.c_keys_pressed_gny)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Handle the mouse motion events.
        Used ther only to click the pause button.
        Send the proper info to the button.
        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        if not self.window.fullscreen:
            ratio_x = self.width/WINDOW_WIDTH
            ratio_y = self.height/WINDOW_HEIGHT
        else:
            ratio_x = self.width/self.window.width
            ratio_y = self.height/self.window.height
        self.mouse.center_x = x * ratio_x + self.view_left
        self.mouse.center_y = y * ratio_y + self.view_bottom
        self.mouse_button_colliding = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Set the attributes to the conditions of a pressed mouse.
        :param float x: x position of the mouse
        :param float y: y position of the mouse
        :param int button: What button was hit. One of:
                           arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT,
                           arcade.MOUSE_BUTTON_MIDDLE
        :param int modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock)
                              pressed during this event. See :ref:`keyboard_modifiers`.
        """
        self.mouse_pressed = True
        self.click = True

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Set the attributes to the conditions of a released mouse.

        :param float x:
        :param float y:
        :param int button:
        :param int modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock)
                              pressed during this event. See :ref:`keyboard_modifiers`.
        """
        self.mouse_pressed = False
        self.unclick = True

    def on_show(self):
        """Called when this view is shown and if window dispatches a on_show event.
        (first time showing window or resize).
        Set also the mous properities for that moment.
        """
        super().on_show()
        self.mouse_button_colliding = False

    def on_draw(self):
        """
        Draw all the objects on the screen.
        """
        arcade.start_render()

        # background
        map_end_length_x = self.lvl_map.tile_size[0] * \
            MAP_SCALING*self.lvl_map.map_size[0]
        map_end_length_y = self.lvl_map.tile_size[1] * \
            MAP_SCALING*self.lvl_map.map_size[1]
        addit_x = WINDOW_WIDTH + self.window.bg_move_x_extension
        addit_y = WINDOW_HEIGHT + self.window.bg_move_y_extension
        bg_center_x = WINDOW_WIDTH / 2 + self.view_left * \
            (1 - (addit_x / (map_end_length_x + self.view_left)))
        bg_center_y = WINDOW_HEIGHT / 2 + self.view_bottom * \
            (1 - (addit_y / (map_end_length_y + self.view_bottom)))
        arcade.draw_texture_rectangle(bg_center_x, bg_center_y, WINDOW_WIDTH + addit_x,
                                      WINDOW_HEIGHT + addit_y, image_background[1])

        # object lists
        self.block_list.draw()
        self.bg_block_list.draw()
        self.maklowicz.draw()
        self.dill_list.draw()
        self.pepper_enemy_list.draw()
        self.pepper_item_list.draw()
        self.noncoll_block_list.draw()

        # current score info
        scores_place_x = self.view_left
        scores_place_y = self.view_bottom + WINDOW_HEIGHT
        arcade.draw_texture_rectangle(scores_place_x + 3*TL//2 + 10, scores_place_y - TL//2,
                                      3*TL*SCORE_SCALING, TL*SCORE_SCALING,
                                      image_hearts[self.maklowicz_lives])
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

        for button in self.button_list:
            button.center_x = button.init_center_x + self.view_left
            button.center_y = button.init_center_y + self.view_bottom
            button.draw()

        # hurt warning on screen
        if self.maklowicz.hurt:
            self.hurt_warn_counter += 1
        if self.hurt_warn_counter > 0:
            self.hurt_warn_counter += 1
        if self.hurt_warn_counter > 8:
            self.hurt_warn_counter = 0
        if self.hurt_warn_counter != 0:
            arcade.draw_rectangle_filled(self.view_left+WINDOW_WIDTH/2, self.view_bottom+WINDOW_HEIGHT/2,
                                         WINDOW_WIDTH, WINDOW_HEIGHT, (255, 0, 0, 50))

    def on_update(self, delta_time):
        """
        Handle the events in the game depending on the current conditions - collisions,
                         textures, audio, game state and so on.
        :param float delta_time: Time interval since the last time the function was called.
        """
        if self.reshow and self.last_ch_view:
            self.window.show_view(self.last_ch_view)
            self.reshow = False

        # mouse
        current_button_set = False
        for button in self.button_list:
            if arcade.check_for_collision(self.mouse, button) and self.mouse_button_colliding:
                if not current_button_set:
                    self.current_button = button
                    current_button_set = True
                if self.click:
                    button.clicked = True
                if self.mouse_pressed and button.clicked and button == self.current_button\
                        and self.level_end == 0:
                    button.texture_change(2)

                elif not self.mouse_pressed and button == self.current_button:
                    button.texture_change(1)
                else:
                    button.texture_change(0)
                if self.unclick and self.level_end == 0:
                    button.on_click()

            else:
                button.clicked = False
                button.texture_change(0)
        self.click = False
        self.unclick = False

        # UPDATE ONLY IF THE GAME IS NOT PAUSED
        if not self.paused:
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

            # winning place
            if arcade.check_for_collision_with_list(self.maklowicz, self.win_block_list):
                self.maklowicz.change_x = 0
                self.maklowicz.change_y = 0
                self.level_end = 1

            # pots collisions and action
            self.pots_picked.update(set(arcade.check_for_collision_with_list(
                self.maklowicz_head_collider, self.pot_sublist)))

            for pot in self.pots_picked:
                if pot.active:
                    if not pot.picked:
                        for _ in range(0, DILL_DROP):
                            new_dill = sprites.Dill(self, pot)
                            self.dill_list.append(new_dill)
                            self.physics_engine_pymunk.add_sprite(
                                new_dill, friction=1, collision_type="item")
                            self.physics_engine_pymunk.apply_force(new_dill, (random.randint(
                                -POPPING_X_FORCE_RANGE_LIMIT, POPPING_X_FORCE_RANGE_LIMIT), POPPING_Y_FORCE))
                    pot.pick_action()

            # moving block bounce
            for block in self.moving_block_sublist:
                if arcade.check_for_collision_with_list(block, self.limit_list):
                    block.change_x = -block.change_x

            # pepper enemy collsisions
            for pepper in self.pepper_enemy_list:
                if pepper.transform_to_item:
                    new_pepper = sprites.PepperItem(self, pepper)
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
                # hurt maklowicz
                if arcade.check_for_collision(self.maklowicz, pepper) and not pepper.killed\
                        and self.level_end == 0:
                    self.maklowicz_lives = self.maklowicz.hurt_action(
                        self.maklowicz_lives)

            # knives and forks collision
            knives_collision = arcade.check_for_collision_with_list(
                self.maklowicz_shoes_collider2, self.knives_list)
            if knives_collision and self.level_end == 0:
                self.maklowicz_lives = self.maklowicz.hurt_action(
                    self.maklowicz_lives)

            fork_collision = arcade.check_for_collision_with_list(
                self.maklowicz_shoes_collider2, self.fork_list)
            if fork_collision and self.level_end == 0:
                self.maklowicz_lives = self.maklowicz.hurt_action(
                    self.maklowicz_lives)

            # dill collisions
            dill_collisions = arcade.check_for_collision_with_list(
                self.maklowicz, self.dill_list)
            for picked in dill_collisions:
                if self.level_end == 0:
                    self.maklowicz.item_collected = True
                    self.dill_list.remove(picked)
                    self.collectable_counters['dill'] += 1

            # pepper item collision
            pepper_item_collisions = arcade.check_for_collision_with_list(
                self.maklowicz, self.pepper_item_list)
            for picked in pepper_item_collisions:
                if self.level_end == 0:
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

            # underground bug "fix"
            height_pump = 1
            while self.maklowicz.center_y < 0:
                self.maklowicz.center_y += height_pump * TL
                height_pump += 1

            # when level finished

            if self.maklowicz_lives <= 0:
                self.level_end = -1
                self.maklowicz.dead = True
                self.maklowicz.change_x = 0
                self.maklowicz.change_y = 0

            if self.level_end != 0:
                self.final_time_counter += 1

            if not self.level_ended_action and self.final_time_counter > FINAL_TIME:

                if self.level_end == -1:
                    new_view = ongameviews.GameOverView(self)
                if self.level_end == 1:
                    new_view = ongameviews.WinningView(self)
                new_view.setup()
                self.window.show_view(new_view)

                self.level_ended_action = True
