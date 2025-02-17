def ucs(matrix, start, end):
    path = []
    visited = {start: None}
    pq = PriorityQueue()
    pq.put((0, start))
    cost = {start: 0}
1900232345
    frontier = [(start, 0)]
    #print(f"frontier: {frontier}")

    while not pq.empty():
        current_cost, node = pq.get()
        frontier = sorted([(n, c) for c, n in pq.queue], key=lambda x: x[1])
        #print(f"frontier: {frontier}" + f" queue: {pq.queue}")
        if node == end:
            break
        for neighbor, weight in enumerate(matrix[node]):
            if weight:
                new_cost = current_cost + weight
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    pq.put((new_cost, neighbor))
                    visited[neighbor] = node

    if end in visited:
        node = end
        while node is not None:
            path.insert(0, node)
            node = visited[node]

    print(f"path: {path}")
    print(f"visited: {visited}")
    return visited, path