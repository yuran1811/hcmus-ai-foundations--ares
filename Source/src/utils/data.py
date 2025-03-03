import os
import re
from dataclasses import dataclass

from constants.paths import DATA_DIR, INPUT_DIR, OUTPUT_DIR

from .base import split_into_chunks


@dataclass
class SolutionType:
    name: str
    steps: int
    weight: int
    node: int
    time: float
    memory: float
    path: str


def extract_data_from_file(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def load_input_data(*, from_index: int = 1, from_filename: str | None = None):
    weights, *map = extract_data_from_file(
        os.path.join(
            DATA_DIR,
            "input",
            from_filename
            if from_filename is not None
            else f"input-{abs(from_index):02}.txt",
        )
    )

    return (
        [int(w) for w in re.split("[\\s\\t]+", weights.strip())],
        "\n".join(map),
    )


def load_output_data(*, from_index: int = 1, from_filename: str | None = None):
    return extract_data_from_file(
        os.path.join(
            DATA_DIR,
            "output",
            from_filename
            if from_filename is not None
            else f"output-{abs(from_index):02}.txt",
        )
    )


def normalize_output_data(raw_data: list[str]):
    data = [d.strip() for d in raw_data]
    algo_sols: list[list[str]] = split_into_chunks(data, 3)

    sols: dict[str, SolutionType] = {}
    for sol in algo_sols:
        name, info, path = sol
        steps, weight, node, time, memory = info.split(", ")

        sols[name] = SolutionType(
            name=name,
            steps=int(steps.split(": ")[1]),
            weight=int(weight.split(": ")[1]),
            node=int(node.split(": ")[1]),
            time=float(time.split(": ")[1].split(" ")[0]),
            memory=float(memory.split(": ")[1].split(" ")[0]),
            path=path,
        )

    return sols


def export_output_data(data: str, filename: str):
    with open(
        os.path.join(DATA_DIR, "output", filename),
        "w",
    ) as file:
        file.write(data)


def get_input_filenames():
    return [f for f in os.listdir(INPUT_DIR) if f.startswith("input-")]


def get_output_filenames():
    return [f for f in os.listdir(OUTPUT_DIR) if f.startswith("output-")]
