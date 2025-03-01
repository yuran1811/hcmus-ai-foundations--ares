from .base import byte_convert, time_convert


def generate_output_content(
    algo: str,
    num_steps: int,
    tot_weight: int,
    num_nodes: int,
    search_time: float,
    mem_used: int,
    action_seq: str,
):
    return f"{algo}\nSteps: {num_steps}, Weight: {tot_weight}, Node: {num_nodes}, Time: {time_convert(search_time)}, Memory: {byte_convert(mem_used)}\n{action_seq}"
