from argparse import ArgumentParser


def with_version_arg(parser: ArgumentParser):
    parser.add_argument("-v", "--version", help="Version", action="store_true")


def with_gui_arg(parser: ArgumentParser):
    parser.add_argument("--gui", help="gui", action="store_true")


def parse_args(*, prog: str, desc: str, wrappers: list):
    parser = ArgumentParser(
        prog=prog,
        description=desc,
    )

    for wrapper in wrappers:
        wrapper(parser)

    return parser.parse_args()
