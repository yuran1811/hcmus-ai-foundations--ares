def dijkstra(matrix, start, end):
    n = len(matrix)
    distances = {i: float('infinity') for i in range(n)}
    distances[start] = 0
    
    visited = {} 
    frontier = [(0, start, None)] 
    path = []

    while frontier:
        current_dist, current, predecessor = min(frontier)
        frontier.remove((current_dist, current, predecessor))
        
        if current in visited:
            continue
            
        visited[current] = predecessor

        while len(path) > 0 and path[-1] != visited[current]:
            path.pop()
        path.append(current)

        if current == end:
            print("-----------------")
            print(f"visited: {visited}")
            print(f"path: {path}")
            print(f"distance: {distances[end]}")
            return visited, path, distances

        for neighbor in range(n):
            if matrix[current][neighbor] != 0 and neighbor not in visited:
                distance = distances[current] + matrix[current][neighbor]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    frontier.append((distance, neighbor, current))

    print(f"No path found!")
    return visited, path, distances