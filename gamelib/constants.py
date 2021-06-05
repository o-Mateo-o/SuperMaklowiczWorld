"""
Constant values defining the static and dynamic game elements.
"""

import arcade

STANDARD_CONTROLL_KEYSET = {'jump': False, 'left': False, 'right': False}

# object scaling
MAP_SCALING = 0.7
SCORE_SCALING = 1
CHARACTER_SCALING = 0.8

# units
TL = 64 * MAP_SCALING
RIGHT_F = 0
LEFT_F = 1

# physics properities
GRAVITY = 1.5
MAKLOWICZ_SPEED = 5
MAKLOWICZ_JUMP_SPEED = 20
CAN_JUMP_DISTANCE = 20
MAKLOWICZ_IMMUNITY_TIME = 30
MAKLOWICZ_KICKBACK = 100

PEPPER_SPEED = 2
PEPPER_JUMP_SPEED = 7
PEPPER_AGONY_TIME = 30

MOVING_BLOCK_SPEED = 2

KNIVES_DISLOCATION = 10

PYMUNK_GRAVITY = -GRAVITY * 1000
PYMUNK_DAMP = 0.1
POPPING_X_FORCE_RANGE_LIMIT = 1000
POPPING_Y_FORCE = 20000

# object actions' properities
POT_ACTION_SPEED = 15
POT_ACTION_HEIGHT = 20
MAKLOWICZ_HEAD_EXTENSION = 10
MAKLOWICZ_SHOES_EXTENSION = -30
MAKLOWICZ_SHOES_EXTENSION_ITEMS = -10

LIVES_NUMBER = 3

DILL_DROP = 2

FINAL_TIME = 80

# window properities
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
WINDOW_HEADING = "Makłowicz Super World"

LEFT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
RIGHT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = WINDOW_HEIGHT/3



# images
IMG_DIR = "assets\images"
image_maklowicz = {
    'idle': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_idle.png"),
    'jump': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_jump.png"),
    'run1': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run1.png"),
    'run2': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run2.png"),
    'box_h': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\BOX_maklowicz_head.png"),
    'box_s': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\BOX_maklowicz_shoes.png"),
    'dead': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_dead.png")}

image_pepper_enemy = {
    'live1': arcade.load_texture_pair(f"{IMG_DIR}\pepper\pepper_enemy1.png"),
    'live2': arcade.load_texture_pair(f"{IMG_DIR}\pepper\pepper_enemy2.png"),
    'live3': arcade.load_texture_pair(f"{IMG_DIR}\pepper\pepper_enemy3.png"),
    'killed': arcade.load_texture_pair(f"{IMG_DIR}\pepper\pepper_enemy_killed.png")}

image_pot = {
    'picked': arcade.load_texture(f"{IMG_DIR}\\blocks\pot_picked.png")}

image_collectable = {
    'dill': arcade.load_texture(f"{IMG_DIR}\\blocks\dill.png"),
    'pepper': arcade.load_texture(f"{IMG_DIR}\pepper\pepper_item.png")}

image_hearts = {
    3: arcade.load_texture(f"{IMG_DIR}\\widget\hearts\hearts3.png"),
    2: arcade.load_texture(f"{IMG_DIR}\\widget\hearts\hearts2.png"),
    1: arcade.load_texture(f"{IMG_DIR}\\widget\hearts\hearts1.png"),
    0: arcade.load_texture(f"{IMG_DIR}\\widget\hearts\hearts0.png")}

image_gui = {
    'board': arcade.load_texture(f"{IMG_DIR}\\widget\\board.png"),
    'full_false_0': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_false_0.png"),
    'full_false_1': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_false_1.png"),
    'full_false_2': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_false_2.png"),
    'full_true_0': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_true_0.png"),
    'full_true_1': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_true_1.png"),
    'full_true_2': arcade.load_texture(f"{IMG_DIR}\\widget\\button_full_true_2.png"),
    'quit_0': arcade.load_texture(f"{IMG_DIR}\\widget\\button_quit_0.png"),
    'quit_1': arcade.load_texture(f"{IMG_DIR}\\widget\\button_quit_1.png"),
    'quit_2': arcade.load_texture(f"{IMG_DIR}\\widget\\button_quit_2.png"),
    'start_0': arcade.load_texture(f"{IMG_DIR}\\widget\\button_start_0.png"),
    'start_1': arcade.load_texture(f"{IMG_DIR}\\widget\\button_start_1.png"),
    'start_2': arcade.load_texture(f"{IMG_DIR}\\widget\\button_start_2.png"),
    'std_0': arcade.load_texture(f"{IMG_DIR}\\widget\\button_std_0.png"),
    'std_1': arcade.load_texture(f"{IMG_DIR}\\widget\\button_std_1.png"),
    'std_2': arcade.load_texture(f"{IMG_DIR}\\widget\\button_std_2.png"),
    't_start': arcade.load_texture(f"{IMG_DIR}\\widget\\label_start.png"),
    't_scores': arcade.load_texture(f"{IMG_DIR}\\widget\\label_scores.png"),
    't_options': arcade.load_texture(f"{IMG_DIR}\\widget\\label_options.png"),
    't_controls': arcade.load_texture(f"{IMG_DIR}\\widget\\label_controls.png"),
    't_about': arcade.load_texture(f"{IMG_DIR}\\widget\\label_about.png")
    }

image_background = {
    1: arcade.load_texture(f"{IMG_DIR}\\bg.jpg")}

# sounds
SND_DIR = "assets\sounds"
sounds_roberto = {
    'hihihi': arcade.Sound(f"{SND_DIR}\\roberto\hihihi.ogg"),
    'oaa': arcade.Sound(f"{SND_DIR}\\roberto\oaa.ogg")}
sound_pepper = {
    'papryka': arcade.Sound(f"{SND_DIR}\\pepper\papryka.ogg"),
    'papryczka': arcade.Sound(f"{SND_DIR}\\pepper\papryczka.ogg"),
    'papryke': arcade.Sound(f"{SND_DIR}\\pepper\papryke.ogg"),
    'paprykowo': arcade.Sound(f"{SND_DIR}\\pepper\paprykowo.ogg")}
sound_environ = {
    'running': arcade.Sound(f"{SND_DIR}\\environment\\running.ogg"),
    'pot': arcade.Sound(f"{SND_DIR}\\environment\\pot.ogg"),
    'loose': arcade.Sound(f"{SND_DIR}\\environment\\jasnygwint.ogg")}



# font paths
COMIC_SANS_FONT = "assets\\fonts\ComicSans.ttf"

# map layers
MAP_LAYER = {'terrain1': "layer", 'pots': "obj", 'dill': "dill",
             'pepper_enemy': "pepper", 'limits': "limits", 'knives': "knives",
             'forks': "forks", 'terrain2': "nonc", 'win': "win", 'terrain0': "bg",
             'mterrain': "moving"}


# maps
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
TEST_MAP = arcade.tilemap.read_tmx("assets\maps\level_test.tmx")
TEST_BLOCK_LAYER = "layer"
