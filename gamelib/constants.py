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


# window properities
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_HEADING = "Makłowicz Super World"

LEFT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
RIGHT_VIEWPORT_MARGIN = WINDOW_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = WINDOW_HEIGHT/5
TOP_VIEWPORT_MARGIN = WINDOW_HEIGHT/10*3

# object scaling
BLOCK_SCALING = 1
CHARACTER_SCALING = 1.3

# image source paths
IMG_DIR = "assets\images"
IMG_MAKLOWICZ_IDLE = arcade.load_texture_pair(
    f"{IMG_DIR}\maklowicz\maklowicz_idle.png")
IMG_MAKLOWICZ_JUMP = arcade.load_texture_pair(
    f"{IMG_DIR}\maklowicz\maklowicz_jump.png")
IMG_MAKLOWICZ_RUN = [arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run1.png"),
                     arcade.load_texture_pair(f"{IMG_DIR}\maklowicz\maklowicz_run2.png")]


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
TEST_MAP = "assets\maps\level_test.tmx"
TEST_BLOCK_LAYER = "layer"
