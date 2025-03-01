from core.game import Game
from utils import (
    get_project_toml_data,
    parse_args,
    with_gui_arg,
    with_version_arg,
)


def dev():
    Game().run()


def solve():
    pass


def main() -> int:
    __toml = get_project_toml_data()

    args = parse_args(
        prog=__toml["name"],
        desc=__toml["description"],
        wrappers=[with_version_arg, with_gui_arg],
    )

    if args.version:
        print(
            f"{__toml['name']} {__toml['version']} -- by {', '.join([x['name'] for x in __toml['authors']])} -- {__toml['license']['text']} LICENSE"
        )
        return 0

    if args.gui:
        Game().run()

    return 0
