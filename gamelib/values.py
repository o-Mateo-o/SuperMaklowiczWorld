"""
Constant values defining the static and dynamic game elements.
"""
import arcade

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

PYMUNK_GRAVITY = -GRAVITY * 1000
PYMUNK_DAMP = 0.1
POPPING_X_FORCE_RANGE_LIMIT = 1000
POPPING_Y_FORCE = 20000

# object actions' properities
POT_ACTION_SPEED = 15
POT_ACTION_HEIGHT = 20
MAKLOWICZ_HEAD_EXTENSION = 10

DILL_DROP = 2

# window properities
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
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
    'box': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\BOX_maklowicz_head.png")}

image_pot = {
    'picked': arcade.load_texture(f"{IMG_DIR}\\blocks\pot_picked.png")}

image_collectable = {
    'dill': arcade.load_texture(f"{IMG_DIR}\\blocks\dill.png")}

image_hearts = {
    3: arcade.load_texture(f"{IMG_DIR}\\widget\hearts\hearts3.png")}

# sounds
SND_DIR = "assets\sounds"
sounds_roberto = {
    'hihihi': arcade.Sound(f"{SND_DIR}\\roberto\hihihi.ogg")}
sound_pepper = {
    'papryka': arcade.Sound(f"{SND_DIR}\\pepper\papryka.ogg"),
    'papryczka': arcade.Sound(f"{SND_DIR}\\pepper\papryczka.ogg"),
    'papryke': arcade.Sound(f"{SND_DIR}\\pepper\papryke.ogg"),
    'paprykowo': arcade.Sound(f"{SND_DIR}\\pepper\paprykowo.ogg")}
sound_environ = {
    'running': arcade.Sound(f"{SND_DIR}\\environment\\running.ogg")}

# sound volumes
sound_volume_factor = 1
standard_sound_volume = 1 * sound_volume_factor
step_volume = 0.5 * sound_volume_factor

# font paths
COMIC_SANS_FONT = "assets\\fonts\ComicSans.ttf"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
TEST_MAP = arcade.tilemap.read_tmx("assets\maps\level_test.tmx")
TEST_BLOCK_LAYER = "layer"
