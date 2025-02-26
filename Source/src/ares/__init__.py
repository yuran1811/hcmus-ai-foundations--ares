import os

from constants.paths import INPUT_DIR
from core.game import Game
from core.solver import SokobanSolver
from utils import (
    byte_convert,
    generate_output_content,
    get_project_toml_data,
    parse_args,
    with_gui_arg,
    with_version_arg,
)


def dev():
    Game().run()


def solve():
    for algo, res in (
        SokobanSolver().load_map(os.path.join(INPUT_DIR, "input-01.txt")).searching()
    ).items():
        (path, weight, expanded_node, explored_node), time, mem, mem_peak = res
        print(
            generate_output_content(
                algo,
                len(path),
                weight,
                expanded_node,
                time,
                byte_convert(mem_peak),
                path,
            )
        )


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
