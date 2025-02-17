def generate_output_content(
    algo, num_steps, tot_weight, num_nodes, search_time, mem_used, action_seq
):
    return f"""{algo}
Steps: {num_steps}, Weight: {tot_weight}, Node: {num_nodes}, Time (ms): {search_time}, Memory (MB): {mem_used}
{action_seq}
"""
