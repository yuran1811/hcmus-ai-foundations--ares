def bfs(matrix, start, end):
    frontier = [start]
    visited = {start: None}
    path = []

    #print(f"frontier: {frontier}")

    while frontier:
        current = frontier.pop(0)
        if current == end:
            visited, path = construct_path(visited, end)
            return visited, path

        for neighbor in range(len(matrix[current])):
            if matrix[current][neighbor] and neighbor == end:
                visited[neighbor] = current
                visited, path = construct_path(visited, end)
                return visited, path  
            if matrix[current][neighbor] and neighbor not in visited:
                visited[neighbor] = current
                frontier.append(neighbor)
        #print(f"frontier: {frontier}")

    print(f"visited: {visited}")
    return visited, path
