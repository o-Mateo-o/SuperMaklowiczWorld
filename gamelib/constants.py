"""
Constant values defining the static and dynamic game elements.
"""
import arcade

# units
TL = 64
RIGHT_F = 0
LEFT_F = 1

# physics properities
GRAVITY = 1.5
MAKLOWICZ_SPEED = 5
MAKLOWICZ_JUMP_SPEED = 20
CAN_JUMP_DISTANCE = 20

# object actions' properities
POT_ACTION_SPEED = 15
POT_ACTION_HEIGHT = 20
MAKLOWICZ_HEAD_EXTENSION = 10

# window properities
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_HEADING = "Makłowicz Super World"

LEFT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
RIGHT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = WINDOW_HEIGHT/5
TOP_VIEWPORT_MARGIN = WINDOW_HEIGHT/10*3

# object scaling
MAP_SCALING = 1
CHARACTER_SCALING = 1.3

# image source paths
IMG_DIR = "assets\images"
IMG_MAKLOWICZ = {
    'idle': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_idle.png"),
    'jump': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_jump.png"),
    'run1': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run1.png"),
    'run2': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run2.png"),
    'box': arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\BOX_maklowicz_head.png")}

IMG_POT = {
    'picked': arcade.load_texture(f"{IMG_DIR}\\blocks\pot_picked.png")}





# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
TEST_MAP = arcade.tilemap.read_tmx("assets\maps\level_test.tmx")
TEST_BLOCK_LAYER = "layer"
