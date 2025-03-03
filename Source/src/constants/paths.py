import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# layer 1
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")
DATA_DIR = os.path.join(ROOT_DIR, "data")
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")

# layer 2
FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
IMAGES_PATH = os.path.join(ASSETS_PATH, "images")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")

INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

LOG_DIR = os.path.join(PUBLIC_DIR, "logs")

# layer 3
CHARACTERS_PATH = os.path.join(IMAGES_PATH, "characters")
ITEMS_PATH = os.path.join(IMAGES_PATH, "items")
<<<<<<< HEAD
TILESETS_PATH = os.path.join(IMAGES_PATH, "tilesets")
=======
TILES_PATH = os.path.join(IMAGES_PATH, "tiles")
>>>>>>> 13d1998856ea5592dace2d4413bbda0213d6835d
UI_PATH = os.path.join(IMAGES_PATH, "ui")

BGMS_PATH = os.path.join(SOUNDS_PATH, "bgms")
SOUND_EFFECTS_PATH = os.path.join(SOUNDS_PATH, "effects")

# layer 4
CURSORS_PATH = os.path.join(UI_PATH, "cursors")
