def astar(matrix, start, end, pos):
    path = []
    visited = {start: None}
    pq = PriorityQueue()
    pq.put((0, start))
    cost = {start: 0}

    frontier = [(start, 0)]
    #print(f"frontier: {frontier}")

    while not pq.empty():
        current_cost, node = pq.get()
        # frontier = sorted([(n, c) for c, n in pq.queue], key=lambda x: x[1])
        #print(f"frontier: {frontier}")
        if node == end:
            break
        for neighbor, weight in enumerate(matrix[node]):
            if weight:
                new_cost = cost[node] + weight
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end, pos)
                    pq.put((priority, neighbor))
                    visited[neighbor] = node
        frontier = sorted([(n, c) for c, n in pq.queue], key=lambda x: x[1])

    if end in visited:
        node = end
        while node is not None:
            path.insert(0, node)
            node = visited[node]

    print(f"path: {path}")
    print(f"visited: {visited}")
    return visited, path

def heuristic(node, end, pos):
    # Euclidean distance as heuristic
    x1, y1 = pos[node]
    x2, y2 = pos[end]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5