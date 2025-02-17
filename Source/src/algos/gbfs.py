def gbfs(matrix, start, end):
    path = []
    visited = {start: None}
    pq = PriorityQueue()
    pq.put((0, start))

    frontier = [(start, 0)]
    while not pq.empty():
        _, node = pq.get()
        #print(f"frontier: {frontier}")
        if node == end:
            break

        for neighbor in range(len(matrix[node])):
            weight = matrix[node][neighbor]
            if weight and neighbor not in visited:
                pq.put((weight, neighbor))
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