def generate_output_content(
    algo: str,
    num_steps: int,
    tot_weight: int,
    num_nodes: int,
    search_time: float,
    mem_used: str,
    action_seq: str,
):
    return f"{algo}\nSteps: {num_steps}, Weight: {tot_weight}, Node: {num_nodes}, Time (ms): {search_time}, Memory: {mem_used}\n{action_seq}"
