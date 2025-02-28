def dfs(matrix, start, end):
    frontier = [(start, None)]
    visited = {}
    path = []

    while frontier:
        current, predecessor = frontier.pop()
        visited[current] = predecessor

        while len(path) > 0 and path[-1] != visited[current]:
            path.pop()
        path.append(current)

        if current == end:
            print("-----------------")
            print(f"visited: {visited}")
            print(f"path: {path}")
            return visited, path

        for neighbor in range(len(matrix[current]) - 1, -1, -1):
            if matrix[current][neighbor] != 0 and neighbor not in visited:
                frontier.append((neighbor, current))

    print(f"visited: {visited}")
    return visited, path