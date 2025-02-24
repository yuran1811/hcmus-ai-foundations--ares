import os

from constants.paths import ROOT_DIR
from utils import (
    generate_output_content,
    get_asset_path,
    get_input_filenames,
    get_output_filenames,
    get_speed,
    load_input_data,
)
from utils.config import get_speed_cycle


def test_generate_output_content():
    assert (
        generate_output_content("BFS", 16, 695, 4321, 58.12, 12.56, "uLulDrrRRRRRRurD")
        == "BFS\nSteps: 16, Weight: 695, Node: 4321, Time (ms): 58.12, Memory (MB): 12.56\nuLulDrrRRRRRRurD"
    )


def test_get_asset_path():
    assert get_asset_path("images", "ui", "cursors") == os.path.join(
        ROOT_DIR, "assets", "images", "ui", "cursors"
    )
    assert get_asset_path(
        "fonts", "Pixelify_Sans", "static", "PixelifySans-Regular.ttf"
    ) == os.path.join(
        ROOT_DIR,
        "assets",
        "fonts",
        "Pixelify_Sans",
        "static",
        "PixelifySans-Regular.ttf",
    )


def test_io_filenames():
    assert get_input_filenames() == [f"input-{x:02}.txt" for x in range(0, 36)]
    assert get_output_filenames() == [f"output-{x:02}.txt" for x in range(0, 36)]


def test_get_speed():
    assert get_speed(1, False) == 1
    assert get_speed(16, True) == 16
    assert get_speed_cycle(1, False) == 16
    assert get_speed_cycle(16, True) == 1

    assert get_speed(1, True) == 2
    assert get_speed(16, False) == 8


def test_load_input_data():
    assert load_input_data(from_index=1) == (
        [1, 99],
        " ###########\n\n##         #\n\n#          #\n\n# $ $      #\n\n#. @      .#\n\n############",
    )
    assert load_input_data(from_index=0, from_filename="input-01.txt") == (
        [1, 99],
        " ###########\n\n##         #\n\n#          #\n\n# $ $      #\n\n#. @      .#\n\n############",
    )
