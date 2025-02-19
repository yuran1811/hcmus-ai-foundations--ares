def generate_output_content(
    algo: str,
    num_steps: int,
    tot_weight: int,
    num_nodes: int,
    search_time: float,
    mem_used: float,
    action_seq: str,
):
    return f"""{algo}
Steps: {num_steps}, Weight: {tot_weight}, Node: {num_nodes}, Time (ms): {search_time}, Memory (MB): {mem_used}
{action_seq}
"""
