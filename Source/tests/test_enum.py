from constants import Direction, GridItem


def test_get_char():
    assert GridItem.get_char(GridItem.WALL) == "#"
    assert GridItem.get_char(GridItem.EMPTY) == " "
    assert GridItem.get_char(GridItem.STONE) == "$"
    assert GridItem.get_char(GridItem.ARES) == "@"
    assert GridItem.get_char(GridItem.SWITCH) == "."
    assert GridItem.get_char(GridItem.STONE_ON_SWITCH) == "*"
    assert GridItem.get_char(GridItem.ARES_ON_SWITCH) == "+"


def test_convert_char():
    assert GridItem.convert_char("#") == 0
    assert GridItem.convert_char(" ") == 1
    assert GridItem.convert_char("$") == 2
    assert GridItem.convert_char("@") == 3
    assert GridItem.convert_char(".") == 4
    assert GridItem.convert_char("*") == 5
    assert GridItem.convert_char("+") == 6


def test_pushing_dir():
    assert Direction.get_pushing(Direction.UP) == "U"
    assert Direction.get_pushing(Direction.DOWN) == "D"
    assert Direction.get_pushing(Direction.LEFT) == "L"
    assert Direction.get_pushing(Direction.RIGHT) == "R"
