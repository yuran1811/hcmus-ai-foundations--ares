import os

from constants.paths import ROOT_DIR
from utils.asset_loader import (
    get_asset_path,
)
from utils.base import byte_convert, split_into_chunks
from utils.config import (
    get_speed,
    get_speed_cycle,
)
from utils.data import (
    get_input_filenames,
    get_output_filenames,
    load_input_data,
)
from utils.generate import generate_output_content


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


def test_byte_convert():
    assert byte_convert(1) == "1.00 B"
    assert byte_convert(1024) == "1.00 KB"
    assert byte_convert(1024**2) == "1.00 MB"
    assert byte_convert(1024**3) == "1.00 GB"
    assert byte_convert(1024**4) == "1.00 TB"
    assert byte_convert(1024**5) == "1.00 PB"
    assert byte_convert(1024**6) == "1024.00 PB"


def test_split_into_chunks():
    assert split_into_chunks("uLulDrrRRRRRRurD", 3) == [
        "uLu",
        "lDr",
        "rRR",
        "RRR",
        "Rur",
        "D",
    ]
    assert split_into_chunks(("uLulDrrRRRRRRurD"), 4) == [
        "uLul",
        "DrrR",
        "RRRR",
        "RurD",
    ]


def test_get_speed():
    assert get_speed(1, False) == 1
    assert get_speed(16, True) == 16
    assert get_speed_cycle(1, False) == 16
    assert get_speed_cycle(16, True) == 1

    assert get_speed(1, True) == 2
    assert get_speed(16, False) == 8


def test_io_filenames():
    assert get_input_filenames() == [f"input-{x:02}.txt" for x in range(0, 37)]
    assert get_output_filenames() == [f"output-{x:02}.txt" for x in range(0, 37)]


def test_load_input_data():
    assert load_input_data(from_index=1) == (
        [1, 99],
        " ###########\n\n##         #\n\n#          #\n\n# $ $      #\n\n#. @      .#\n\n############",
    )
    assert load_input_data(from_index=0, from_filename="input-01.txt") == (
        [1, 99],
        " ###########\n\n##         #\n\n#          #\n\n# $ $      #\n\n#. @      .#\n\n############",
    )


def test_generate_output_content():
    assert (
        generate_output_content(
            "BFS", 16, 695, 4321, 0.05812, 13170114, "uLulDrrRRRRRRurD"
        )
        == "BFS\nSteps: 16, Weight: 695, Node: 4321, Time: 58.12 ms, Memory: 12.56 MB\nuLulDrrRRRRRRurD"
    )
