import os

from constants.enums import Algorithm
from constants.paths import INPUT_DIR
from core.game import Game
from core.solver import SokobanSolver
from utils import (
    export_output_data,
    get_project_toml_data,
    parse_args,
    with_gui_arg,
    with_version_arg,
)
from utils.generate import generate_output_content


def dev():
    Game().run()


def solve():
    for inp_path, out_path in [
        (
            f"input-{'0' if i < 10 else ''}{i}.txt",
            f"output-{'0' if i < 10 else ''}{i}.txt",
        )
        # for i in [1, 4, 6, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34]
        # for i in [2, 3, 5, 7, 8, 11, 20, 35, 36]
        # for i in [0, 9, 10, 12, 13, 14, 15, 16, 17, 33]
        for i in range(1, 37)
    ]:
        output_data = ""

        for algo, res in (
            SokobanSolver()
            .load_map(os.path.join(INPUT_DIR, inp_path))
            .searching(
                [
                    # Algorithm.BFS,
                    # Algorithm.DFS,
                    # Algorithm.UCS,
                    # Algorithm.DIJKSTRA,
                    # Algorithm.GREEDY,
                    Algorithm.ASTAR,
                    # Algorithm.SWARM,
                    # Algorithm.CONVERGENT_SWARM,
                    # Algorithm.BIDIR_SWARM,
                    # Algorithm.ANT_COLONY,
                ]
            )
        ).items():
            (path, weight, expanded_node, explored_node), time, mem, mem_peak = res

            output_data += (
                generate_output_content(
                    algo,
                    len(path),
                    weight,
                    expanded_node,
                    time,
                    mem_peak,
                    path,
                )
                + "\n"
            )

        export_output_data(output_data, out_path)


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
