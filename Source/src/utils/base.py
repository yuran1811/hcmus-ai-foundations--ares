def split_into_chunks(arr: list, chunk_size: int):
    return [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
